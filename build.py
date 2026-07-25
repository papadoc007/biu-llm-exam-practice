"""Merge parts/*.json into questions.json and inline it into index.html."""
import json, pathlib

HERE = pathlib.Path(__file__).parent
qs = []
for p in sorted((HERE / "parts").glob("*.json")):
    qs += json.loads(p.read_text(encoding="utf-8"))
qs.sort(key=lambda q: q["id"])

(HERE / "questions.json").write_text(
    json.dumps(qs, ensure_ascii=False, indent=1), encoding="utf-8")

tpl = (HERE / "app.html").read_text(encoding="utf-8")
blob = json.dumps(qs, ensure_ascii=False).replace("</", "<\\/")
(HERE / "index.html").write_text(tpl.replace("__QUESTIONS__", blob), encoding="utf-8")

print(f"{len(qs)} questions -> questions.json, index.html")
