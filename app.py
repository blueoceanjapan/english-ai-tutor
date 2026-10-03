import json
import os

import streamlit as st
from google import genai


# =========================================================
# 基本設定
# =========================================================

MODEL_NAME = "gemini-3.8-flash"


# =========================================================
# ページ設定
# =========================================================

st.set_page_config(
    page_title="中2英語 個別学習支援ドリル",
    page_icon="📚",
    layout="centered",
)


# =========================================================
# APIキー設定
# =========================================================

api_key = None

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]

elif os.environ.get("GEMINI_API_KEY"):
    api_key = os.environ.get("GEMINI_API_KEY")


if not api_key:
    st.error(
        "Gemini APIキーが設定されていません。\n\n"
        "Streamlit Secrets に GEMINI_API_KEY を設定してください。"
    )
    st.stop()


# =========================================================
# Gemini Client
# =========================================================

@st.cache_resource
def get_client(api_key):
    return genai.Client(api_key=api_key)


client = get_client(api_key)


# =========================================================
# JSON Schema
# =========================================================

EVALUATION_SCHEMA = {
    "type": "object",
    "properties": {
        "is_correct": {
            "type": "boolean"
        },
        "judgement": {
            "type": "string",
            "enum": [
                "正解！",
                "要修正・不正解"
            ]
        },
        "feedback": {
            "type": "string"
        },
        "mistake_type": {
            "type": "string",
            "enum": [
                "correct",
                "gerund_vs_infinitive",
                "verb_form",
                "word_order",
                "missing_word",
                "unnecessary_word",
                "vocabulary",
                "spelling",
                "grammar_other",
                "meaning",
                "other"
            ]
        },
        "weakness": {
            "type": "string"
        },
        "grammar_point": {
            "type": "string"
        }
    },
    "required": [
        "is_correct",
        "judgement",
        "feedback",
        "mistake_type",
        "weakness",
        "grammar_point"
    ]
}


QUESTION_SCHEMA = {
    "type": "object",
    "properties": {
        "question": {
            "type": "string"
        },
        "answer": {
            "type": "string"
        },
        "grammar_point": {
            "type": "string"
        },
        "difficulty": {
            "type": "string",
            "enum": [
                "basic",
                "intermediate"
            ]
        }
    },
    "required": [
        "question",
        "answer",
        "grammar_point",
        "difficulty"
    ]
}


# =========================================================
# Gemini JSON生成関数
# =========================================================

def generate_json(prompt, schema):
    """
    Geminiから構造化JSONを取得する。
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": schema,
        },
    )

    # response.parsed が利用できる場合はそれを使用
    if getattr(response, "parsed", None) is not None:
        return response.parsed

    # 念のため text からJSONを読む
    if response.text:
        return json.loads(response.text)

    raise ValueError("Geminiから有効なJSONレスポンスを取得できませんでした。")


# =========================================================
# セッション状態の初期化
# =========================================================

if "current_question" not in st.session_state:

    st.session_state.current_question = (
        '次の日本語を英語に訳しなさい。'
        '「私はテニスをすることが好きです。」'
    )


if "correct_answer" not in st.session_state:

    st.session_state.correct_answer = (
        "I like playing tennis."
    )


if "current_grammar_point" not in st.session_state:

    st.session_state.current_grammar_point = (
        "like ＋ 動名詞"
    )


if "current_difficulty" not in st.session_state:

    st.session_state.current_difficulty = (
        "basic"
    )


if "history" not in st.session_state:

    st.session_state.history = []


if "feedback" not in st.session_state:

    st.session_state.feedback = ""


if "next_ready" not in st.session_state:

    st.session_state.next_ready = False


# =========================================================
# タイトル
# =========================================================

st.title("📚 中2英語 個別学習支援ドリル")

st.markdown(
    "### 単元：動名詞 (Gerund) - 適応型AI学習システム"
)

st.caption(
    "生徒の解答履歴を分析し、理解度に応じて次の問題を調整します。"
)

st.markdown("---")


# =========================================================
# 現在の問題
# =========================================================

st.markdown("### 📌 問題")

st.info(
    f"**【問題】**\n\n"
    f"{st.session_state.current_question}"
)


# =========================================================
# 解答フォーム
# =========================================================

with st.form("answer_form"):

    user_answer = st.text_input(
        "あなたの解答を入力してください"
    )

    submit_button = st.form_submit_button(
        "回答する 🚀",
        type="primary"
    )


# =========================================================
# 回答処理
# =========================================================

if submit_button:

    if not user_answer.strip():

        st.warning(
            "解答を入力してください。"
        )

    else:

        with st.spinner(
            "解答を分析しています..."
        ):

            # -------------------------------------------------
            # AI採点プロンプト
            # -------------------------------------------------

            eval_prompt = f"""
