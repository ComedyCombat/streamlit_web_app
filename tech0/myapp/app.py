import streamlit as st
import speech_recognition as sr

# デフォルトの言語を設定
set_language = "ja"

# 音声認識の関数を定義
def mic_speech_to_text(language):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        return r.recognize_google(audio, language=language)
    except sr.UnknownValueError:
        return "音声を認識できませんでした"
    except sr.RequestError:
        return "音声認識サービスに接続できませんでした"

st.title("文字起こしアプリ")
st.write("マイクでの音声認識はこちらのボタンから")

state = st.empty()

# "音声認識開始"ボタンと"終了"ボタン
start_button = st.button("音声認識開始")
stop_button = st.button("終了")

if start_button:
    state.write("音声認識中...")
    while not stop_button:
        result_text = mic_speech_to_text(set_language)
        state.write("音声認識結果:")
        st.write(result_text)
        stop_button = st.button("終了")  # 終了ボタンの状態を更新
