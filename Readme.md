# About
簡体字をピン音とカタカナに変換します
Google翻訳も一応可能

Streamlit利用しています

```
streamlit run app.py
```

# Use

## pinyin 変換
pypinyin
https://pypi.org/project/pypinyin/

## Pinyinとカナ対応
https://cn.heibonsha.co.jp/

* 平凡社メディアガイドラインを参考に対応作成
* pypinyinとの組み合わせのため、üはvに記述変更して追加


## Google Cloud
翻訳部分
https://cloud.google.com/translate/docs?hl=ja

Google Cloud Shellで有効にする
```
gcloud services enable translate.googleapis.com
```

## ローカル環境用Google　Cloud設定
https://cloud.google.com/docs/authentication/provide-credentials-adc?hl=ja

### Google Cloud CLIインストール時のエラーについて
./google-cloud-sdk/install.sh の実行でエラー発生した(Mac M1)
```
AttributeError: module 'google._upb._message' has no attribute 'MessageMapContainer' 
```
以下コマンドを打ってから再度install.sh実行でインストール完了
```
pip install proto-plus==1.24.0.dev1
```

```
$ gcloud components update
```


```
gcloud init
```
利用プロジェクトの設定など

```
 gcloud config get-value core/project
 ```

 ローカル環境での認証

 ```
 gcloud auth application-default login
 ```