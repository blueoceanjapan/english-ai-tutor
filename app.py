import streamlit as st
import google.generativeai as genai

# ページの設定
st.set_page_config(
    page_title="中学英語 動名詞一問一答ドリル", page_icon="📝", layout="centered"
)

st.title("📝 中学2年英語：動名詞 一問一答ドリル")
st.write(
    "動名詞（〜すること / enjoy, finish, stop, mind など）の基礎を固めるためのドリル型AIチューターです。答えを入力すると、AIが誤答の分析と類題を出してくれます！"
)

# サイドバー：APIキー入力
st.sidebar.header("設定")
api_key = st.sidebar.text_input("Gemini API Key を入力", type="password")

if not api_key:
    st.warning("👈 左側のサイドバーに Gemini API Key を入力してください。")
    st.stop()

# APIの設定
genai.configure(api_key=api_key)
# 安定性の高い Gemini 2.5 Flash または 1.5 Flash を使用
model = genai.GenerativeModel("gemini-3.8-flash")

# セッション状態の初期化
if "current_question" not in st.session_state:
    st.session_state.current_question = (
        "次の日本語を英語に訳しなさい。\n「私はテニスをすることが好きです。」 (playを使わず、likeを使用)"
    )
    st.session_state.correct_answer = "I like playing tennis."
    st.session_state.history = []
    st.session_state.feedback = ""
    st.session_state.next_ready = False

# 問題表示エリア
st.markdown("### 📌 現在の問題")
st.info(st.session_state.current_question)

# ユーザーの解答入力
user_answer = st.text_input("あなたの解答を入力してください:", key="user_input")

col1, col2 = st.columns(2)

with col1:
    if st.button("回答する 🚀", type="primary"):
        if not user_answer:
            st.warning("解答を入力してください。")
        else:
            with st.spinner("AIが解答を分析中..."):
                # プロンプトの構築（誤答分析と類題作成を指示）
                prompt = f"""
あなたは中学2年生向けの丁寧で優しい英語の個別指導AIチューターです。
以下の問題に対する生徒の解答を分析し、フィードバックと類題を作成してください。

【単元】中学2年 英語「動名詞」
【問題】{st.session_state.current_question}
【模範解答】{st.session_state.correct_answer}
【生徒の解答】{user_answer}

以下のフォーマットで出力してください（Markdown形式）：
1. **判定**: 「正解！」または「惜しい！」、「不正解…」
2. **解説**: なぜその形になるのかの分かりやすい解説。
3. **つまずき分析**: もし間違えている場合、生徒がどこで勘違いしているか（例：不定詞と混同している、動詞の原形になっている等）の分析。
4. **類題出題**: 定着のために、**まったく同じ文法ルールの新しい問題（一問一答）を1問だけ**新しく出してください。
"""
                response = model.generate_content(prompt)
                st.session_state.feedback = response.text
                st.session_state.history.append(
                    {
                        "q": st.session_state.current_question,
                        "a": user_answer,
                        "f": response.text,
                    }
                )
                st.session_state.next_ready = True

# フィードバックの表示
if st.session_state.feedback:
    st.markdown("---")
    st.markdown("### 🔍 AIチューターからのフィードバック・分析")
    st.write(st.session_state.feedback)

# 次の問題へ進むボタン
if st.session_state.next_ready:
    st.markdown("---")
    if st.button("次の類題に進む ➡️"):
        with st.spinner("次の問題を作成中..."):
            # これまでのやり取りを基に、新しい動名詞の問題をAIに作成させる
            gen_prompt = """
あなたは中学2年生向けの優れた英語教師AIです。
動名詞（gerund）の学習用として、次の類題を1問作成してください。
必ず以下のフォーマット（目印）に従って出力してください。

[問題]
次の日本語を英語に訳しなさい。「〇〇」 (...)

[模範解答]
〇〇〇〇〇〇.
"""
            res = model.generate_content(gen_prompt)
        response_text = res.text.strip()

        # AIの出力から「問題」と「模範解答」を切り分けてセッションに保存する
        if "[模範解答]" in response_text:
            parts = response_text.split("[模範解答]")
            question_part = parts[0].replace("[問題]", "").strip()
            answer_part = parts[1].strip()
            
            st.session_state.current_question = question_part
            st.session_state.correct_answer = answer_part
        else:
            # 万が一フォーマットがズレた場合の保険
            st.session_state.current_question = response_text
            st.session_state.correct_answer = "I like playing tennis."

        # 次の問題へ進んだので、前のフィードバックやボタン状態をリセット
        st.session_state.feedback = ""
        st.session_state.next_ready = False
