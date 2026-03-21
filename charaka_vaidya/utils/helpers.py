
import re, json, os

def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def load_json(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)

def save_json(data: dict, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def truncate(text: str, n: int = 150) -> str:
    return text[:n] + "..." if len(text) > n else text

def build_herb_key(name: str) -> str:
    return name.lower().split("(")[0].strip().replace(" ", "_")
