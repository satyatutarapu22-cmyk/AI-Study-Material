import json
from pathlib import Path
from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from docx import Document
from .database import get_db
from .ai_engine import analyze

main = Blueprint("main", __name__)
ALLOWED = {"pdf", "txt", "docx"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED

def extract_text(path):
    ext = Path(path).suffix.lower()
    if ext == ".pdf":
        reader = PdfReader(path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if ext == ".docx":
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs)
    return Path(path).read_text(encoding="utf-8", errors="ignore")

@main.route("/")
def index():
    conn = get_db()
    query = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    sql = "SELECT * FROM materials WHERE 1=1"
    params = []
    if query:
        sql += " AND (title LIKE ? OR category LIKE ? OR content LIKE ?)"
        like = f"%{query}%"
        params.extend([like, like, like])
    if category:
        sql += " AND category = ?"
        params.append(category)
    sql += " ORDER BY created_at DESC"
    materials = conn.execute(sql, params).fetchall()
    categories = conn.execute("SELECT DISTINCT category FROM materials ORDER BY category").fetchall()
    total = conn.execute("SELECT COUNT(*) FROM materials").fetchone()[0]
    conn.close()
    return render_template("index.html", materials=materials, categories=categories, total=total, query=query, selected_category=category)

@main.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("file")
        title = request.form.get("title", "").strip()
        if not file or not file.filename:
            flash("Please select a study file.", "error")
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash("Allowed files: PDF, TXT, DOCX.", "error")
            return redirect(request.url)
        filename = secure_filename(file.filename)
        save_path = Path(current_app.config["UPLOAD_FOLDER"]) / filename
        file.save(save_path)
        try:
            content = extract_text(save_path)
            if not content.strip():
                raise ValueError("The file contains no readable text.")
            category, summary, questions = analyze(content)
            final_title = title or Path(filename).stem.replace("_", " ").title()
            conn = get_db()
            conn.execute("INSERT INTO materials (title, filename, category, summary, content, questions) VALUES (?, ?, ?, ?, ?, ?)", (final_title, filename, category, summary, content, json.dumps(questions)))
            conn.commit()
            conn.close()
            flash("Study material organized successfully!", "success")
            return redirect(url_for("main.index"))
        except Exception as exc:
            if save_path.exists(): save_path.unlink()
            flash(f"Could not process the file: {exc}", "error")
            return redirect(request.url)
    return render_template("upload.html")

@main.route("/material/<int:material_id>")
def material(material_id):
    conn = get_db()
    item = conn.execute("SELECT * FROM materials WHERE id = ?", (material_id,)).fetchone()
    conn.close()
    if not item:
        flash("Material not found.", "error")
        return redirect(url_for("main.index"))
    return render_template("material.html", item=item, questions=json.loads(item["questions"] or "[]"))

@main.route("/delete/<int:material_id>", methods=["POST"])
def delete(material_id):
    conn = get_db()
    item = conn.execute("SELECT filename FROM materials WHERE id = ?", (material_id,)).fetchone()
    if item:
        conn.execute("DELETE FROM materials WHERE id = ?", (material_id,))
        conn.commit()
        path = Path(current_app.config["UPLOAD_FOLDER"]) / item["filename"]
        if path.exists(): path.unlink()
    conn.close()
    flash("Material deleted.", "success")
    return redirect(url_for("main.index"))

@main.route("/api/stats")
def stats():
    conn = get_db()
    rows = conn.execute("SELECT category, COUNT(*) AS count FROM materials GROUP BY category ORDER BY count DESC").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])
