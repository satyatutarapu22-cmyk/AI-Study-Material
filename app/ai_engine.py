import re
from collections import Counter

SUBJECT_KEYWORDS = {
    "Python": ["python", "numpy", "pandas", "function", "list", "dictionary", "tuple", "class"],
    "Data Science": ["data science", "dataset", "data analysis", "machine learning", "statistics", "visualization"],
    "Web Development": ["html", "css", "javascript", "web", "dom", "http", "frontend", "backend"],
    "Database": ["database", "sql", "mysql", "mongodb", "table", "query", "normalization"],
    "Computer Networks": ["network", "tcp", "ip", "router", "protocol", "osi", "http"],
    "Operating Systems": ["operating system", "process", "thread", "deadlock", "paging", "semaphore"],
    "Artificial Intelligence": ["artificial intelligence", "ai", "neural network", "deep learning", "nlp", "computer vision"],
    "Cyber Security": ["security", "cyber", "encryption", "malware", "firewall", "authentication"],
}
STOP_WORDS = {"the","and","for","that","this","with","from","are","was","were","have","has","into","their","there","which","about","using","used","than","then","also","can","will","would","should","these","those","your","you","our","they","them","its","not","but","what","when","where","how","why","who","a","an","of","to","in","on","is","as"}

def clean_text(text):
    return re.sub(r"\s+", " ", text or "").strip()

def detect_category(text):
    lower = text.lower()
    scores = {category: sum(lower.count(word) for word in words) for category, words in SUBJECT_KEYWORDS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "General"

def important_words(text, limit=8):
    words = re.findall(r"[A-Za-z][A-Za-z0-9+#-]{2,}", text.lower())
    counts = Counter(w for w in words if w not in STOP_WORDS)
    return [word for word, _ in counts.most_common(limit)]

def summarize(text, max_sentences=5):
    text = clean_text(text)
    if not text:
        return "No readable text was found in this material."
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if len(s.strip()) > 35]
    if not sentences:
        return text[:700] + ("..." if len(text) > 700 else "")
    keywords = set(important_words(text, 12))
    scored = []
    for index, sentence in enumerate(sentences):
        words = set(re.findall(r"[A-Za-z][A-Za-z0-9+#-]{2,}", sentence.lower()))
        scored.append((len(words & keywords), -index, sentence))
    selected = sorted(scored, reverse=True)[:max_sentences]
    selected = sorted(selected, key=lambda x: -x[1])
    return " ".join(item[2] for item in selected)

def generate_questions(text, category):
    keywords = important_words(text, 5)
    templates = [
        "What is {topic} and why is it important?",
        "Explain the main features or concepts of {topic}.",
        "How is {topic} used in practical applications?",
        "What are the advantages and limitations related to {topic}?",
        "Write a short note on {topic}."
    ]
    questions = [templates[i].format(topic=topic) for i, topic in enumerate(keywords[:5])]
    return questions or [
        f"What are the important concepts in {category}?",
        f"Explain the basic principles of {category}.",
        f"Give practical examples related to {category}."
    ]

def analyze(text):
    category = detect_category(text)
    return category, summarize(text), generate_questions(text, category)
