import streamlit as st
import pypinyin
import csv
from os import environ
from google.cloud import translate

# 翻訳
def translate_text(text: str, target_language_code: str) -> str:
    if not text:
        return ""
    
    PROJECT_ID = environ.get("PROJECT_ID", "")
    PARENT = f"projects/{PROJECT_ID}"
    client = translate.TranslationServiceClient()

    response = client.translate_text(
        parent=PARENT,
        contents=[text],
        target_language_code=target_language_code,
    )

    return response.translations[0].translated_text

# ピン音
def pinyin(word, style=pypinyin.NORMAL) -> str:
    return ' '.join(i[0] for i in pypinyin.pinyin(word, style))

def load_pinyin_kana() -> dict:
    pinyin_kana_map = {}
    with open('./pinyinkana.csv', 'r', encoding="utf-8_sig") as f:
        for row in csv.DictReader(f):
            pinyin_kana_map[row["pinyin"]] = row["kana"]
    return pinyin_kana_map

def pinyin_to_kana(line: str, pinyin_kana_map: dict) -> str:
    return ' '.join(pinyin_kana_map[word] for word in line.split() if word in pinyin_kana_map)

def main():
    pinyin_kana_map = load_pinyin_kana()
    label = "中国語（簡体字）"
    trans_on = st.toggle("翻訳(日)")

    input_text = st.text_area(label)

    if trans_on:
        translation = translate_text(input_text, 'ja')
        st.markdown(f"> {translation}")

    for line in input_text.splitlines():
        if line.strip():
            normal_pinyin = pinyin(line, pypinyin.STYLE_NORMAL)
            kana_text = pinyin_to_kana(normal_pinyin, pinyin_kana_map)
            tone_pinyin = pinyin(line, pypinyin.STYLE_TONE)

            st.caption(kana_text)
            st.text(tone_pinyin)
            st.markdown(f"**{line}**")
        else:
            st.divider()

if __name__ == "__main__":
    main()
