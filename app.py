import json
import os
import re
from datetime import datetime

import streamlit as st
from google import genai
from google.genai import types


# =========================================================
# アプリ基本設定
# =========================================================

st.set_page_config(
    page_title="中2英語 個別学習支援ドリル",
    page_icon="📚",
    layout="centered",
)


APP_VERSION = "1.0.1"
STATE_VERSION = 2
MODEL_NAME = "gemini-3.8-flash"


# =========================================================
# 教育設計
# =========================================================
#
# 「何を学ばせるのか」をAIに決めさせない。
# 学習目標はアプリ側で明示的に定義する。
#

LEARNING_OBJECTIVES = {
    "gerund_basic": {
        "name": "動名詞の基本",
        "description": "動詞に -ing を付け、動名詞として使える。",
        "target": "動名詞の基本形",
    },
    "like_gerund": {
        "name": "like + 動名詞",
        "description": (
            "like の後ろに動名詞を使って「～することが好き」と表現できる。"
        ),
        "target": "like + 動名詞",
    },
    "enjoy_gerund": {
        "name": "enjoy + 動名詞",
        "description": (
            "enjoy の後ろに動名詞を使って「～することを楽しむ」と表現できる。"
        ),
        "target": "enjoy + 動名詞",
    },
    "finish_gerund": {
        "name": "finish + 動名詞",
        "description": (
            "finish の後ろに動名詞を使って「～し終える」と表現できる。"
        ),
        "target": "finish + 動名詞",
    },
    "gerund_vs_infinitive": {
        "name": "動名詞と不定詞の区別",
        "description": (
            "今回の学習目標で指定された動名詞と不定詞を区別できる。"
        ),
        "target": "動名詞・不定詞の使い分け",
    },
}


# =========================================================
# 問題バンク
# =========================================================
#
# 第1段階ではAIに問題を作らせない。
# 問題・正解・学習目標・難易度を開発者側で管理する。
#

