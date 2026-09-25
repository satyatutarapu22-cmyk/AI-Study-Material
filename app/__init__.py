from flask import Flask
from pathlib import Path
from .database import init_db

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "change-this-secret-key"
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
    base_dir = Path(app.root_path).parent
    app.config["UPLOAD_FOLDER"] = str(base_dir / "uploads")
    Path(app.config["UPLOAD_FOLDER"]).mkdir(exist_ok=True)
    init_db()
    from .routes import main
    app.register_blueprint(main)
    return app
