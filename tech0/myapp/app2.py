import streamlit as st
import speech_recognition as sr
import openai

# OpenAIのAPIキーを設定
openai.api_key = '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'

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

# キャラクターの選択
character = st.radio("あなたのキャラクターを選んでください", list(character_data.keys()))

# キャラクターに対応する画像の表示 (サイズを300pxに統一)
st.image(character_data[character]["image"], width=250)

st.write("マイクでの音声認識はこちらのボタンから")

# 音声認識の状態を表示するためのスペース
state = st.empty()

# "音声認識開始"ボタン
if st.button("音声認識開始"):
    state.text("音声認識中...")
    result_text = mic_speech_to_text(set_language)
    state.text("音声認識結果:")
    st.write(result_text)
    
    # GPTによる応答
    response_text = generate_response(result_text, character)
    st.write(f"{character} GPTの返答:")
    st.write(response_text)

# ユーザーのテキスト入力
user_text = st.text_input("またはここにテキストを入力してください")

# ボタン配置のための列を作成
# ボタン配置のための列を作成

col1, col2 = st.columns(2)


# テキスト送信ボタン
send_button = col1.button("送る")

# テキスト入力クリアボタン
clear_button = col2.button("クリア")

# テキスト入力と送信ボタンが押された場合の応答
if user_text and send_button:
    # GPTによる応答
    response_text = generate_response(user_text, character)
    st.write("あなたの入力:")
    st.write(user_text)
    st.write(f"{character} GPTの返答:")
    st.write(response_text)

    user_text = ""  # テキスト入力をクリア

# クリアボタンが押されたときは入力フィールドを空にする
if clear_button:
    user_text = ""