QUESTION_BANK = [
    {
        "id": "like_001",
        "objective": "like_gerund",
        "difficulty": 1,
        "question": (
            "次の日本語を英語に訳しなさい。\n"
            "「私はテニスをすることが好きです。」"
        ),
        "model_answer": "I like playing tennis.",
        "accepted_answers": [
            "I like playing tennis.",
        ],
        "require_target_pattern": True,
        "explanation": (
            "like の後ろでは、今回の学習目標として "
            "動名詞 playing を使います。"
        ),
    },
    {
        "id": "like_002",
        "objective": "like_gerund",
        "difficulty": 1,
        "question": (
            "次の日本語を英語に訳しなさい。\n"
            "「私は音楽を聴くことが好きです。」"
        ),
        "model_answer": "I like listening to music.",
        "accepted_answers": [
            "I like listening to music.",
        ],
        "require_target_pattern": True,
        "explanation": (
            "like の後ろに listening を使います。"
        ),
    },
    {
        "id": "like_003",
        "objective": "like_gerund",
        "difficulty": 2,
        "question": (
            "次の日本語を英語に訳しなさい。\n"
            "「彼女は本を読むことが好きです。」"
        ),
        "model_answer": "She likes reading books.",
        "accepted_answers": [
            "She likes reading books.",
        ],
        "require_target_pattern": True,
        "explanation": (
            "主語が she なので like は likes になります。"
            "その後ろに reading を使います。"
        ),
    },
    {
        "id": "enjoy_001",
        "objective": "enjoy_gerund",
        "difficulty": 1,
        "question": (
            "次の日本語を英語に訳しなさい。\n"
            "「私は英語を勉強することを楽しんでいます。」"
        ),
        "model_answer": "I enjoy studying English.",
        "accepted_answers": [
            "I enjoy studying English.",
        ],
        "require_target_pattern": True,
        "explanation": (
            "enjoy の後ろには studying のような動名詞を使います。"
        ),
    },
    {
        "id": "enjoy_002",
        "objective": "enjoy_gerund",
        "difficulty": 1,
        "question": (
            "次の日本語を英語に訳しなさい。\n"
            "「私は料理をすることを楽しんでいます。」"
        ),
        "model_answer": "I enjoy cooking.",
        "accepted_answers": [
            "I enjoy cooking.",
        ],
        "require_target_pattern": True,
        "explanation": (
            "enjoy の後ろに cooking を使います。"
        ),
    },
    {
        "id": "enjoy_003",
        "objective": "enjoy_gerund",
        "difficulty": 2,
        "question": (
            "次の日本語を英語に訳しなさい。\n"
            "「彼はサッカーをすることを楽しんでいます。」"
        ),
        "model_answer": "He enjoys playing soccer.",
        "accepted_answers": [
            "He enjoys playing soccer.",
        ],
        "require_target_pattern": True,
        "explanation": (
            "主語が he なので enjoys になります。"
            "その後ろに playing を使います。"
        ),
    },
    {
        "id": "finish_001",
        "objective": "finish_gerund",
        "difficulty": 1,
        "question": (
            "次の日本語を英語に訳しなさい。\n"
            "「私は宿題を終えました。」"
        ),
        "model_answer": "I finished doing my homework.",
        "accepted_answers": [
            "I finished doing my homework.",
        ],
        "require_target_pattern": True,
        "explanation": (
            "finish の後ろに doing のような動名詞を使います。"
        ),
    },
    {
        "id": "finish_002",
        "objective": "finish_gerund",
        "difficulty": 1,
        "question": (
            "次の日本語を英語に訳しなさい。\n"
            "「彼女は昼食を食べ終えました。」"
        ),
        "model_answer": "She finished eating lunch.",
        "accepted_answers": [
            "She finished eating lunch.",
        ],
        "require_target_pattern": True,
        "explanation": (
            "finish の後ろに eating を使います。"
        ),
    },
    {
        "id": "basic_001",
        "objective": "gerund_basic",
        "difficulty": 1,
        "question": (
            "次の日本語を英語に訳しなさい。\n"
            "「泳ぐことは楽しいです。」"
        ),
        "model_answer": "Swimming is fun.",
        "accepted_answers": [
            "Swimming is fun.",
        ],
        "require_target_pattern": True,
        "explanation": (
            "Swimming が文の主語として使われています。"
        ),
    },
    {
        "id": "basic_002",
        "objective": "gerund_basic",
        "difficulty": 1,
        "question": (
            "次の日本語を英語に訳しなさい。\n"
            "「本を読むことは大切です。」"
        ),
        "model_answer": "Reading books is important.",
        "accepted_answers": [
            "Reading books is important.",
        ],
        "require_target_pattern": True,
        "explanation": (
            "Reading books が文の主語として使われています。"
        ),
    },
    {
        "id": "compare_001",
        "objective": "gerund_vs_infinitive",
        "difficulty": 2,
        "question": (
            "次の日本語を英語に訳しなさい。\n"
            "「私はテニスをすることが好きです。」\n\n"
            "今回の問題では、動名詞を使いなさい。"
        ),
        "model_answer": "I like playing tennis.",
        "accepted_answers": [
            "I like playing tennis.",
        ],
        "require_target_pattern": True,
        "explanation": (
            "今回の学習目標では like の後ろに "
            "動名詞 playing を使います。"
        ),
    },
]


# =========================================================
# AI採点用JSONスキーマ
# =========================================================

