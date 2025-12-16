# src/summarize_chapters.py
import re
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent.parent
CHAPTERS_ROOT = BASE_DIR / "outputs" / "chapters"
SUMMARIES_ROOT = BASE_DIR / "outputs" / "summaries" / "summarized"

SUMMARY_SENTENCES = 5


# =====================
# 텍스트 정제
# =====================
def clean_text(text: str) -> str:
    text = re.sub(r"\b[Pp][Aa][Gg][Ee]\s*\d+\b", "", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"www\.\S+", "", text)
    # (숫자). 또는 숫자. 제거
    text = re.sub(r"\(\d+\)\.|\b\d+\.", "", text)
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def split_sentences(text: str):
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if len(s.strip()) > 20]


def extract_keywords(text: str, top_k=20):
    words = re.findall(r"[가-힣]{2,}", text)
    return {w for w, _ in Counter(words).most_common(top_k)}


def score_sentences(sentences, keywords):
    scores = {}
    for i, s in enumerate(sentences):
        score = sum(2 for k in keywords if k in s)
        if i < 5:
            score += 2
        if len(s) > 75:
            score -= 1
        scores[s] = score
    return scores


def summarize_chapter(txt_path: Path) -> str:
    text = clean_text(txt_path.read_text(encoding="utf-8"))
    sentences = split_sentences(text)
    if not sentences:
        return "- 요약 불가"

    keywords = extract_keywords(text)
    scores = score_sentences(sentences, keywords)

    top = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:SUMMARY_SENTENCES]
    ordered = sorted([s for s, _ in top], key=lambda s: sentences.index(s))

    return "\n".join(f"- {s}" for s in ordered)


# =====================
# 전체 요약 실행
# =====================
def main():
    if not CHAPTERS_ROOT.exists():
        print("❌ outputs/chapters 폴더가 없습니다.")
        return

    doc_dirs = [d for d in CHAPTERS_ROOT.iterdir() if d.is_dir()]
    if not doc_dirs:
        print("❌ chapters 안에 문서 폴더가 없습니다.")
        return

    for doc_dir in doc_dirs:
        out_dir = SUMMARIES_ROOT / doc_dir.name
        out_dir.mkdir(parents=True, exist_ok=True)

        txt_files = sorted(doc_dir.glob("*.txt"))
        if not txt_files:
            print(f"⚠️ {doc_dir.name} 폴더에 txt 없음")
            continue

        for txt_file in txt_files:
            summary = summarize_chapter(txt_file)
            out_file = out_dir / txt_file.name
            out_file.write_text(summary, encoding="utf-8")
            print(f"✅ {doc_dir.name} / {txt_file.name}")

    print(f"\n🎉 모든 문서 요약 완료 → {SUMMARIES_ROOT}")


if __name__ == "__main__":
    main()







