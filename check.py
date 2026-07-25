"""Self-check for the question bank. Fails loudly on a malformed entry."""
import json, pathlib, collections, sys

qs = json.loads((pathlib.Path(__file__).parent / "questions.json").read_text(encoding="utf-8"))

assert len(qs) == 180, f"expected 180 questions, got {len(qs)}"
ids = [q["id"] for q in qs]
dupes = [i for i, n in collections.Counter(ids).items() if n > 1]
assert not dupes, f"duplicate ids: {dupes}"
assert sorted(ids) == list(range(1, 181)), f"ids are not 1..180: missing {set(range(1,181)) - set(ids)}"

for q in qs:
    w = f"q{q['id']}"
    assert len(q["opts"]) == 4, f"{w}: {len(q['opts'])} options, expected 4"
    assert len(set(q["opts"])) == 4, f"{w}: duplicate option text"
    assert isinstance(q["correct"], int) and 0 <= q["correct"] <= 3, f"{w}: bad correct index"
    assert q["conf"] in ("high", "med", "low"), f"{w}: bad conf {q['conf']!r}"
    for f in ("q", "why", "src", "topic"):
        assert q.get(f, "").strip(), f"{w}: empty field {f}"

by_conf = collections.Counter(q["conf"] for q in qs)
by_ans = collections.Counter(q["correct"] for q in qs)
print(f"OK  180 questions  |  conf: {dict(by_conf)}  |  answer spread a/b/c/d: "
      f"{[by_ans[i] for i in range(4)]}")
low = [q["id"] for q in qs if q["conf"] == "low"]
if low:
    print(f"unverified (check these yourself): {low}")
