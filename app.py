import json
from datetime import datetime

import streamlit as st


# =========================================================
# アプリ基本設定
# =========================================================

st.set_page_config(
    page_title="中2英語 個別学習支援ドリル",
    page_icon="📚",
    layout="centered",
)

APP_VERSION = "1.3.0"
STATE_VERSION = 5

QUESTIONS_PER_BATCH = 5


# =========================================================
# 教育設計
# =========================================================
#
# 第1段階：
#
# ・空欄補充
# ・4択
# ・ア／イ／ウ／エで回答
# ・5問を1セットとして提示
# ・5問終了後に一括採点
# ・Pythonによる正誤判定
# ・AIはまだ使用しない
#
# =========================================================


LEARNING_OBJECTIVES = {
    "gerund_basic": {
        "name": "動名詞の基本",
        "description": (
            "動詞に -ing を付けて、動名詞として使える。"
        ),
    },
    "like_gerund": {
        "name": "like + 動名詞",
        "description": (
            "like の後ろに動名詞を使って、"
            "「～することが好き」と表現できる。"
        ),
    },
    "enjoy_gerund": {
        "name": "enjoy + 動名詞",
        "description": (
            "enjoy の後ろに動名詞を使って、"
            "「～することを楽しむ」と表現できる。"
        ),
    },
    "finish_gerund": {
        "name": "finish + 動名詞",
        "description": (
            "finish の後ろに動名詞を使って、"
            "「～し終える」と表現できる。"
        ),
    },
}


# =========================================================
# 選択肢記号
# =========================================================

CHOICE_LABELS = [
    "ア",
    "イ",
    "ウ",
    "エ",
]


# =========================================================
# 問題バンク
# =========================================================
#
# 現段階では10問。
#
# 1セット5問。
#
# 最初の5問を解いた後、
# 次の5問に進む。
#
# =========================================================


