import streamlit as st
import pypinyin
import csv
from os import environ
from google.cloud import translate

pinyinKanaMap = {}
# 翻訳
def translate_text(text: str, target_language_code: str) -> translate.Translation:
    if text: 
        PROJECT_ID = environ.get("PROJECT_ID", "")
        PARENT = f"projects/{PROJECT_ID}"
        client = translate.TranslationServiceClient()

        response = client.translate_text(
            parent=PARENT,
            contents=[text],
            target_language_code=target_language_code,
        )

        return response.translations[0]
    else:
        return

# ピン音
def pinyin(word, style=pypinyin.NORMAL):
    s = ''
    for i in pypinyin.pinyin(word, style):
    #for i in pypinyin.pinyin(word, heteronym=True):
        #print(i[0])
        s += i[0]
        s += " "
    return s

def loadPinyinKana():
    csv_header = ["pinyin","kana"]
    pinyinKanaMap = {}
    with open('./pinyinkana.csv', 'r',encoding="utf-8_sig") as f:
    # DictReaderと共にHeaderを渡すことで辞書形式で返す。
    # 取得したデータを1行ずつ出力。
        for row in csv.DictReader(f, csv_header):
            pinyinKanaMap[row["pinyin"]] = row["kana"]
    return pinyinKanaMap

def pinyin_to_kana(line):
    s = ''
    for word in line.split():
        if word in pinyinKanaMap:
            s += pinyinKanaMap[word]
            s += " "
    return s


##### 
def main():
    pinyinKanaMap = loadPinyinKana()
    label = "中国語（簡体字）"

    trans_on = st.toggle("翻訳(日)")

    # 入力
    # input_text = st.text_area(label, value="", height=None, max_chars=None, key=None, help=None, on_change=None, args=None, kwargs=None, *, placeholder=None, disabled=False, label_visibility="visible")

    input_text = st.text_area(
        label
    )

    # 変換

    # 翻訳
    transLines = []
    if trans_on:
        translation = translate_text(input_text, 'ja')
        st.markdown(">"+translation.translated_text+"")

    # 拼音併記
    for line in input_text.splitlines():
        if line:
            #NORMALピンイン
            pinyin_text = pinyin(line, pypinyin.STYLE_NORMAL)
            #st.text(pinyin_text)
            #ピンイン->カナ
            kana_text = pinyin_to_kana(pinyin_text)
            #四声つきピンイン
            pinyin_text = pinyin(line, pypinyin.STYLE_TONE)

            st.caption(kana_text)
            st.text(pinyin_text)
            st.markdown("**"+line+"**")
            #st.divider()
        else:
            st.divider()

main()