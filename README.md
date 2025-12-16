# pdf_summarizer

**src폴더 안에 있는 extract_text.py, split_chapters.py, summarize_chapters.py, summeries_to_pdf.py순서로 실행시키시면 됩니다.**

**아래 내용도 꼭 읽어주세요**

**아래는 각 파이썬 파일을 실행시키는 방법입니다.**

1. 파일을 켜줍니다

2. ctrl + shift + ~ 를 눌러 터미널을 열어줍니다

3. cd pdf_summarizor로 경로를 설정해줍니다. 터미널에 cd입력후 사진속 빨간 부분(dpf_summarizer)를 드래그해줍니다.

4. 경로 설정후 실행하고자 하는 파일을 아래 방법대로 실행시키시면 됩니다

pdf파일에서 텍스트를 추출해서 요약 후 pdf를 만들어줍니다.

**중요** 사용하시기전에 data폴더의 Hello, outputs/chapters폴더의 World! txt파일들은 지우고 사용해주세요!

**중요** 다운로드 후 사용하시기 전 requirements.txt를 읽어주세요!

<img width="1724" height="744" alt="data" src="https://github.com/user-attachments/assets/441259b2-7bf0-4099-832e-9b068c7ecd85" />

data폴더에 요약하고자 하는 pdf를 넣습니다.

extract_text.py를 실행시켜서 pdf에서 텍스트를 추출합니다. 터미널에 python src/extract_text.py를 입력합니다

<img width="1610" height="742" alt="output" src="https://github.com/user-attachments/assets/fbb4d9a0-e163-4c95-ac72-94906664a9ee" />

추출된 텍스트들은 outputs폴더에 txt파일로 저장됩니다. 
그 후 split_chapters.py를 실행시키면 추출한 텍스트에서 챕터들을 분류해 각각의 txt파일로 만들어줍니다. 터미널에 python src/split_chapters.py를 입력합니다.

<img width="2222" height="1120" alt="chap" src="https://github.com/user-attachments/assets/7c541287-bf73-4c21-aa6a-267401119fef" />

이 파일들은 outputs/chapters폴더에 하위 폴더를 만들고 그 안에 저장됩니다. 

이제 summarize_chapters.py를 실행시키면 각각의 챕터txt파일들의 내용을 요약해줍니다. 터미널에 python src/summarize_chapters.py를 입력합니다

그 후 summaries_to_pdf.py를 실행시키면 최종 pdf가 완성됩니다. 터미널에 python src/summaries_to_pdf.py를 입력합니다.