QUESTION_BANK = [

    # =====================================================
    # 第1セット
    # =====================================================

    {
        "id": "basic_001",
        "question_type": "fill_blank_choice",
        "objective": "gerund_basic",
        "difficulty": 1,
        "question": (
            "次の英文の空欄に入る最も適切な語を選びなさい。\n\n"
            "（　　　）is fun."
        ),
        "japanese": "「泳ぐことは楽しいです。」",
        "options": [
            {
                "label": "ア",
                "value": "Swim",
                "error_type": "base_form",
            },
            {
                "label": "イ",
                "value": "Swimming",
                "error_type": "none",
            },
            {
                "label": "ウ",
                "value": "Swims",
                "error_type": "third_person",
            },
            {
                "label": "エ",
                "value": "Swam",
                "error_type": "past_form",
            },
        ],
        "answer": "イ",
        "explanation": (
            "「泳ぐこと」を表す動名詞は "
            "swim に -ing を付けた Swimming です。"
        ),
    },

    {
        "id": "like_001",
        "question_type": "fill_blank_choice",
        "objective": "like_gerund",
        "difficulty": 1,
        "question": (
            "次の英文の空欄に入る最も適切な語を選びなさい。\n\n"
            "I like（　　　）tennis."
        ),
        "japanese": "「私はテニスをすることが好きです。」",
        "options": [
            {
                "label": "ア",
                "value": "playing",
                "error_type": "none",
            },
            {
                "label": "イ",
                "value": "play",
                "error_type": "base_form",
            },
            {
                "label": "ウ",
                "value": "played",
                "error_type": "past_form",
            },
            {
                "label": "エ",
                "value": "plays",
                "error_type": "third_person",
            },
        ],
        "answer": "ア",
        "explanation": (
            "今回の学習目標では、like の後ろに "
            "動名詞 playing を使います。"
        ),
    },

    {
        "id": "like_002",
        "question_type": "fill_blank_choice",
        "objective": "like_gerund",
        "difficulty": 1,
        "question": (
            "次の英文の空欄に入る最も適切な語を選びなさい。\n\n"
            "I like（　　　）to music."
        ),
        "japanese": "「私は音楽を聴くことが好きです。」",
        "options": [
            {
                "label": "ア",
                "value": "listen",
                "error_type": "base_form",
            },
            {
                "label": "イ",
                "value": "listening",
                "error_type": "none",
            },
            {
                "label": "ウ",
                "value": "listened",
                "error_type": "past_form",
            },
            {
                "label": "エ",
                "value": "listens",
                "error_type": "third_person",
            },
        ],
        "answer": "イ",
        "explanation": (
            "like の後ろに動名詞を使うので、"
            "listen → listening となります。"
        ),
    },

    {
        "id": "enjoy_001",
        "question_type": "fill_blank_choice",
        "objective": "enjoy_gerund",
        "difficulty": 1,
        "question": (
            "次の英文の空欄に入る最も適切な語を選びなさい。\n\n"
            "I enjoy（　　　）English."
        ),
        "japanese": "「私は英語を勉強することを楽しんでいます。」",
        "options": [
            {
                "label": "ア",
                "value": "study",
                "error_type": "base_form",
            },
            {
                "label": "イ",
                "value": "studying",
                "error_type": "none",
            },
            {
                "label": "ウ",
                "value": "studied",
                "error_type": "past_form",
            },
            {
                "label": "エ",
                "value": "studies",
                "error_type": "third_person",
            },
        ],
        "answer": "イ",
        "explanation": (
            "enjoy の後ろに動名詞 studying を使います。"
        ),
    },

    {
        "id": "finish_001",
        "question_type": "fill_blank_choice",
        "objective": "finish_gerund",
        "difficulty": 1,
        "question": (
            "次の英文の空欄に入る最も適切な語を選びなさい。\n\n"
            "I finished（　　　）my homework."
        ),
        "japanese": "「私は宿題を終えました。」",
        "options": [
            {
                "label": "ア",
                "value": "do",
                "error_type": "base_form",
            },
            {
                "label": "イ",
                "value": "doing",
                "error_type": "none",
            },
            {
                "label": "ウ",
                "value": "did",
                "error_type": "past_form",
            },
            {
                "label": "エ",
                "value": "does",
                "error_type": "third_person",
            },
        ],
        "answer": "イ",
        "explanation": (
            "finish の後ろに動名詞 doing を使います。"
        ),
    },


    # =====================================================
    # 第2セット
    # =====================================================

    {
        "id": "basic_002",
        "question_type": "fill_blank_choice",
        "objective": "gerund_basic",
        "difficulty": 1,
        "question": (
            "次の英文の空欄に入る最も適切な語を選びなさい。\n\n"
            "My hobby is（　　　）pictures."
        ),
        "japanese": "「私の趣味は絵を描くことです。」",
        "options": [
            {
                "label": "ア",
                "value": "draw",
                "error_type": "base_form",
            },
            {
                "label": "イ",
                "value": "drew",
                "error_type": "past_form",
            },
            {
                "label": "ウ",
                "value": "drawing",
                "error_type": "none",
            },
            {
                "label": "エ",
                "value": "draws",
                "error_type": "third_person",
            },
        ],
        "answer": "ウ",
        "explanation": (
            "「絵を描くこと」は動名詞 drawing で表します。"
        ),
    },

    {
        "id": "like_003",
        "question_type": "fill_blank_choice",
        "objective": "like_gerund",
        "difficulty": 2,
        "question": (
            "次の英文の空欄に入る最も適切な語を選びなさい。\n\n"
            "She likes（　　　）books."
        ),
        "japanese": "「彼女は本を読むことが好きです。」",
        "options": [
            {
                "label": "ア",
                "value": "read",
                "error_type": "base_form",
            },
            {
                "label": "イ",
                "value": "reads",
                "error_type": "third_person",
            },
            {
                "label": "ウ",
                "value": "reading",
                "error_type": "none",
            },
            {
                "label": "エ",
                "value": "readed",
                "error_type": "other",
            },
        ],
        "answer": "ウ",
        "explanation": (
            "like の後ろに動名詞 reading を使います。"
        ),
    },

    {
        "id": "enjoy_002",
        "question_type": "fill_blank_choice",
        "objective": "enjoy_gerund",
        "difficulty": 1,
        "question": (
            "次の英文の空欄に入る最も適切な語を選びなさい。\n\n"
            "I enjoy（　　　）."
        ),
        "japanese": "「私は料理をすることを楽しんでいます。」",
        "options": [
            {
                "label": "ア",
                "value": "cook",
                "error_type": "base_form",
            },
            {
                "label": "イ",
                "value": "cooked",
                "error_type": "past_form",
            },
            {
                "label": "ウ",
                "value": "cooks",
                "error_type": "third_person",
            },
            {
                "label": "エ",
                "value": "cooking",
                "error_type": "none",
            },
        ],
        "answer": "エ",
        "explanation": (
            "enjoy の後ろに動名詞 cooking を使います。"
        ),
    },

    {
        "id": "finish_002",
        "question_type": "fill_blank_choice",
        "objective": "finish_gerund",
        "difficulty": 1,
        "question": (
            "次の英文の空欄に入る最も適切な語を選びなさい。\n\n"
            "She finished（　　　）lunch."
        ),
        "japanese": "「彼女は昼食を食べ終えました。」",
        "options": [
            {
                "label": "ア",
                "value": "eat",
                "error_type": "base_form",
            },
            {
                "label": "イ",
                "value": "eats",
                "error_type": "third_person",
            },
            {
                "label": "ウ",
                "value": "eating",
                "error_type": "none",
            },
            {
                "label": "エ",
                "value": "ate",
                "error_type": "past_form",
            },
        ],
        "answer": "ウ",
        "explanation": (
            "finish の後ろに動名詞 eating を使います。"
        ),
    },

    {
        "id": "basic_003",
        "question_type": "fill_blank_choice",
        "objective": "gerund_basic",
        "difficulty": 2,
        "question": (
            "次の英文の空欄に入る最も適切な語を選びなさい。\n\n"
            "（　　　）English is important."
        ),
        "japanese": "「英語を勉強することは大切です。」",
        "options": [
            {
                "label": "ア",
                "value": "Study",
                "error_type": "base_form",
            },
            {
                "label": "イ",
                "value": "Studied",
                "error_type": "past_form",
            },
            {
                "label": "ウ",
                "value": "Studies",
                "error_type": "third_person",
            },
            {
                "label": "エ",
                "value": "Studying",
                "error_type": "none",
            },
        ],
        "answer": "エ",
        "explanation": (
            "「英語を勉強すること」を文の主語として使うため、"
            "動名詞 Studying を使います。"
        ),
    },
]