あなたは中学2年生向けの英語教師です。

以下の問題について、生徒の英作文を評価してください。

【単元】
中学2年 英語「動名詞」

【問題】
{st.session_state.current_question}

【文法項目】
{st.session_state.current_grammar_point}

【難易度】
{st.session_state.current_difficulty}

【模範解答】
{st.session_state.correct_answer}

【生徒の回答】
{user_answer}

以下の観点から評価してください。

1. 生徒の英文が文法的に正しいか。
2. 日本語の意味を正しく表しているか。
3. 模範解答と異なっていても、別の自然で正しい英文として認められる可能性があるか。
4. 間違っている場合、具体的にどのような間違いなのか。
5. 今回の回答から、生徒のどのようなつまずきが考えられるか。

重要：
- 模範解答との単純な文字列一致だけで正誤を判断しないこと。
- 正しい別表現が可能な場合は、それを正解として扱うこと。
- 中学2年生に対するフィードバックとして、分かりやすく説明すること。
- 「正解」の場合も、なぜ正しいのかを簡潔に説明すること。
- 「不正解」の場合は、生徒を責める表現を使わず、次にどう直せばよいかを説明すること。
- weaknessには、今回の回答から判断できる学習上の特徴を書くこと。
- 判断できない場合は、無理に推測せず「今回の回答だけでは明確に判断できません」とすること。
"""


            # -------------------------------------------------
            # AI採点
            # -------------------------------------------------

            try:

                eval_data = generate_json(
                    eval_prompt,
                    EVALUATION_SCHEMA
                )

            except Exception as e:

                # ---------------------------------------------
                # AI採点に失敗した場合のフォールバック
                # ---------------------------------------------

                normalized_user = (
                    user_answer
                    .strip()
                    .lower()
                    .rstrip(".!?")
                )

                normalized_answer = (
                    st.session_state.correct_answer
                    .strip()
                    .lower()
                    .rstrip(".!?")
                )

                fallback_correct = (
                    normalized_user
                    == normalized_answer
                )

                eval_data = {
                    "is_correct": fallback_correct,
                    "judgement": (
                        "正解！"
                        if fallback_correct
                        else "要修正・不正解"
                    ),
                    "feedback": (
                        "AIによる詳細な分析を取得できなかったため、"
                        "模範解答との基本的な照合結果を表示しています。"
                    ),
                    "mistake_type": (
                        "correct"
                        if fallback_correct
                        else "other"
                    ),
                    "weakness": (
                        "今回の回答だけでは判断できません。"
                    ),
                    "grammar_point": (
                        st.session_state.current_grammar_point
                    ),
                }

                # 開発中のみエラー内容を確認できるようにする
                with st.expander(
                    "⚠️ 開発用：AIエラー詳細"
                ):

                    st.write(
                        str(e)
                    )


            # -------------------------------------------------
            # 結果取得
            # -------------------------------------------------

            is_correct = bool(
                eval_data.get(
                    "is_correct",
                    False
                )
            )

            judgement = eval_data.get(
                "judgement",
                "要修正・不正解"
            )

            feedback_text = eval_data.get(
                "feedback",
                "詳細なフィードバックを取得できませんでした。"
            )

            mistake_type = eval_data.get(
                "mistake_type",
                "other"
            )

            weakness = eval_data.get(
                "weakness",
                "今回の回答からは判断できません。"
            )


            # -------------------------------------------------
            # フィードバック保存
            # -------------------------------------------------

            st.session_state.feedback = (
                f"**{judgement}**\n\n"
                f"{feedback_text}\n\n"
                f"**今回のつまずき分析**\n\n"
                f"{weakness}"
            )


            # -------------------------------------------------
            # 学習履歴保存
            # -------------------------------------------------

            st.session_state.history.append(
                {
                    "question": (
                        st.session_state.current_question
                    ),
                    "user_answer": user_answer,
                    "correct_answer": (
                        st.session_state.correct_answer
                    ),
                    "grammar_point": (
                        st.session_state.current_grammar_point
                    ),
                    "difficulty": (
                        st.session_state.current_difficulty
                    ),
                    "is_correct": is_correct,
                    "mistake_type": mistake_type,
                    "feedback": feedback_text,
                    "weakness": weakness,
                }
            )


            st.session_state.next_ready = True

            st.rerun()


# =========================================================
# フィードバック表示
# =========================================================

if st.session_state.feedback:

    st.markdown("---")

    st.markdown(
        "### 🔍 AIチューターからのフィードバック・分析"
    )

    st.write(
        st.session_state.feedback
    )


# =========================================================
# 次の問題生成
# =========================================================

if st.session_state.next_ready:

    st.markdown("---")

    if st.button(
        "次の類題に進む ➡️",
        type="primary"
    ):

        with st.spinner(
            "これまでの解答履歴を分析し、次の問題を作成しています..."
        ):

            # -------------------------------------------------
            # 履歴の整理
            # -------------------------------------------------

            history_summary = ""

            if st.session_state.history:

                history_summary = (
                    "これまでの生徒の解答履歴：\n"
                )

                for i, h in enumerate(
                    st.session_state.history,
                    1
                ):

                    status = (
                        "正解"
                        if h.get(
                            "is_correct",
                            False
                        )
                        else "不正解"
                    )

                    history_summary += (
                        f"\n第{i}問\n"
                        f"- 文法項目: "
                        f"{h.get('grammar_point', '')}\n"
                        f"- 難易度: "
                        f"{h.get('difficulty', '')}\n"
                        f"- 判定: {status}\n"
                        f"- 誤答タイプ: "
                        f"{h.get('mistake_type', '')}\n"
                        f"- 生徒の回答: "
                        f"{h.get('user_answer', '')}\n"
                        f"- 模範解答: "
                        f"{h.get('correct_answer', '')}\n"
                        f"- つまずき: "
                        f"{h.get('weakness', '')}\n"
                    )


            # -------------------------------------------------
            # 基本統計
            # -------------------------------------------------

            total_q = len(
                st.session_state.history
            )

            correct_q = sum(
                1
                for h in st.session_state.history
                if h.get(
                    "is_correct",
                    False
                )
            )

            accuracy = (
                correct_q / total_q
                if total_q > 0
                else 0
            )


            # -------------------------------------------------
            # 次問題生成プロンプト
            # -------------------------------------------------

            gen_prompt = f"""
