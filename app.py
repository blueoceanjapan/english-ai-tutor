import json
import os
import streamlit as st
import google.generativeai as genai

# ページ設定
st.set_page_config(
    page_title="中2英語 AI個別学習支援ドリル (動名詞)", page_icon="📚", layout="centered"
)

# APIキーの設定
if "GEMINI_API_KEY" in st.secrets:
  genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
elif os.environ.get("GEMINI_API_KEY"):
  genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# モデルの初期化 (Gemini 3.8 Flash)
@st.cache_resource
def get_model():
  return genai.GenerativeModel("gemini-3.8-flash")


model = get_model()

# セッション状態の初期化
if "current_question" not in st.session_state:
  st.session_state.current_question = (
      "次の日本語を英語に訳しなさい。「私はテニスをすることが好きです。」"
      "（playを使わず、likeを使用）"
  )
if "correct_answer" not in st.session_state:
  st.session_state.correct_answer = "I like playing tennis."
if "current_grammar_point" not in st.session_state:
  st.session_state.current_grammar_point = "like ＋ 動名詞"
if "history" not in st.session_state:
  st.session_state.history = []
if "feedback" not in st.session_state:
  st.session_state.feedback = ""
if "next_ready" not in st.session_state:
  st.session_state.next_ready = False

st.title("📚 中2英語 AI個別学習支援ドリル")
st.markdown("### 単元：動名詞 (Gerund) - 適応型AI学習システム")
st.markdown("---")

# 1. 問題の表示
st.info(
    f"**【問題】**\n\n{st.session_state.current_question}\n\n*（現在の焦点文法項目: `{st.session_state.current_grammar_point}`）*"
)

# 2. 解答入力フォーム
with st.form("answer_form"):
  user_answer = st.text_input(
      "あなたの解答を入力してください（例: I like playing tennis.）"
  )
  submit_button = st.form_submit_button("回答する 🚀")

# 3. 採点・分析の処理
if submit_button and user_answer:
  with st.spinner("AIが解答を分析中..."):
    eval_prompt = f"""
    あなたは中学2年生向けの優しく丁寧な英語学習AIチューターです。
    以下の問題に対して、生徒が回答しました。この回答を採点し、つまずきを分析してください。

    [問題]
    {st.session_state.current_question}

    [模範解答]
    {st.session_state.correct_answer}

    [生徒の回答]
    {user_answer}

    以下の形式で出力してください：
    1. 正誤判定（「正解！」または「要修正・不正解」から始める）
    2. なぜ間違えたのか、あるいはどこが素晴らしいかの丁寧な解説
    """

    eval_response = model.generate_content(eval_prompt)
    feedback_text = eval_response.text

    # 正誤判定の判定補助
    is_correct = (
        "正解！" in feedback_text
        or user_answer.strip().lower()
        == st.session_state.correct_answer.strip().lower()
    )

    st.session_state.feedback = feedback_text

    # 履歴への保存（文法タグや正誤を詳細に蓄積）
    st.session_state.history.append({
        "question": st.session_state.current_question,
        "user_answer": user_answer,
        "correct_answer": st.session_state.correct_answer,
        "grammar_point": st.session_state.current_grammar_point,
        "is_correct": is_correct,
        "feedback": feedback_text,
    })

    st.session_state.next_ready = True
    st.rerun()

# 4. フィードバックの表示
if st.session_state.feedback:
  st.markdown("---")
  st.markdown("### 🔍 AIチューターからのフィードバック・分析")
  st.write(st.session_state.feedback)

