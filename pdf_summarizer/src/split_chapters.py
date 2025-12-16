# src/split_chapters.py
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"


def split_one_txt(txt_path: Path):
    text = txt_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # 🔓 챕터 인식 기준을 "느슨하게"
    chapter_pattern = re.compile(
        r"^\s*(\d{1,3})\s*[\.|\)|]?\s*(.+)?$"
    )

    chapters = []
    seen_chapters = set()

    current_title = None
    current_content = []

    page_seen = False

    for line in lines:
        if re.search(r"\bPAGE\s*\d+\b", line, re.IGNORECASE):
            page_seen = True
            continue

        if not page_seen:
            continue  # PAGE 이전 텍스트 무시


        match = chapter_pattern.match(line)

        if match:
            chap_num = match.group(1)
            chap_title = (match.group(2) or "").strip()

            # 🔍 제목이 너무 짧거나 숫자만 있으면 무시
            if not (5 <= len(chap_title) <= 20):
                if current_title:
                    current_content.append(line)
                continue

            # 🔁 같은 챕터 번호 중복 방지
            if chap_num in seen_chapters:
                if current_title:
                    current_content.append(line)
                continue

            seen_chapters.add(chap_num)

            if current_title:
                chapters.append((current_title, "\n".join(current_content)))

            current_title = f"{chap_num}. {chap_title}"
            current_content = [line]
        else:
            if current_title:
                current_content.append(line)

    if current_title:
        chapters.append((current_title, "\n".join(current_content)))

    if not chapters:
        print(f"⚠️ 챕터 인식 실패: {txt_path.name}")
        return False

    chapter_dir = OUTPUTS_DIR / "chapters" / txt_path.stem
    chapter_dir.mkdir(parents=True, exist_ok=True)

    for i, (title, content) in enumerate(chapters, 1):
        safe_title = re.sub(r'[\\/:*?"<>|]', "", title)
        out_file = chapter_dir / f"{i:02d}_{safe_title}.txt"
        out_file.write_text(content.strip(), encoding="utf-8")

    print(f"✅ {txt_path.name} → 챕터 {len(chapters)}개 분리 완료")
    return True


def main():
    txt_files = list(OUTPUTS_DIR.glob("*.txt"))

    if not txt_files:
        print("❌ outputs 폴더에 txt 파일이 없습니다.")
        return

    for txt_file in txt_files:
        success = split_one_txt(txt_file)
        if success:
            txt_file.unlink()

    print("\n🎉 모든 txt 챕터 분리 작업 완료")


if __name__ == "__main__":
    main()













