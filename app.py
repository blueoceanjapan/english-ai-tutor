import json
import os

import streamlit as st
from google import genai
from google.genai import types


# =========================================================
# ページ設定
# =========================================================

st.set_page_config(
    page_title="中2英語 個別学習支援ドリル",
    page_icon="📚",
    layout="centered",
)


# =========================================================
# Gemini APIキー
# =========================================================

api_key = None

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
elif os.environ.get("GEMINI_API_KEY"):
    api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error(
        "Gemini APIキーが設定されていません。"
        "Streamlit Secrets または環境変数 GEMINI_API_KEY を設定してください。"
    )
    st.stop()


# =========================================================
# Geminiクライアント
# =========================================================

MODEL_NAME = "gemini-3.8-flash"


@st.cache_resource
def get_client(api_key):
    return genai.Client(api_key=api_key)


client = get_client(api_key)


# =========================================================
# JSONスキーマ
# =========================================================

EVALUATION_SCHEMA = {
    "type": "object",
    "properties": {
        "is_correct": {
            "type": "boolean",
            "description": "生徒の回答が正しいかどうか"
        },
        "judgement": {
            "type": "string",
            "description": "正解または要修正・不正解"
        },
        "feedback": {
            "type": "string",
            "description": "生徒に分かりやすい具体的なフィードバック"
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
            "type": "string",
            "description": "今回の回答から判断できる生徒のつまずき"
        },
        "grammar_point": {
            "type": "string",
            "description": "今回確認した文法項目"
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
            "type": "string",
            "description": "生徒に提示する問題文"
        },
        "answer": {
            "type": "string",
            "description": "模範解答"
        },
        "grammar_point": {
            "type": "string",
            "description": "問題で測定する文法項目"
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
# GeminiへJSONを要求する共通関数
# =========================================================

def generate_json(prompt, schema):
    """
    GeminiにJSON形式で回答させる。
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema,
            max_output_tokens=2000,
        ),
    )

    # 構造化出力がparsedとして取得できる場合
    if getattr(response, "parsed", None) is not None:

        parsed = response.parsed

        if isinstance(parsed, dict):
            return parsed

        try:
            return dict(parsed)
        except Exception:
            pass

    # 通常のtextとして取得
    text = response.text

    if not text:
        raise ValueError(
            "Geminiから有効な回答が返されませんでした。"
        )

    return json.loads(text)


# =========================================================
# セッション状態
# =========================================================

if "current_question" not in st.session_state:

    st.session_state.current_question = (
        "次の日本語を英語に訳しなさい。"
        "「私はテニスをすることが好きです。」"
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

    st.session_state.current_difficulty = "basic"


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
    "### 単元：動名詞 - 適応型AI学習システム"
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
        type="primary",
    )


# =========================================================
# AI採点・分析
# =========================================================

if submit_button:

    if not user_answer.strip():

        st.warning(
            "解答を入力してください。"
        )

    else:

        with st.spinner(
            "AIが解答を分析しています..."
        ):

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

【評価ルール】

1. 生徒の英文が文法的に正しいか確認してください。
2. 日本語の意味を正しく表しているか確認してください。
3. 模範解答と異なっていても、自然で意味が正しい英文なら正解として認めてください。
4. 単純な文字列一致だけで正誤を判断しないでください。
5. 動名詞と不定詞の使い分けを確認してください。
6. 動詞の形を確認してください。
7. 語順を確認してください。
8. 必要な単語の欠落を確認してください。
9. 不要な単語が入っていないか確認してください。
10. スペルミスを確認してください。
11. 意味が日本語の問題文と一致しているか確認してください。
12. 今回の回答から判断できる学習上のつまずきを説明してください。

正しい英文であれば、過度に厳しく不正解にしないでください。

中学2年生の生徒に対するフィードバックとして、
「何ができているか」
「どこを直せばよいか」
「次に何を意識すればよいか」
が分かるようにしてください。
"""

            try:

                eval_data = generate_json(
                    eval_prompt,
                    EVALUATION_SCHEMA
                )

                ai_error = None

            except Exception as e:

                eval_data = None
                ai_error = str(e)


        # =================================================
        # AI採点成功
        # =================================================

        if eval_data is not None:

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
                "フィードバックを取得できませんでした。"
            )

            mistake_type = eval_data.get(
                "mistake_type",
                "other"
            )

            weakness = eval_data.get(
                "weakness",
                "今回の回答からは判断できません。"
            )

            grammar_point = eval_data.get(
                "grammar_point",
                st.session_state.current_grammar_point
            )


            # ---------------------------------------------
            # フィードバック保存
            # ---------------------------------------------

            st.session_state.feedback = (
                f"**{judgement}**\n\n"
                f"{feedback_text}\n\n"
                f"**今回のつまずき分析**\n\n"
                f"{weakness}"
            )


            # ---------------------------------------------
            # 履歴保存
            # ---------------------------------------------

            st.session_state.history.append(
                {
                    "question":
                        st.session_state.current_question,

                    "user_answer":
                        user_answer,

                    "correct_answer":
                        st.session_state.correct_answer,

                    "grammar_point":
                        grammar_point,

                    "difficulty":
                        st.session_state.current_difficulty,

                    "is_correct":
                        is_correct,

                    "mistake_type":
                        mistake_type,

                    "feedback":
                        feedback_text,

                    "weakness":
                        weakness,
                }
            )


            st.session_state.next_ready = True

            st.rerun()


        # =================================================
        # AI採点失敗
        # =================================================

        else:

            st.error(
                "GeminiによるAI分析に失敗しました。"
            )

            st.warning(
                "今回は自動フォールバックを行わず、"
                "AI接続のエラー内容を確認できるようにしています。"
            )

            if ai_error:

                with st.expander(
                    "🔧 エラー詳細を表示"
                ):

                    st.code(
                        ai_error,
                        language="text"
                    )


# =========================================================
# フィードバック表示
# =========================================================

if st.session_state.feedback:

    st.markdown("---")

    st.markdown(
        "### 🔍 AIチューターからのフィードバック・分析"
    )

    st.markdown(
        st.session_state.feedback
    )


# =========================================================
# 次の問題生成
# =========================================================

if st.session_state.next_ready:

    st.markdown("---")

    if st.button(
        "次の類題に進む ➡️",
        type="primary",
    ):

        with st.spinner(
            "これまでの学習履歴を分析し、次の問題を作成しています..."
        ):

            # ---------------------------------------------
            # 履歴をまとめる
            # ---------------------------------------------

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
                        if h.get("is_correct", False)
                        else "不正解"
                    )

                    history_summary += (
                        f"\n第{i}問\n"
                        f"- 文法項目："
                        f"{h.get('grammar_point', '')}\n"
                        f"- 難易度："
                        f"{h.get('difficulty', '')}\n"
                        f"- 判定：{status}\n"
                        f"- 誤答タイプ："
                        f"{h.get('mistake_type', '')}\n"
                        f"- 生徒の回答："
                        f"{h.get('user_answer', '')}\n"
                        f"- 模範解答："
                        f"{h.get('correct_answer', '')}\n"
                        f"- つまずき："
                        f"{h.get('weakness', '')}\n"
                    )


            # ---------------------------------------------
            # 正答率
            # ---------------------------------------------

            total_q = len(
                st.session_state.history
            )

            correct_q = sum(
                1
                for h in st.session_state.history
                if h.get("is_correct", False)
            )

            accuracy = (
                correct_q / total_q
                if total_q > 0
                else 0
            )


            # ---------------------------------------------
            # 次問題生成プロンプト
            # ---------------------------------------------

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

【問題作成方針】

1. 生徒の弱点が明確な場合は、その弱点を重点的に練習できる問題にする。
2. 同じ問題の単なる言い換えではなく、同じ学習能力を測定できる新しい問題にする。
3. 連続して正解している場合は、必要に応じて少し難易度を上げる。
4. 連続して間違えている場合は、基本レベルに戻す。
5. 中学2年生として自然な日本語と英語を使用する。
6. 問題文に答えを推測できるヒントを入れない。
7. 答えを直接指定する表現は使用しない。
8. 問題文そのものに文法項目名を表示しない。
9. 複数の正解が考えられる問題はできるだけ避ける。
10. 模範解答は自然で中学2年生に適した英文にする。
11. grammar_pointには、その問題で測定したい文法知識を記録する。
12. difficultyはbasicまたはintermediateのどちらかにする。

特に重要なのは、

「動名詞という単元が同じ」

だけではなく、

「生徒が直前まで苦手としている具体的な学習内容」

を考慮することです。
"""


            # ---------------------------------------------
            # AI問題生成
            # ---------------------------------------------

            try:

                data = generate_json(
                    gen_prompt,
                    QUESTION_SCHEMA
                )

                generation_error = None

            except Exception as e:

                data = None
                generation_error = str(e)


            # ---------------------------------------------
            # AI生成成功
            # ---------------------------------------------

            if data is not None:

                st.session_state.current_question = data.get(
                    "question",
                    "次の日本語を英語に訳しなさい。"
                    "「私は英語を勉強することを楽しんでいます。」"
                )

                st.session_state.correct_answer = data.get(
                    "answer",
                    "I enjoy studying English."
                )

                st.session_state.current_grammar_point = data.get(
                    "grammar_point",
                    "enjoy ＋ 動名詞"
                )

                st.session_state.current_difficulty = data.get(
                    "difficulty",
                    "basic"
                )

                st.session_state.feedback = ""

                st.session_state.next_ready = False

                st.rerun()


            # ---------------------------------------------
            # AI生成失敗
            # ---------------------------------------------

            else:

                st.error(
                    "次の問題のAI生成に失敗しました。"
                )

                if generation_error:

                    with st.expander(
                        "🔧 エラー詳細を表示"
                    ):

                        st.code(
                            generation_error,
                            language="text"
                        )


# =========================================================
# 学習ダッシュボード
# =========================================================

if st.session_state.history:

    st.markdown("---")

    with st.expander(
        "📊 学習ダッシュボード（履歴・弱点分析）"
    ):

        total_q = len(
            st.session_state.history
        )

        correct_count = sum(
            1
            for h in st.session_state.history
            if h.get("is_correct", False)
        )

        accuracy = (
            correct_count / total_q * 100
            if total_q > 0
            else 0
        )


        # ---------------------------------------------
        # 基本統計
        # ---------------------------------------------

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


        # ---------------------------------------------
        # 文法項目別
        # ---------------------------------------------

        st.markdown(
            "#### 📚 文法項目ごとの学習状況"
        )

        grammar_stats = {}

        for h in st.session_state.history:

            grammar = h.get(
                "grammar_point",
                "一般動名詞"
            )

            if grammar not in grammar_stats:

                grammar_stats[grammar] = {
                    "total": 0,
                    "correct": 0
                }

            grammar_stats[grammar]["total"] += 1

            if h.get(
                "is_correct",
                False
            ):

                grammar_stats[grammar]["correct"] += 1


        for grammar, stats in grammar_stats.items():

            total = stats["total"]

            correct = stats["correct"]

            rate = (
                correct / total * 100
                if total > 0
                else 0
            )

            st.write(
                f"**{grammar}**　"
                f"{correct}/{total}問正解 "
                f"（{rate:.1f}%）"
            )


        # ---------------------------------------------
        # 誤答タイプ
        # ---------------------------------------------

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


        # ---------------------------------------------
        # 詳細履歴
        # ---------------------------------------------

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

            is_correct = h.get(
                "is_correct",
                False
            )

            status = (
                "🟢 正解"
                if is_correct
                else "🔴 要復習"
            )

            grammar = h.get(
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
                f"| `{grammar}` "
                f"| 難易度：`{difficulty}`"
            )

            st.text(
                f"問題："
                f"{h.get('question', '')}"
            )

            st.text(
                f"あなたの回答："
                f"{h.get('user_answer', '')}"
            )

            st.text(
                f"模範解答："
                f"{h.get('correct_answer', '')}"
            )

            if not is_correct:

                st.caption(
                    f"誤答タイプ："
                    f"{mistake_type}"
                )

                st.caption(
                    f"つまずき："
                    f"{h.get('weakness', '')}"
                )

                st.caption(
                    f"AIフィードバック："
                    f"{h.get('feedback', '')}"
                )

            st.markdown("---")
