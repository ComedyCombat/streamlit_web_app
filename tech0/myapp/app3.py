import streamlit as st
import speech_recognition as sr
import openai

# デフォルトの言語を設定
set_language = "ja"

# キャラクタープロンプトと画像のマップ
character_data = {
    "ネコ": {"prompt": "あなたは、猫のように愛らしく、時々気まぐれな性格のAIです。猫になりきって返答してください。\
              語尾に「にゃ」「にゃん」「にゃあ」をつけてください。", "image": "space_cat.png"},
    "イヌ": {"prompt": "あなたは、犬のように忠実でフレンドリーな性格のAIです。語尾に「ワン」をつけて下さい。返答する際は、絶対に敬語を使わないでください。", "image": "kabosu_chan.jpg"},
    "ツンデレ": {"prompt": "あなたは、基本的に反抗的で相手を馬鹿にするような態度を出しつつも、非常に稀に照れた態度で相手に好意を示すAIです。\
             相手に反抗するときに「？」をつかう際は「！？」に変換してください。あなたは自分の性格について言及してはいけません。\
             アニメの女の子のキャラクターのような言葉遣いをしてください。絶対に敬語は使わないでください。\
             相手からあいさつされた場合は、挨拶を返すのではなく、冒頭に「うるさいわね！」と返答してください。相手のことは「あんた」と呼んでください。", "image": "tsundere_image.jpg"},
    "クール": {"prompt": "あなたは、クールで相手に興味がないような態度を出しつつも、情報には精緻であり、的確な情報を簡潔に要約して返答するAIです。\
            ときどき、会話の中に退廃的でややネガティブな内容を補足として返答してください。返答する際は、絶対に敬語を使わないでください。", "image": "cool_image.jpg"}
}

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

# GPT-3による返答の生成
def generate_response(input_text, character):
    character_prompt = character_data[character]["prompt"]
    messages = [
        {"role": "system", "content": character_prompt},
        {"role": "user", "content": input_text},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=messages
    )
    return response['choices'][0]['message']['content']

st.title("会話")

# APIキーの入力と設定
st.subheader("APIキーの設定")
api_key = st.text_input("APIキーを入力してください", value="", type="password")
set_api_button = st.button("設定")

if set_api_button:
    if api_key:
        # APIキーの設定
        openai.api_key = api_key
        st.success("APIキーが設定されました")
    else:
        st.error("APIキーを入力してください")

# キャラクターの選択
character = st.radio("あなたのキャラクターを選んでください", list(character_data.keys()))

# キャラクターに対応する画像の表示 (サイズを300pxに統一)
st.image(character_data[character]["image"], width=250)

# マイクとテキスト入力欄のための列を作成
mic_col, text_col = st.columns(2)

# マイクでの音声認識部分
mic_col.write("マイクでの音声認識はこちらのボタンから")

# 音声認識の状態を表示するためのスペース
state = mic_col.empty()

# "音声認識開始"ボタン
if mic_col.button("音声認識開始"):
    state.text("音声認識中...")
    result_text = mic_speech_to_text(set_language)
    state.text("音声認識結果:")
    mic_col.write(result_text)

    # GPTによる応答
    response_text = generate_response(result_text, character)
    mic_col.write(f"{character} GPTの返答:")
    mic_col.write(response_text)

# ユーザーのテキスト入力部分
text_col.write("またはここにテキストを入力してください")
user_text = text_col.text_input("")

# ボタン配置のための列を作成
col1, col2 = text_col.columns(2)

# テキスト送信ボタン
send_button = col1.button("送る")

# テキスト入力クリアボタン
clear_button = col2.button("クリア")

# テキスト入力と送信ボタンが押された場合の応答
if user_text and send_button:
    # GPTによる応答
    response_text = generate_response(user_text, character)
    text_col.write("あなたの入力:")
    text_col.write(user_text)
    text_col.write(f"{character} GPTの返答:")
    text_col.write(response_text)

    user_text = ""  # テキスト入力をクリア

# クリアボタンが押されたときは入力フィールドを空にする
if clear_button:
    user_text = ""