# 5. 次の問題へ進むボタン（適応型学習：履歴を考慮して次の問題を生成）
if st.session_state.next_ready:
  st.markdown("---")
  if st.button("次の類題に進む（AIが難易度・項目を自動調整） ➡️"):
    with st.spinner(
        "生徒の解答履歴を分析し、最適な次の問題を作成中..."
    ):
      # 過去の履歴を要約してプロンプトに反映（適応型学習の核心）
      history_summary = ""
      if st.session_state.history:
        history_summary = "これまでの生徒の解答履歴：\n"
        for h in st.session_state.history:
          is_corr = h.get("is_correct", False)
          status = "正解" if is_corr else "不正解"
          g_point = h.get("grammar_point", "一般動名詞")
          u_ans = h.get("user_answer", "")
          history_summary += (
              f"- 項目: {g_point}, 判定: {status} (生徒の回答: {u_ans})\n"
          )

      gen_prompt = f"""
      あなたは中2英語の優秀な教材開発AIです。動名詞(gerund)の学習ドリルを作成しています。
      {history_summary}

      上記を踏まえ、生徒のつまずき傾向（間違えた文法パターンなど）を考慮し、次に解くべき類題を1問作成してください。
      必ず以下の【JSON形式】のみで出力してください（マークダウンの ```json やバッククォートは一切使わず、純粋なJSON文字列のみを出力してください）。

      {{
        "question": "次の日本語を英語に訳しなさい。「〇〇」 (...) の形式で記述",
        "answer": "模範解答の英文",
        "grammar_point": "例: like + gerund, enjoy + gerund, finish + gerund, stop + gerund, 動名詞と不定詞の区別 など",
        "difficulty": "basic または intermediate"
      }}
      """

      res = model.generate_content(gen_prompt)
      res_text = res.text.strip()

      # マークダウンのコードブロックが含まれていた場合の保険処理
      if res_text.startswith("```json"):
        res_text = res_text[7:]
      if res_text.startswith("```"):
        res_text = res_text[3:]
      if res_text.endswith("```"):
        res_text = res_text[:-3]
      res_text = res_text.strip()

      try:
        data = json.loads(res_text)
        st.session_state.current_question = data.get(
            "question",
            "次の日本語を英語に訳しなさい。「私は映画を見ることを楽しんでいます。」",
        )
        st.session_state.correct_answer = data.get(
            "answer", "I enjoy watching movies."
        )
        st.session_state.current_grammar_point = data.get(
            "grammar_point", "enjoy + gerund"
        )
      except Exception:
        # JSONパースエラー時のフォールバック
        st.session_state.current_question = (
            "次の日本語を英語に訳しなさい。「私は宿題を終えました。」"
            "（finishを使用）"
        )
        st.session_state.correct_answer = "I finished doing my homework."
        st.session_state.current_grammar_point = "finish + gerund"

      # 状態をリセット
      st.session_state.feedback = ""
      st.session_state.next_ready = False
      st.rerun()

# 6. 学習ダッシュボード（ポートフォリオとしての価値を高める機能）
if st.session_state.history:
  st.markdown("---")
  with st.expander("📊 あなたの学習ダッシュボード（履歴・弱点分析）"):
    total_q = len(st.session_state.history)
    correct_count = sum(
        1 for h in st.session_state.history if h.get("is_correct", False)
    )
    accuracy = (correct_count / total_q) * 100 if total_q > 0 else 0

    col1, col2 = st.columns(2)
    with col1:
      st.metric(label="総解答数", value=f"{total_q} 問")
    with col2:
      st.metric(label="正答率", value=f"{accuracy:.1f}%")

    st.markdown("#### 📝 過去の解答履歴と文法タグ")
    for i, h in enumerate(reversed(st.session_state.history), 1):
      is_corr = h.get("is_correct", False)
      status_icon = "🟢 正解" if is_corr else "🔴 要復習"
      g_point = h.get("grammar_point", "一般動名詞")
      st.markdown(
          f"**第 {total_q - i + 1} 問** | 項目: `{g_point}` - {status_icon}"
      )
      st.text(f"問題: {h.get('question', '')}")
      st.text(f"あなたの回答: {h.get('user_answer', '')}")
      st.text(f"模範解答: {h.get('correct_answer', '')}")
      st.markdown("---")