FEEDBACK_SCHEMA = {
    "type": "object",
    "properties": {
        "is_grammatically_correct": {
            "type": "boolean",
            "description": "生徒の英文が文法的に正しいか",
        },
        "meaning_matches": {
            "type": "boolean",
            "description": "日本語の意味を正しく表しているか",
        },
        "target_grammar_used": {
            "type": "boolean",
            "description": "今回指定された学習目標の文法を使用しているか",
        },
        "mistake_type": {
            "type": "string",
            "enum": [
                "none",
                "target_grammar",
                "verb_form",
                "subject_verb_agreement",
                "word_order",
                "missing_word",
                "unnecessary_word",
                "spelling",
                "meaning",
                "other",
            ],
        },
        "feedback": {
            "type": "string",
            "description": "中学2年生に分かりやすい短いフィードバック",
        },
    },
    "required": [
        "is_grammatically_correct",
        "meaning_matches",
        "target_grammar_used",
        "mistake_type",
        "feedback",
    ],
}


# =========================================================
# Gemini APIキー
# =========================================================


def get_api_key():
    """Streamlit Secrets または環境変数からAPIキーを取得する。"""

    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"]

    return os.environ.get("GEMINI_API_KEY")


api_key = get_api_key()


if not api_key:
    st.error(
        "Gemini APIキーが設定されていません。\n\n"
        "Streamlit Secrets または環境変数 GEMINI_API_KEY "
        "を設定してください。"
    )
    st.stop()


# =========================================================
# Geminiクライアント
# =========================================================


@st.cache_resource
def get_client(api_key_value):
    return genai.Client(api_key=api_key_value)


client = get_client(api_key)


# =========================================================
# セッション状態
# =========================================================


def initialize_state():
    """
    アプリ起動時のセッション状態を初期化する。

    旧バージョンとの互換性を考慮し、
    STATE_VERSION が変わった場合には
    互換性のない一時状態を初期化する。
    """

    current_state_version = st.session_state.get(
        "state_version"
    )

    if current_state_version != STATE_VERSION:

        # 問題・表示状態は安全側に初期化
        st.session_state.current_question_id = "like_001"
        st.session_state.feedback = None
        st.session_state.last_result = None
        st.session_state.next_ready = False

        # 学習履歴は旧形式との互換性が保証できないため、
        # 状態バージョン変更時には初期化する。
        #
        # 今後はJSON保存・復元を利用して学習履歴を保持できる。
        st.session_state.history = []

        st.session_state.state_version = STATE_VERSION

    else:

        if "current_question_id" not in st.session_state:
            st.session_state.current_question_id = "like_001"

        if "history" not in st.session_state:
            st.session_state.history = []

        if "feedback" not in st.session_state:
            st.session_state.feedback = None

        if "last_result" not in st.session_state:
            st.session_state.last_result = None

        if "next_ready" not in st.session_state:
            st.session_state.next_ready = False

    if "student_name" not in st.session_state:
        st.session_state.student_name = ""


initialize_state()


# =========================================================
# 問題取得
# =========================================================


def get_question(question_id):
    """問題IDから問題を取得する。"""

    for question in QUESTION_BANK:

        if question["id"] == question_id:
            return question

    return QUESTION_BANK[0]


def get_current_question():
    return get_question(
        st.session_state.current_question_id
    )


# =========================================================
# 回答の正規化
# =========================================================


def normalize_answer(text):
    """
    英作文比較用の最低限の正規化。

    ・前後空白を削除
    ・連続空白を1つにする
    ・大文字小文字を統一
    ・アポストロフィ表記を統一

    文法そのものを変更するような
    過度な正規化は行わない。
    """

    text = text.strip().lower()

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    text = text.replace(
        "’",
        "'",
    )

    return text


# =========================================================
# コード側による一次判定
# =========================================================


def deterministic_check(
    question,
    user_answer,
):
    """
    コード側で確実に判定できる部分を先に判定する。
    """

    normalized_user = normalize_answer(
        user_answer
    )

    accepted = [
        normalize_answer(answer)
        for answer in question["accepted_answers"]
    ]

    if normalized_user in accepted:

        return {
            "status": "correct",
            "is_correct": True,
            "reason": "registered_answer",
        }

    return {
        "status": "needs_ai_check",
        "is_correct": None,
        "reason": "not_registered_answer",
    }


