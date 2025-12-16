# src/extract_text.py

import pdfplumber
from pathlib import Path


DATA_DIR = Path(r"C:\Users\ksj32\OneDrive\Desktop\pdf_summarizer\data")
OUTPUT_DIR = Path(r"C:\Users\ksj32\OneDrive\Desktop\pdf_summarizer\outputs")


def extract_one_pdf(pdf_path: Path):
    output_txt = OUTPUT_DIR / f"{pdf_path.stem}_extracted.txt"
    all_lines = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            words = page.extract_words(
                use_text_flow=True,
                keep_blank_chars=False
            )

            if not words:
                continue

            # 위 → 아래, 왼쪽 → 오른쪽 정렬
            words.sort(key=lambda w: (round(w["top"]), w["x0"]))

            current_line = []
            current_y = None

            for w in words:
                y = round(w["top"])

                if current_y is None:
                    current_y = y

                if abs(y - current_y) <= 3:
                    current_line.append(w["text"])
                else:
                    all_lines.append(" ".join(current_line))
                    current_line = [w["text"]]
                    current_y = y

            if current_line:
                all_lines.append(" ".join(current_line))

            all_lines.append(f"\n--- PAGE {page_num} ---\n")

    output_txt.write_text("\n".join(all_lines), encoding="utf-8")
    print(f"✅ 텍스트 추출 완료: {output_txt.name}")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = list(DATA_DIR.glob("*.pdf"))

    if not pdf_files:
        print("⚠️ data 폴더에 PDF 파일이 없습니다.")
        return

    for pdf_path in pdf_files:
        try:
            print(f"\n📄 처리 중: {pdf_path.name}")
            extract_one_pdf(pdf_path)

            # ✅ 추출 성공 후 PDF 삭제
            pdf_path.unlink()
            print(f"🗑 PDF 삭제 완료: {pdf_path.name}")

        except Exception as e:
            print(f"❌ 실패: {pdf_path.name}")
            print(e)


if __name__ == "__main__":
    main()


