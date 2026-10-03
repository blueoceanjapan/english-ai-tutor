from google import genai
import streamlit as st

st.set_page_config(page_title="中学英語 AI個別指導チューター", layout="centered")

st.title("🎓 中学英語 AI個別指導チューター")
st.markdown(
    "英語の文法や英作文について、AIの先生に質問してみよう！"
    "（答えをそのまま教えず、考えるヒントをくれます）"
)

# APIキーの入力欄
api_key = st.text_input("Gemini API Key を入力してください", type="password")

if api_key:
  client = genai.Client(api_key=api_key)

  # ユーザー入力欄
  user_input = st.text_area(
      "先生に質問したいことや、書いた英文を入力してね",
      "例: He readed a book yesterday. って書いたんだけど、どこが変かな？",
      height=100,
  )

  if st.button("先生に相談する"):
    if user_input:
      with st.spinner("AIチューターが考えています..."):
        try:
          system_instruction = (
              "あなたは中学生向けの優しくフレンドリーな英語学習AIチューター（個別指導の先生）です。"
              "生徒が入力した英文の誤りや質問に対して、以下の方針でサポートしてください。\n"
              "1. まず褒めて励ます\n"
              "2. 答えをそのまま教えず、気づきを促すためのヒントや問いかけを与える\n"
              "3. 分かりやすい解説と例示を添える\n"
              "4. 中学生が親しみを持てる、丁寧で温かいトーン（「〜だよ！」「〜してみよう！」など）を使う。"
          )

          prompt = f"{system_instruction}\n\n【生徒からの入力・質問】\n{user_input}"

          response = client.models.generate_content(
              model="gemini-3.8-flash",
              contents=prompt,
          )

          st.subheader("💡 AIチューターからのアドバイス")
          st.markdown(response.text)

        except Exception as e:
          st.error(f"エラーが発生しました: {e}")
    else:
      st.warning("入力欄にメッセージを入力してください。")
else:
  st.info("👆 Google AI Studio で取得した API キーを入力してください。")
