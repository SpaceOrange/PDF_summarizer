import extract_text
import split_chapters
import summarize_chapters
import summaries_to_pdf

def run():
    print("\n🚀 [1/4] 텍스트 추출 시작")
    extract_text.main()

    print("\n🚀 [2/4] 챕터 분리 시작")
    split_chapters.main()

    print("\n🚀 [3/4] 챕터 요약 시작")
    summarize_chapters.summarize_all()

    print("\n🚀 [4/4] PDF 생성 시작")
    summaries_to_pdf.main()

    print("\n🎉 전체 파이프라인 완료!")

if __name__ == "__main__":
    run()