あなたは中学2年生向けの優秀な英語教材開発AIです。

単元は「動名詞（gerund）」です。

生徒のこれまでの学習履歴を分析し、
この生徒が次に取り組むのに適した問題を1問作成してください。

{history_summary}

【現在までの状況】

総問題数：
{total_q}

正答数：
{correct_q}

全体正答率：
{accuracy * 100:.1f}%

【問題作成の基本方針】

1. 生徒の弱点が明確な場合は、その弱点を重点的に練習できる問題にする。
2. 同じ問題の単なる言い換えではなく、同じ学習能力を測定できる新しい問題にする。
3. 連続して正解している場合は、必要に応じて少し難易度を上げる。
4. 連続して間違えている場合は、基本レベルに戻す。
5. 中学2年生として自然な日本語と英語を使用する。
6. 問題文に答えを推測できるヒントを入れない。
7. 「～を使わず」「～を使って」など、答えを直接指定する表現は使用しない。
8. 問題そのものに文法項目名を表示しない。
9. 複数の正解が考えられる場合は、できるだけ避ける。
10. 模範解答は自然で中学2年生に適した英文にする。
11. grammar_pointには、その問題で測定したい具体的な文法知識を記録する。
12. difficultyはbasicまたはintermediateのどちらかにする。
13. 直前の問題と同じ問題を再利用しない。
14. 生徒の誤答タイプも考慮する。

特に重要なのは、

「動名詞という単元が同じ」

だけではなく、

「生徒が具体的に何につまずいているのか」

を考慮することです。

例えば、

- like ＋ 動名詞
- enjoy ＋ 動名詞
- finish ＋ 動名詞
- stop ＋ 動名詞
- 動名詞と不定詞の区別
- 動詞のing形
- 語順