# =========================================================
# 問題取得
# =========================================================


def get_question(
    question_id,
):
    """問題IDから問題を取得する。"""

    for question in QUESTION_BANK:

        if question["id"] == question_id:

            return question

    return QUESTION_BANK[0]


def get_questions_for_batch(
    batch_number,
):
    """
    指定されたセットの5問を取得する。

    batch_number:
        0 → 第1セット
        1 → 第2セット
    """

    start = (
        batch_number
        * QUESTIONS_PER_BATCH
    )

    end = (
        start
        + QUESTIONS_PER_BATCH
    )

    return QUESTION_BANK[
        start:end
    ]


# =========================================================
# 回答の正規化
# =========================================================


def normalize_answer(
    text,
):
    """
    回答比較用の正規化。

    ア・イ・ウ・エの記号について、
    「ア。」
    「ア．」
    なども同じものとして扱う。
    """

    if text is None:

        return ""

    text = str(text).strip()

    text = text.replace(
        "　",
        " ",
    )

    text = text.lower()

    text = text.rstrip(
        "。．.、,）)"
    )

    return text.strip()


# =========================================================
# 選択肢取得
# =========================================================


def get_option_by_label(
    question,
    label,
):
    """記号から選択肢を取得する。"""

    for option in question["options"]:

        if option["label"] == label:

            return option

    return None


# =========================================================
# 1問の回答判定
# =========================================================


def check_answer(
    question,
    user_answer,
):
    """
    4択問題を判定する。

    生徒は、
        ア
        イ
        ウ
        エ

    の記号で回答する。

    選択肢そのものを入力した場合も受け付ける。
    """

    normalized_user = normalize_answer(
        user_answer
    )

    correct_label = normalize_answer(
        question["answer"]
    )

    correct_option = get_option_by_label(
        question,
        question["answer"],
    )

    if correct_option is None:

        raise ValueError(
            "正解の選択肢が問題データにありません。"
        )

    correct_value = normalize_answer(
        correct_option["value"]
    )

    # -----------------------------------------------------
    # 正解記号
    # -----------------------------------------------------

    if normalized_user == correct_label:

        return {
            "is_correct": True,
            "judgement": "正解",
            "mistake_type": "none",
            "feedback": (
                "正解です。"
                "\n\n"
                + question["explanation"]
            ),
        }

    # -----------------------------------------------------
    # 選択肢そのもの
    # -----------------------------------------------------

    if normalized_user == correct_value:

        return {
            "is_correct": True,
            "judgement": "正解",
            "mistake_type": "none",
            "feedback": (
                "正解です。"
                "\n\n"
                + question["explanation"]
            ),
        }

    # -----------------------------------------------------
    # 不正解
    # -----------------------------------------------------

    selected_option = None

    for option in question["options"]:

        if (
            normalize_answer(
                option["label"]
            )
            == normalized_user
        ):

            selected_option = option

            break

    if selected_option:

        mistake_type = selected_option.get(
            "error_type",
            "answer_error",
        )

    else:

        mistake_type = "invalid_answer"

    return {
        "is_correct": False,
        "judgement": "不正解",
        "mistake_type": mistake_type,
        "feedback": (
            "今回は正解ではありません。"
            "\n\n"
            + question["explanation"]
        ),
    }


