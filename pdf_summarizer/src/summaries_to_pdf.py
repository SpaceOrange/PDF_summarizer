from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
import shutil

# =====================
# 📁 경로 설정
# =====================
BASE_DIR = Path(__file__).resolve().parent.parent
SUMMARIES_ROOT = BASE_DIR / "outputs" / "summaries"
FONT_PATH = BASE_DIR / "fonts" / "NotoSansKR-Regular.ttf"

pdfmetrics.registerFont(TTFont("NotoKR", str(FONT_PATH)))

# =====================
# 🎨 스타일
# =====================
styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name="ChapterTitleKR",
    fontName="NotoKR",
    fontSize=18,
    leading=22,
    spaceBefore=20,
    spaceAfter=14
))

styles.add(ParagraphStyle(
    name="BodyKR",
    fontName="NotoKR",
    fontSize=11,
    leading=16,
    leftIndent=16,
    spaceAfter=6
))


def main():
    if not SUMMARIES_ROOT.exists():
        print("❌ summaries 폴더가 없습니다.")
        return

    txt_files = sorted(SUMMARIES_ROOT.rglob("*.txt"))

    if not txt_files:
        print("❌ 요약 txt 파일을 찾지 못했습니다.")
        return

    pdf_name = input("📄 생성할 PDF 파일 이름 (확장자 제외): ").strip() or "summary_result"
    output_pdf = BASE_DIR / "outputs" / f"{pdf_name}.pdf"

    doc = SimpleDocTemplate(
        str(output_pdf),
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    elements = []

    for txt_file in txt_files:
        lines = txt_file.read_text(encoding="utf-8").splitlines()
        if not lines:
            continue

        # 📌 챕터 제목 = 파일명
        chapter_title = txt_file.stem.replace("_", " ")
        elements.append(Paragraph(chapter_title, styles["ChapterTitleKR"]))
        elements.append(Spacer(1, 8))

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith("-"):
                line = "• " + line.lstrip("- ").strip()

            elements.append(Paragraph(line, styles["BodyKR"]))

        elements.append(Spacer(1, 24))

    doc.build(elements)

    # 🧹 summaries 폴더 전체 정리
    shutil.rmtree(SUMMARIES_ROOT)

    print(f"✅ PDF 생성 완료: {output_pdf}")
    print("🧹 summaries 폴더 자동 정리 완료")


if __name__ == "__main__":
    main()
