などを必要に応じて使い分けてください。
"""


            # -------------------------------------------------
            # AIによる次問題生成
            # -------------------------------------------------

            try:

                question_data = generate_json(
                    gen_prompt,
                    QUESTION_SCHEMA
                )

            except Exception as e:

                # ---------------------------------------------
                # AI生成失敗時のフォールバック
                # ---------------------------------------------

                question_data = {
                    "question": (
                        '次の日本語を英語に訳しなさい。'
                        '「私は英語を勉強することを楽しんでいます。」'
                    ),
                    "answer": (
                        "I enjoy studying English."
                    ),
                    "grammar_point": (
                        "enjoy ＋ 動名詞"
                    ),
                    "difficulty": "basic",
                }

                with st.expander(
                    "⚠️ 開発用：AIエラー詳細"
                ):

                    st.write(
                        str(e)
                    )


            # -------------------------------------------------
            # 新しい問題を保存
            # -------------------------------------------------

            st.session_state.current_question = (
                question_data.get(
                    "question",
                    (
                        '次の日本語を英語に訳しなさい。'
                        '「私は英語を勉強することを楽しんでいます。」'
                    )
                )
            )

            st.session_state.correct_answer = (
                question_data.get(
                    "answer",
                    "I enjoy studying English."
                )
            )

            st.session_state.current_grammar_point = (
                question_data.get(
                    "grammar_point",
                    "enjoy ＋ 動名詞"
                )
            )

            st.session_state.current_difficulty = (
                question_data.get(
                    "difficulty",
                    "basic"
                )
            )


            # -------------------------------------------------
            # 状態リセット
            # -------------------------------------------------

            st.session_state.feedback = ""

            st.session_state.next_ready = False

            st.rerun()


# =========================================================
# 学習ダッシュボード
# =========================================================

if st.session_state.history:

    st.markdown("---")

    with st.expander(
        "📊 学習ダッシュボード（履歴・弱点分析）"
    ):

        # -------------------------------------------------
        # 基本統計
        # -------------------------------------------------

        total_q = len(
            st.session_state.history
        )

        correct_count = sum(
            1
            for h in st.session_state.history
            if h.get(
                "is_correct",
                False
            )
        )

        accuracy = (
            correct_count / total_q * 100
            if total_q > 0
            else 0
        )


        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                label="総解答数",
                value=f"{total_q} 問"
            )

        with col2:

            st.metric(
                label="正答数",
                value=f"{correct_count} 問"
            )

        with col3:

            st.metric(
                label="正答率",
                value=f"{accuracy:.1f}%"
            )


        # -------------------------------------------------
        # 文法項目別集計
        # -------------------------------------------------

        st.markdown(
            "#### 📚 文法項目ごとの学習状況"
        )

        grammar_stats = {}


        for h in st.session_state.history:

            g_point = h.get(
                "grammar_point",
                "一般動名詞"
            )

            if g_point not in grammar_stats:

                grammar_stats[g_point] = {
                    "total": 0,
                    "correct": 0,
                }

            grammar_stats[g_point]["total"] += 1

            if h.get(
                "is_correct",
                False
            ):

                grammar_stats[g_point]["correct"] += 1


        for g_point, stats in grammar_stats.items():

            g_total = stats["total"]

            g_correct = stats["correct"]

            g_accuracy = (
                g_correct / g_total * 100
                if g_total > 0
                else 0
            )

            st.write(
                f"**{g_point}**　"
                f"{g_correct}/{g_total}問正解 "
                f"（{g_accuracy:.1f}%）"
            )


        # -------------------------------------------------
        # 誤答タイプ集計
        # -------------------------------------------------

        mistake_stats = {}


        for h in st.session_state.history:

            if h.get(
                "is_correct",
                False
            ):
                continue

            mistake = h.get(
                "mistake_type",
                "other"
            )

            mistake_stats[mistake] = (
                mistake_stats.get(
                    mistake,
                    0
                ) + 1
            )


        if mistake_stats:

            st.markdown(
                "#### 🔎 主な誤答タイプ"
            )

            for mistake, count in sorted(
                mistake_stats.items(),
                key=lambda x: x[1],
                reverse=True
            ):

                st.write(
                    f"- `{mistake}`：{count}問"
                )


        # -------------------------------------------------
        # 詳細履歴
        # -------------------------------------------------

        st.markdown(
            "#### 📝 過去の解答履歴"
        )


        for i, h in enumerate(
            reversed(
                st.session_state.history
            ),
            1
        ):

            question_number = (
                total_q - i + 1
            )

            is_corr = h.get(
                "is_correct",
                False
            )

            status = (
                "🟢 正解"
                if is_corr
                else "🔴 要復習"
            )

            g_point = h.get(
                "grammar_point",
                "一般動名詞"
            )

            difficulty = h.get(
                "difficulty",
                "basic"
            )

            mistake_type = h.get(
                "mistake_type",
                "other"
            )


            st.markdown(
                f"**第{question_number}問** "
                f"| {status} "
                f"| `{g_point}` "
                f"| 難易度：`{difficulty}`"
            )

            st.text(
                f"問題：{h.get('question', '')}"
            )

            st.text(
                f"あなたの回答："
                f"{h.get('user_answer', '')}"
            )

            st.text(
                f"模範解答："
                f"{h.get('correct_answer', '')}"
            )


            if not is_corr:

                st.caption(
                    f"誤答タイプ：{mistake_type}"
                )

                st.caption(
                    f"つまずき："
                    f"{h.get('weakness', '')}"
                )

            st.markdown("---")