# =========================================================
# 5問セットの一括採点
# =========================================================


def evaluate_batch(
    questions,
    answers,
):
    """
    5問をまとめて採点する。
    """

    results = []

    for question in questions:

        user_answer = answers.get(
            question["id"],
            "",
        )

        if not user_answer.strip():

            result = {
                "is_correct": False,
                "judgement": "未回答",
                "mistake_type": "unanswered",
                "feedback": (
                    "この問題には回答がありません。"
                ),
            }

        else:

            result = check_answer(
                question,
                user_answer,
            )

        results.append(
            {
                "question": question,
                "user_answer": user_answer,
                "result": result,
            }
        )

    return results


# =========================================================
# 学習履歴レコード
# =========================================================


def create_history_record(
    question,
    user_answer,
    result,
):
    """1問分の学習履歴を作成する。"""

    objective_id = question[
        "objective"
    ]

    objective = LEARNING_OBJECTIVES[
        objective_id
    ]

    correct_option = get_option_by_label(
        question,
        question["answer"],
    )

    return {
        "timestamp": datetime.now().isoformat(
            timespec="seconds"
        ),
        "batch_number": (
            st.session_state.batch_number
        ),
        "question_id": question["id"],
        "question_type": question[
            "question_type"
        ],
        "objective": objective_id,
        "objective_name": objective[
            "name"
        ],
        "difficulty": question[
            "difficulty"
        ],
        "question": question[
            "question"
        ],
        "japanese": question.get(
            "japanese",
            "",
        ),
        "user_answer": user_answer,
        "correct_answer": question[
            "answer"
        ],
        "correct_value": (
            correct_option["value"]
            if correct_option
            else ""
        ),
        "is_correct": result[
            "is_correct"
        ],
        "judgement": result[
            "judgement"
        ],
        "mistake_type": result[
            "mistake_type"
        ],
        "feedback": result[
            "feedback"
        ],
    }


# =========================================================
# 学習状況
# =========================================================


def calculate_overall_stats():
    """全問題の成績を計算する。"""

    total = len(
        st.session_state.history
    )

    correct = sum(
        1
        for record
        in st.session_state.history
        if record.get(
            "is_correct",
            False,
        )
    )

    accuracy = (
        correct
        / total
        * 100
        if total > 0
        else 0
    )

    return {
        "total": total,
        "correct": correct,
        "accuracy": accuracy,
    }


def calculate_objective_stats():
    """
    学習目標ごとの成績を計算する。
    """

    stats = {}

    for (
        objective_id,
        objective,
    ) in LEARNING_OBJECTIVES.items():

        stats[objective_id] = {
            "name": objective[
                "name"
            ],
            "total": 0,
            "correct": 0,
            "accuracy": 0.0,
        }

    for record in (
        st.session_state.history
    ):

        objective_id = record.get(
            "objective"
        )

        if objective_id not in stats:

            continue

        stats[
            objective_id
        ]["total"] += 1

        if record.get(
            "is_correct",
            False,
        ):

            stats[
                objective_id
            ]["correct"] += 1

    for objective_id in stats:

        total = stats[
            objective_id
        ]["total"]

        correct = stats[
            objective_id
        ]["correct"]

        if total > 0:

            stats[
                objective_id
            ]["accuracy"] = (
                correct
                / total
                * 100
            )

    return stats


# =========================================================
# 誤答傾向
# =========================================================