# =========================================================
# AIによる答案分析
# =========================================================


def analyze_with_ai(
    question,
    user_answer,
):
    """
    登録された正解と一致しなかった答案だけを
    AIに分析させる。

    AIには問題生成・次問題選択をさせない。
    """

    objective = LEARNING_OBJECTIVES[
        question["objective"]
    ]

    prompt = f"""
あなたは中学2年生向け英語教材の答案分析担当です。

あなたの役割は「問題を作ること」ではありません。
与えられた問題と学習目標に対して、
生徒の答案を分析してください。

【学習目標】
{objective["name"]}

【学習目標の説明】
{objective["description"]}

【問題】
{question["question"]}

【登録された模範解答】
{question["model_answer"]}

【今回の学習目標】
{objective["target"]}

【生徒の回答】
{user_answer}

【重要なルール】

1. 生徒の回答が文法的に正しいか確認する。
2. 日本語の意味を正しく表しているか確認する。
3. 今回の問題で指定された学習目標を満たしているか確認する。
4. 模範解答と完全一致しないだけで不正解にしない。
5. ただし、今回の問題が「動名詞を使う」と指定している場合、
   不定詞など別の構文に置き換えた場合は、
   英語として自然でも今回の学習目標を達成したとは判定しない。
6. スペルミスだけで文全体を過度に不正解扱いしない。
7. 生徒が中学2年生であることを考慮する。
8. フィードバックは短く具体的にする。
9. 「何ができているか」と
   「何を直せばよいか」が分かるようにする。
10. 問題そのものを変更しない。
11. 次の問題を提案しない。
12. 学習履歴を推測しない。
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=FEEDBACK_SCHEMA,
            max_output_tokens=1000,
        ),
    )

    if getattr(
        response,
        "parsed",
        None,
    ) is not None:

        parsed = response.parsed

        if isinstance(
            parsed,
            dict,
        ):
            return parsed

        try:
            return dict(parsed)

        except Exception:
            pass

    text = response.text

    if not text:
        raise ValueError(
            "Geminiから回答が返されませんでした。"
        )

    return json.loads(text)


# =========================================================
# 最終判定
# =========================================================


def evaluate_answer(
    question,
    user_answer,
):
    """
    回答を評価する。

    1. コード側で登録正解を確認
    2. 一致しなければAI分析
    3. 教育目標に沿って最終判定
    """

    deterministic_result = deterministic_check(
        question,
        user_answer,
    )

    if deterministic_result["is_correct"] is True:

        return {
            "is_correct": True,
            "judgement": "正解",
            "mistake_type": "none",
            "feedback": question["explanation"],
            "source": "deterministic",
            "ai_used": False,
        }

    ai_result = analyze_with_ai(
        question,
        user_answer,
    )

    grammatically_correct = bool(
        ai_result.get(
            "is_grammatically_correct",
            False,
        )
    )

    meaning_matches = bool(
        ai_result.get(
            "meaning_matches",
            False,
        )
    )

    target_grammar_used = bool(
        ai_result.get(
            "target_grammar_used",
            False,
        )
    )

    mistake_type = ai_result.get(
        "mistake_type",
        "other",
    )

    feedback = ai_result.get(
        "feedback",
        "回答を確認してください。",
    )

    if question["require_target_pattern"]:

        is_correct = (
            grammatically_correct
            and meaning_matches
            and target_grammar_used
        )

    else:

        is_correct = (
            grammatically_correct
            and meaning_matches
        )

    if is_correct:

        judgement = "正解"

    else:

        judgement = "要復習"

    return {
        "is_correct": is_correct,
        "judgement": judgement,
        "mistake_type": mistake_type,
        "feedback": feedback,
        "source": "ai",
        "ai_used": True,
        "ai_grammar_correct": grammatically_correct,
        "ai_meaning_matches": meaning_matches,
        "ai_target_grammar_used": target_grammar_used,
    }


# =========================================================
# 学習履歴レコード
# =========================================================


def create_history_record(
    question,
    user_answer,
    result,
):
    """1問分の学習履歴を作る。"""

    return {
        "timestamp": datetime.now().isoformat(
            timespec="seconds"
        ),
        "question_id": question["id"],
        "objective": question["objective"],
        "objective_name": LEARNING_OBJECTIVES[
            question["objective"]
        ]["name"],
        "difficulty": question["difficulty"],
        "question": question["question"],
        "user_answer": user_answer,
        "model_answer": question["model_answer"],
        "is_correct": result["is_correct"],
        "judgement": result["judgement"],
        "mistake_type": result["mistake_type"],
        "feedback": result["feedback"],
        "ai_used": result.get(
            "ai_used",
            False,
        ),
    }


# =========================================================
# 学習項目別成績
# =========================================================


def calculate_objective_stats():
    """
    学習目標ごとの成績を計算する。

    AIには計算させない。
    """

    stats = {}

    for (
        objective_id,
        objective,
    ) in LEARNING_OBJECTIVES.items():

        stats[objective_id] = {
            "name": objective["name"],
            "total": 0,
            "correct": 0,
            "accuracy": 0.0,
        }

    for record in st.session_state.history:

        objective_id = record.get(
            "objective"
        )

        if objective_id not in stats:
            continue

        stats[objective_id]["total"] += 1

        if record.get(
            "is_correct",
            False,
        ):

            stats[objective_id]["correct"] += 1

    for objective_id in stats:

        total = stats[objective_id]["total"]

        correct = stats[objective_id]["correct"]

        if total > 0:

            stats[objective_id]["accuracy"] = (
                correct
                / total
                * 100
            )

    return stats


# =========================================================
# 連続正解・連続不正解
# =========================================================


def get_recent_results(
    objective_id,
    count=3,
):
    """指定された学習目標の直近結果を取得する。"""

    records = [
        record
        for record in st.session_state.history
        if record.get("objective")
        == objective_id
    ]

    return records[-count:]


def get_streak(
    objective_id,
):
    """
    直近の連続正解・連続不正解を計算する。
    """

    recent = get_recent_results(
        objective_id,
        count=10,
    )

    if not recent:

        return {
            "type": None,
            "count": 0,
        }

    last_value = recent[-1].get(
        "is_correct",
        False,
    )

    count = 0

    for record in reversed(recent):

        if record.get(
            "is_correct",
            False,
        ) == last_value:

            count += 1

        else:

            break

    return {
        "type": (
            "correct"
            if last_value
            else "incorrect"
        ),
        "count": count,
    }


# =========================================================
# 次の問題選択
# =========================================================
#
# AIには次の問題を決めさせない。
#
# 学習履歴
#   ↓
# ルール
#   ↓
# 問題バンク
#

def select_next_question():
    """
    学習履歴に基づいて次の問題を決定する。
    """

    stats = calculate_objective_stats()

    current_id = (
        st.session_state.current_question_id
    )

    attempted_ids = {
        record.get("question_id")
        for record in st.session_state.history
    }

    # -----------------------------------------------------
    # 1. 未学習問題を優先
    # -----------------------------------------------------

    unattempted = [
        question
        for question in QUESTION_BANK
        if question["id"]
        not in attempted_ids
    ]

    if unattempted:

        unattempted.sort(
            key=lambda q: (
                q["difficulty"],
                q["id"],
            )
        )

        return unattempted[0]

    # -----------------------------------------------------
    # 2. 習熟度が最も低い学習目標
    # -----------------------------------------------------

    candidates = []

    for (
        objective_id,
        stat,
    ) in stats.items():

        if stat["total"] == 0:

            score = 0

        else:

            score = stat["accuracy"]

        candidates.append(
            (
                score,
                stat["total"],
                objective_id,
            )
        )

    candidates.sort(
        key=lambda x: (
            x[0],
            x[1],
        )
    )

    target_objective = candidates[0][2]

    # -----------------------------------------------------
    # 3. 対象学習目標の問題
    # -----------------------------------------------------

    objective_questions = [
        question
        for question in QUESTION_BANK
        if question["objective"]
        == target_objective
    ]

    different_questions = [
        question
        for question in objective_questions
        if question["id"] != current_id
    ]

    if different_questions:

        objective_questions = different_questions

    # -----------------------------------------------------
    # 4. 習熟度によって難易度を決定
    # -----------------------------------------------------

    stat = stats[target_objective]

    if stat["total"] == 0:

        target_difficulty = 1

    elif stat["accuracy"] < 60:

        target_difficulty = 1

    elif stat["accuracy"] < 80:

        target_difficulty = 1

    else:

        target_difficulty = 2

    suitable = [
        question
        for question in objective_questions
        if question["difficulty"]
        == target_difficulty
    ]

    if not suitable:

        suitable = objective_questions

    if not suitable:

        return QUESTION_BANK[0]

    # -----------------------------------------------------
    # 5. 過去の出題順を利用して選択
    # -----------------------------------------------------

    history_order = {
        record.get("question_id"): index
        for index, record
        in enumerate(
            st.session_state.history
        )
    }

    suitable.sort(
        key=lambda q: history_order.get(
            q["id"],
            -1,
        )
    )

    return suitable[0]


# =========================================================
# 学習履歴エクスポート
# =========================================================


def create_export_data():
    """学習履歴をJSON形式で出力する。"""

    export_data = {
        "app_version": APP_VERSION,
        "state_version": STATE_VERSION,
        "exported_at": datetime.now().isoformat(
            timespec="seconds"
        ),
        "student_name": (
            st.session_state.student_name
        ),
        "history": st.session_state.history,
    }

    return json.dumps(
        export_data,
        ensure_ascii=False,
        indent=2,
    )


# =========================================================
# 学習履歴インポート
# =========================================================


def import_history(
    uploaded_file,
):
    """
    エクスポートしたJSONを読み込む。
    """

    raw = uploaded_file.read()

    data = json.loads(
        raw.decode("utf-8")
    )

    if "history" not in data:

        raise ValueError(
            "学習履歴データが見つかりません。"
        )

    if not isinstance(
        data["history"],
        list,
    ):

        raise ValueError(
            "学習履歴の形式が正しくありません。"
        )

    st.session_state.history = (
        data["history"]
    )

    if data.get("student_name"):

        st.session_state.student_name = (
            data["student_name"]
        )


# =========================================================
# タイトル
# =========================================================


st.title(
    "📚 中2英語 個別学習支援ドリル"
)

st.caption(
    "第1段階：動名詞の基礎学習"
)

st.info(
    "この試験版では、問題と学習目標は固定しています。"
    "AIは主に自由記述答案の分析とフィードバックに使用します。"
)


# =========================================================
# 生徒情報
# =========================================================


st.markdown(
    "### 👤 学習者"
)

student_name = st.text_input(
    "名前または識別用の名前",
    value=st.session_state.student_name,
)

st.session_state.student_name = student_name


# =========================================================
# 現在の問題
# =========================================================


question = get_current_question()

objective = LEARNING_OBJECTIVES[
    question["objective"]
]


st.markdown("---")

st.markdown(
    "### 🎯 今回の学習目標"
)

st.write(
    f"**{objective['name']}**"
)

st.caption(
    objective["description"]
)


st.markdown(
    "### 📌 問題"
)

st.info(
    question["question"]
)


# =========================================================
# 回答フォーム
# =========================================================


with st.form(
    "answer_form"
):

    user_answer = st.text_input(
        "あなたの解答",
        placeholder="英文を入力してください",
    )

    submit_button = st.form_submit_button(
        "回答する 🚀",
        type="primary",
    )


# =========================================================
# 採点
# =========================================================


if submit_button:

    if not user_answer.strip():

        st.warning(
            "解答を入力してください。"
        )

    else:

        with st.spinner(
            "回答を分析しています..."
        ):

            try:

                result = evaluate_answer(
                    question,
                    user_answer,
                )

                history_record = (
                    create_history_record(
                        question,
                        user_answer,
                        result,
                    )
                )

                st.session_state.history.append(
                    history_record
                )

                st.session_state.last_result = (
                    result
                )

                st.session_state.feedback = (
                    result
                )

                st.session_state.next_ready = (
                    True
                )

                st.rerun()

            except Exception as e:

                st.error(
                    "答案の分析中にエラーが発生しました。"
                )

                with st.expander(
                    "🔧 エラー詳細"
                ):

                    st.code(
                        str(e),
                        language="text",
                    )


# =========================================================
# フィードバック表示
# =========================================================
#
# 旧バージョンの文字列が残っていても、
# dictでなければここには入らない。
#

feedback_data = st.session_state.get(
    "feedback"
)


if (
    isinstance(
        feedback_data,
        dict,
    )
    and "is_correct" in feedback_data
):

    result = feedback_data

    st.markdown("---")

    if result.get(
        "is_correct",
        False,
    ):

        st.success(
            "🟢 正解です。"
        )

    else:

        st.error(
            "🔴 今回の学習目標では要復習です。"
        )

    st.markdown(
        "### 🔍 フィードバック"
    )

    st.write(
        result.get(
            "feedback",
            "フィードバックがありません。",
        )
    )

    if not result.get(
        "is_correct",
        False,
    ):

        st.markdown(
            "### 📖 模範解答"
        )

        st.code(
            question["model_answer"]
        )

        st.caption(
            question["explanation"]
        )

    if result.get(
        "ai_used",
        False,
    ):

        st.caption(
            "この回答はAIによる答案分析を使用しています。"
        )

    else:

        st.caption(
            "登録された正解との一致によって判定しました。"
        )


# =========================================================
# 次の問題
# =========================================================


if st.session_state.get(
    "next_ready",
    False,
):

    st.markdown("---")

    if st.button(
        "次の問題へ ➡️",
        type="primary",
    ):

        next_question = (
            select_next_question()
        )

        st.session_state.current_question_id = (
            next_question["id"]
        )

        st.session_state.feedback = None

        st.session_state.last_result = None

        st.session_state.next_ready = False

        st.rerun()


# =========================================================
# 学習状況
# =========================================================


if st.session_state.history:

    st.markdown("---")

    st.markdown(
        "## 📊 学習状況"
    )

    stats = calculate_objective_stats()

    total_questions = len(
        st.session_state.history
    )

    total_correct = sum(
        1
        for record
        in st.session_state.history
        if record.get(
            "is_correct",
            False,
        )
    )

    overall_accuracy = (
        total_correct
        / total_questions
        * 100
        if total_questions > 0
        else 0
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "解答数",
            f"{total_questions}問",
        )

    with col2:

        st.metric(
            "正解数",
            f"{total_correct}問",
        )

    with col3:

        st.metric(
            "全体正答率",
            f"{overall_accuracy:.1f}%",
        )


    # -----------------------------------------------------
    # 学習目標別
    # -----------------------------------------------------

    st.markdown(
        "### 🎯 学習目標別の習熟状況"
    )

    for (
        objective_id,
        stat,
    ) in stats.items():

        if stat["total"] == 0:

            st.write(
                f"**{stat['name']}**：未学習"
            )

            continue

        st.write(
            f"**{stat['name']}**："
            f"{stat['correct']}/"
            f"{stat['total']}問"
            f"（{stat['accuracy']:.1f}%）"
        )

        st.progress(
            min(
                int(stat["accuracy"]),
                100,
            )
        )


    # -----------------------------------------------------
    # 誤答タイプ
    # -----------------------------------------------------

    mistake_stats = {}

    for record in st.session_state.history:

        if record.get(
            "is_correct",
            False,
        ):

            continue

        mistake = record.get(
            "mistake_type",
            "other",
        )

        mistake_stats[mistake] = (
            mistake_stats.get(
                mistake,
                0,
            )
            + 1
        )

    if mistake_stats:

        st.markdown(
            "### 🔎 誤答傾向"
        )

        sorted_mistakes = sorted(
            mistake_stats.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        for (
            mistake,
            count,
        ) in sorted_mistakes:

            st.write(
                f"- `{mistake}`：{count}問"
            )


    # -----------------------------------------------------
    # 詳細履歴
    # -----------------------------------------------------

    with st.expander(
        "📝 詳細な学習履歴"
    ):

        for (
            index,
            record,
        ) in enumerate(
            reversed(
                st.session_state.history
            ),
            1,
        ):

            question_number = (
                len(
                    st.session_state.history
                )
                - index
                + 1
            )

            status = (
                "🟢 正解"
                if record.get(
                    "is_correct",
                    False,
                )
                else "🔴 要復習"
            )

            st.markdown(
                f"**第{question_number}問** "
                f"{status}"
            )

            st.caption(
                f"学習項目："
                f"{record.get('objective_name', '')}"
            )

            st.text(
                f"問題：\n"
                f"{record.get('question', '')}"
            )

            st.text(
                f"あなたの回答：\n"
                f"{record.get('user_answer', '')}"
            )

            st.text(
                f"模範解答：\n"
                f"{record.get('model_answer', '')}"
            )

            st.caption(
                f"誤答タイプ："
                f"{record.get('mistake_type', 'other')}"
            )

            st.caption(
                f"フィードバック："
                f"{record.get('feedback', '')}"
            )

            st.markdown("---")


# =========================================================
# 学習データ
# =========================================================


st.markdown("---")

st.markdown(
    "## 💾 学習データ"
)

st.caption(
    "現在の試験版では、学習履歴をJSONファイルとして保存・復元できます。"
)


# =========================================================
# エクスポート
# =========================================================


if st.session_state.history:

    export_data = create_export_data()

    st.download_button(
        label="📥 学習履歴を保存",
        data=export_data,
        file_name="english_learning_history.json",
        mime="application/json",
    )


# =========================================================
# インポート
# =========================================================


uploaded_file = st.file_uploader(
    "保存した学習履歴を復元",
    type=["json"],
)


if uploaded_file is not None:

    if st.button(
        "📤 学習履歴を復元する"
    ):

        try:

            import_history(
                uploaded_file
            )

            st.success(
                "学習履歴を復元しました。"
            )

            st.rerun()

        except Exception as e:

            st.error(
                "学習履歴を復元できませんでした。"
            )

            st.code(
                str(e),
                language="text",
            )


# =========================================================
# 開発者向け情報
# =========================================================


with st.expander(
    "🔧 開発者向け情報"
):

    st.write(
        f"アプリバージョン：{APP_VERSION}"
    )

    st.write(
        f"セッション状態バージョン："
        f"{STATE_VERSION}"
    )

    st.write(
        f"使用モデル：{MODEL_NAME}"
    )

    st.write(
        f"問題数：{len(QUESTION_BANK)}"
    )

    st.write(
        f"学習目標数："
        f"{len(LEARNING_OBJECTIVES)}"
    )

    st.write(
        "問題生成：固定問題バンク"
    )

    st.write(
        "次問題選択：ルールベース"
    )

    st.write(
        "答案分析：Gemini"
    )

    st.write(
        "学習履歴："
        "Streamlitセッション＋JSONエクスポート"
    )