def calculate_mistake_stats():
    """
    誤答タイプを集計する。

    例：

    base_form
    past_form
    third_person
    other
    unanswered

    """

    mistake_stats = {}

    for record in (
        st.session_state.history
    ):

        if record.get(
            "is_correct",
            False,
        ):

            continue

        mistake_type = record.get(
            "mistake_type",
            "other",
        )

        mistake_stats[
            mistake_type
        ] = (
            mistake_stats.get(
                mistake_type,
                0,
            )
            + 1
        )

    return mistake_stats


# =========================================================
# 学習履歴エクスポート
# =========================================================


def create_export_data():

    export_data = {
        "app_version": APP_VERSION,
        "state_version": STATE_VERSION,
        "exported_at": datetime.now().isoformat(
            timespec="seconds"
        ),
        "student_name": (
            st.session_state.student_name
        ),
        "history": (
            st.session_state.history
        ),
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

    if data.get(
        "student_name"
    ):

        st.session_state.student_name = (
            data["student_name"]
        )


# =========================================================
# セッション状態
# =========================================================


def initialize_state():

    current_version = (
        st.session_state.get(
            "state_version"
        )
    )

    # -----------------------------------------------------
    # 新バージョン
    # -----------------------------------------------------

    if current_version != STATE_VERSION:

        st.session_state.state_version = (
            STATE_VERSION
        )

        st.session_state.batch_number = 0

        st.session_state.history = []

        st.session_state.batch_results = None

        st.session_state.batch_submitted = False

        st.session_state.student_answers = {}

    # -----------------------------------------------------
    # 通常起動
    # -----------------------------------------------------

    else:

        if (
            "batch_number"
            not in st.session_state
        ):

            st.session_state.batch_number = 0

        if (
            "history"
            not in st.session_state
        ):

            st.session_state.history = []

        if (
            "batch_results"
            not in st.session_state
        ):

            st.session_state.batch_results = None

        if (
            "batch_submitted"
            not in st.session_state
        ):

            st.session_state.batch_submitted = False

        if (
            "student_answers"
            not in st.session_state
        ):

            st.session_state.student_answers = {}

    if (
        "student_name"
        not in st.session_state
    ):

        st.session_state.student_name = ""


initialize_state()


# =========================================================
# 現在の5問
# =========================================================


current_questions = get_questions_for_batch(
    st.session_state.batch_number
)


# =========================================================
# タイトル
# =========================================================


st.title(
    "📚 中2英語 個別学習支援ドリル"
)

st.caption(
    "第1段階：動名詞・空欄補充4択"
)

st.info(
    "この試験版では、5問をまとめて解答します。"
    "答えは「ア・イ・ウ・エ」の記号で入力してください。"
)


# =========================================================
# 学習者
# =========================================================


st.markdown(
    "### 👤 学習者"
)

student_name = st.text_input(
    "名前または識別用の名前",
    value=(
        st.session_state.student_name
    ),
)

st.session_state.student_name = (
    student_name
)


# =========================================================
# 学習目標
# =========================================================


st.markdown("---")

st.markdown(
    "### 🎯 今回の学習目標"
)

st.write(
    "**動名詞の基本を理解する**"
)

st.caption(
    "今回の5問では、動名詞の形や、"
    "like・enjoy・finish の後ろでの使い方を確認します。"
)


# =========================================================
# 問題セット
# =========================================================


st.markdown(
    "---"
)

st.markdown(
    f"## 📝 第{st.session_state.batch_number + 1}セット"
)

st.caption(
    f"{len(current_questions)}問"
)


# =========================================================
# 回答フォーム
# =========================================================


with st.form(
    f"batch_form_{st.session_state.batch_number}"
):

    answer_inputs = {}

    for index, question in enumerate(
        current_questions,
        start=1,
    ):

        st.markdown(
            f"### 第{index}問"
        )

        st.caption(
            "問題形式：空欄補充・4択"
        )

        st.info(
            question["question"]
        )

        # -------------------------------------------------
        # 選択肢
        # -------------------------------------------------

        for option in question[
            "options"
        ]:

            st.write(
                f"**{option['label']}．** "
                f"{option['value']}"
            )

        # -------------------------------------------------
        # 回答欄
        # -------------------------------------------------
        #
        # 重要：
        # placeholder は設定しない。
        #
        # 回答欄には何も表示しない。
        #

        answer_inputs[
            question["id"]
        ] = st.text_input(
            "あなたの答え",
            key=(
                f"answer_"
                f"{st.session_state.batch_number}_"
                f"{question['id']}"
            ),
        )

        if index < len(
            current_questions
        ):

            st.markdown("---")

    # -----------------------------------------------------
    # 5問まとめて採点
    # -----------------------------------------------------

    submit_batch = (
        st.form_submit_button(
            "5問をまとめて採点する 📝",
            type="primary",
        )
    )


# =========================================================
# 一括採点
# =========================================================


if submit_batch:

    st.session_state.student_answers = (
        answer_inputs
    )

    batch_results = evaluate_batch(
        current_questions,
        answer_inputs,
    )

    st.session_state.batch_results = (
        batch_results
    )

    st.session_state.batch_submitted = (
        True
    )

    # -----------------------------------------------------
    # 学習履歴へ追加
    # -----------------------------------------------------

    for item in batch_results:

        history_record = (
            create_history_record(
                item["question"],
                item["user_answer"],
                item["result"],
            )
        )

        st.session_state.history.append(
            history_record
        )

    st.rerun()


# =========================================================
# 今回の5問の結果
# =========================================================


if (
    st.session_state.batch_submitted
    and st.session_state.batch_results
):

    batch_results = (
        st.session_state.batch_results
    )

    st.markdown("---")

    st.markdown(
        "## 📊 今回の5問の結果"
    )

    batch_total = len(
        batch_results
    )

    batch_correct = sum(
        1
        for item
        in batch_results
        if item["result"].get(
            "is_correct",
            False,
        )
    )

    batch_accuracy = (
        batch_correct
        / batch_total
        * 100
        if batch_total > 0
        else 0
    )

    col1, col2, col3 = (
        st.columns(3)
    )

    with col1:

        st.metric(
            "問題数",
            f"{batch_total}問",
        )

    with col2:

        st.metric(
            "正解",
            f"{batch_correct}問",
        )

    with col3:

        st.metric(
            "正答率",
            f"{batch_accuracy:.1f}%",
        )


    # -----------------------------------------------------
    # 各問題の結果
    # -----------------------------------------------------

    st.markdown(
        "### 🔍 各問題の結果"
    )

    for index, item in enumerate(
        batch_results,
        start=1,
    ):

        question = item[
            "question"
        ]

        result = item[
            "result"
        ]

        user_answer = item[
            "user_answer"
        ]

        if result.get(
            "is_correct",
            False,
        ):

            st.success(
                f"第{index}問　🟢 正解"
            )

        elif result.get(
            "mistake_type"
        ) == "unanswered":

            st.warning(
                f"第{index}問　⚪ 未回答"
            )

        else:

            st.error(
                f"第{index}問　🔴 不正解"
            )

        st.write(
            f"あなたの答え："
            f"「{user_answer}」"
        )

        correct_option = (
            get_option_by_label(
                question,
                question["answer"],
            )
        )

        if correct_option:

            st.write(
                f"正解："
                f"**{correct_option['label']}．"
                f"{correct_option['value']}**"
            )

        st.write(
            result.get(
                "feedback",
                "",
            )
        )

        if index < len(
            batch_results
        ):

            st.markdown("---")


    # =====================================================
    # 今回の5問の誤答分析
    # =====================================================

    st.markdown(
        "### 🔎 今回の5問の誤答傾向"
    )

    batch_mistakes = {}

    for item in batch_results:

        result = item[
            "result"
        ]

        if result.get(
            "is_correct",
            False,
        ):

            continue

        mistake_type = result.get(
            "mistake_type",
            "other",
        )

        batch_mistakes[
            mistake_type
        ] = (
            batch_mistakes.get(
                mistake_type,
                0,
            )
            + 1
        )

    if not batch_mistakes:

        st.success(
            "今回の5問では誤答はありませんでした。"
        )

    else:

        for (
            mistake_type,
            count,
        ) in sorted(
            batch_mistakes.items(),
            key=lambda item: item[1],
            reverse=True,
        ):

            st.write(
                f"- `{mistake_type}`："
                f"{count}問"
            )


    # =====================================================
    # 次の5問
    # =====================================================

    if (
        st.session_state.batch_number
        < (
            len(QUESTION_BANK)
            // QUESTIONS_PER_BATCH
        )
        - 1
    ):

        st.markdown("---")

        if st.button(
            "次の5問へ ➡️",
            type="primary",
        ):

            st.session_state.batch_number += 1

            st.session_state.batch_results = (
                None
            )

            st.session_state.batch_submitted = (
                False
            )

            st.session_state.student_answers = (
                {}
            )

            st.rerun()

    else:

        st.markdown("---")

        st.success(
            "現在用意されている問題はすべて終了しました。"
        )


# =========================================================
# 全体の学習状況
# =========================================================


if st.session_state.history:

    st.markdown("---")

    st.markdown(
        "## 📈 学習状況"
    )

    overall_stats = (
        calculate_overall_stats()
    )

    col1, col2, col3 = (
        st.columns(3)
    )

    with col1:

        st.metric(
            "解答数",
            f"{overall_stats['total']}問",
        )

    with col2:

        st.metric(
            "正解数",
            f"{overall_stats['correct']}問",
        )

    with col3:

        st.metric(
            "全体正答率",
            f"{overall_stats['accuracy']:.1f}%",
        )


    # -----------------------------------------------------
    # 学習目標別
    # -----------------------------------------------------

    st.markdown(
        "### 🎯 学習目標別"
    )

    objective_stats = (
        calculate_objective_stats()
    )

    for (
        objective_id,
        stat,
    ) in objective_stats.items():

        if stat["total"] == 0:

            st.write(
                f"**{stat['name']}：未学習**"
            )

            continue

        st.write(
            f"**{stat['name']}**："
            f"{stat['correct']}/"
            f"{stat['total']}問正解 "
            f"（{stat['accuracy']:.1f}%）"
        )

        st.progress(
            min(
                int(stat["accuracy"]),
                100,
            )
        )


    # -----------------------------------------------------
    # 全体の誤答傾向
    # -----------------------------------------------------

    mistake_stats = (
        calculate_mistake_stats()
    )

    if mistake_stats:

        st.markdown(
            "### 🔎 全体の誤答傾向"
        )

        for (
            mistake_type,
            count,
        ) in sorted(
            mistake_stats.items(),
            key=lambda item: item[1],
            reverse=True,
        ):

            st.write(
                f"- `{mistake_type}`："
                f"{count}問"
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

            if record.get(
                "is_correct",
                False,
            ):

                status = "🟢 正解"

            elif record.get(
                "mistake_type"
            ) == "unanswered":

                status = "⚪ 未回答"

            else:

                status = "🔴 不正解"

            st.markdown(
                f"**第{index}問** "
                f"{status}"
            )

            st.caption(
                f"セット："
                f"{record.get('batch_number', 0) + 1}"
            )

            st.caption(
                f"学習項目："
                f"{record.get('objective_name', '')}"
            )

            st.text(
                f"あなたの回答："
                f"{record.get('user_answer', '')}"
            )

            st.text(
                f"正解："
                f"{record.get('correct_answer', '')}"
                f"（"
                f"{record.get('correct_value', '')}"
                f"）"
            )

            st.caption(
                f"誤答タイプ："
                f"{record.get('mistake_type', '')}"
            )

            st.caption(
                f"解説："
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
    "現在の試験版では、学習履歴をJSONファイルとして"
    "保存・復元できます。"
)


# =========================================================
# 保存
# =========================================================


if st.session_state.history:

    export_data = (
        create_export_data()
    )

    st.download_button(
        label="📥 学習履歴を保存",
        data=export_data,
        file_name=(
            "english_learning_history.json"
        ),
        mime="application/json",
    )


# =========================================================
# 復元
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
        f"アプリバージョン："
        f"{APP_VERSION}"
    )

    st.write(
        f"セッション状態バージョン："
        f"{STATE_VERSION}"
    )

    st.write(
        f"現在のセット："
        f"{st.session_state.batch_number + 1}"
    )

    st.write(
        f"1セットの問題数："
        f"{QUESTIONS_PER_BATCH}問"
    )

    st.write(
        f"登録問題数："
        f"{len(QUESTION_BANK)}問"
    )

    st.write(
        "問題形式：空欄補充・4択"
    )

    st.write(
        "選択肢：ア・イ・ウ・エ"
    )

    st.write(
        "回答方法：記号または選択肢の語句"
    )

    st.write(
        "回答欄：プレースホルダーなし"
    )

    st.write(
        "採点：5問一括"
    )

    st.write(
        "AI問題生成：使用しない"
    )

    st.write(
        "AI採点：使用しない"
    )

    st.write(
        "正誤判定：Python"
    )

    st.write(
        "学習履歴："
        "Streamlitセッション＋JSON"
    )
