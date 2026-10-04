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

APP_VERSION = "1.4.0"
STATE_VERSION = 6

QUESTIONS_PER_BATCH = 5


# =========================================================
# 教育設計
# =========================================================
#
# 現在の第1段階では、
#
# 大問1
# 「次の日本文に合うように、（　）にもっとも適するものを
#  ア～エから1つ選び、記号で答えなさい。」
#
# という学校のテストに近い形式を実装する。
#
# 各小問：
#   ・日本語訳
#   ・英文の空欄
#   ・ア～エの4択
#   ・クリック式回答
#
# 5問を1セットとして出題し、
# 5問まとめて採点する。
#
# AIは現段階では使用しない。
#
# =========================================================


# =========================================================
# 学習目標
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
# 大問の指示文
# =========================================================

MAJOR_QUESTION_INSTRUCTION = (
    "次の日本文に合うように、（　）にもっとも適するものを"
    "ア～エから1つ選び、記号で答えなさい。"
)


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
# 大問1
#
# 現在は10問。
# 1セット5問。
#
# 正解位置は意図的に分散させている。
#
# error_type は内部分析用。
# 生徒画面には表示しない。
#
# =========================================================

QUESTION_BANK = [

    # =====================================================
    # 第1セット
    # =====================================================

    {
        "id": "gerund_001",
        "major_question": 1,
        "question_number": 1,
        "question_type": "japanese_to_english_choice",
        "objective": "gerund_basic",
        "difficulty": 1,

        "japanese": (
            "泳ぐことは楽しいです。"
        ),

        "english": (
            "（　　　）is fun."
        ),

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
            "「泳ぐこと」を表す動名詞は、"
            "swim に -ing を付けた swimming です。"
        ),
    },

    {
        "id": "gerund_002",
        "major_question": 1,
        "question_number": 2,
        "question_type": "japanese_to_english_choice",
        "objective": "like_gerund",
        "difficulty": 1,

        "japanese": (
            "私はテニスをすることが好きです。"
        ),

        "english": (
            "I like（　　　）tennis."
        ),

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
            "今回の学習目標では、like の後ろに"
            "動名詞 playing を使います。"
        ),
    },

    {
        "id": "gerund_003",
        "major_question": 1,
        "question_number": 3,
        "question_type": "japanese_to_english_choice",
        "objective": "like_gerund",
        "difficulty": 1,

        "japanese": (
            "私は音楽を聴くことが好きです。"
        ),

        "english": (
            "I like（　　　）to music."
        ),

        "options": [
            {
                "label": "ア",
                "value": "listen",
                "error_type": "base_form",
            },
            {
                "label": "イ",
                "value": "listened",
                "error_type": "past_form",
            },
            {
                "label": "ウ",
                "value": "listening",
                "error_type": "none",
            },
            {
                "label": "エ",
                "value": "listens",
                "error_type": "third_person",
            },
        ],

        "answer": "ウ",

        "explanation": (
            "like の後ろに動名詞を使うので、"
            "listen → listening となります。"
        ),
    },

    {
        "id": "gerund_004",
        "major_question": 1,
        "question_number": 4,
        "question_type": "japanese_to_english_choice",
        "objective": "enjoy_gerund",
        "difficulty": 1,

        "japanese": (
            "私は英語を勉強することを楽しんでいます。"
        ),

        "english": (
            "I enjoy（　　　）English."
        ),

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
        "id": "gerund_005",
        "major_question": 1,
        "question_number": 5,
        "question_type": "japanese_to_english_choice",
        "objective": "finish_gerund",
        "difficulty": 1,

        "japanese": (
            "私は宿題を終えました。"
        ),

        "english": (
            "I finished（　　　）my homework."
        ),

        "options": [
            {
                "label": "ア",
                "value": "do",
                "error_type": "base_form",
            },
            {
                "label": "イ",
                "value": "did",
                "error_type": "past_form",
            },
            {
                "label": "ウ",
                "value": "does",
                "error_type": "third_person",
            },
            {
                "label": "エ",
                "value": "doing",
                "error_type": "none",
            },
        ],

        "answer": "エ",

        "explanation": (
            "finish の後ろに動名詞 doing を使います。"
        ),
    },


    # =====================================================
    # 第2セット
    # =====================================================

    {
        "id": "gerund_006",
        "major_question": 1,
        "question_number": 6,
        "question_type": "japanese_to_english_choice",
        "objective": "gerund_basic",
        "difficulty": 1,

        "japanese": (
            "私の趣味は絵を描くことです。"
        ),

        "english": (
            "My hobby is（　　　）pictures."
        ),

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
                "value": "draws",
                "error_type": "third_person",
            },
            {
                "label": "エ",
                "value": "drawing",
                "error_type": "none",
            },
        ],

        "answer": "エ",

        "explanation": (
            "「絵を描くこと」は動名詞 drawing で表します。"
        ),
    },

    {
        "id": "gerund_007",
        "major_question": 1,
        "question_number": 7,
        "question_type": "japanese_to_english_choice",
        "objective": "like_gerund",
        "difficulty": 2,

        "japanese": (
            "彼女は本を読むことが好きです。"
        ),

        "english": (
            "She likes（　　　）books."
        ),

        "options": [
            {
                "label": "ア",
                "value": "reading",
                "error_type": "none",
            },
            {
                "label": "イ",
                "value": "read",
                "error_type": "base_form",
            },
            {
                "label": "ウ",
                "value": "reads",
                "error_type": "third_person",
            },
            {
                "label": "エ",
                "value": "readed",
                "error_type": "other",
            },
        ],

        "answer": "ア",

        "explanation": (
            "like の後ろに動名詞 reading を使います。"
        ),
    },

    {
        "id": "gerund_008",
        "major_question": 1,
        "question_number": 8,
        "question_type": "japanese_to_english_choice",
        "objective": "enjoy_gerund",
        "difficulty": 1,

        "japanese": (
            "私は料理をすることを楽しんでいます。"
        ),

        "english": (
            "I enjoy（　　　）."
        ),

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
        "id": "gerund_009",
        "major_question": 1,
        "question_number": 9,
        "question_type": "japanese_to_english_choice",
        "objective": "finish_gerund",
        "difficulty": 1,

        "japanese": (
            "彼女は昼食を食べ終えました。"
        ),

        "english": (
            "She finished（　　　）lunch."
        ),

        "options": [
            {
                "label": "ア",
                "value": "eat",
                "error_type": "base_form",
            },
            {
                "label": "イ",
                "value": "eating",
                "error_type": "none",
            },
            {
                "label": "ウ",
                "value": "eats",
                "error_type": "third_person",
            },
            {
                "label": "エ",
                "value": "ate",
                "error_type": "past_form",
            },
        ],

        "answer": "イ",

        "explanation": (
            "finish の後ろに動名詞 eating を使います。"
        ),
    },

    {
        "id": "gerund_010",
        "major_question": 1,
        "question_number": 10,
        "question_type": "japanese_to_english_choice",
        "objective": "gerund_basic",
        "difficulty": 2,

        "japanese": (
            "英語を勉強することは大切です。"
        ),

        "english": (
            "（　　　）English is important."
        ),

        "options": [
            {
                "label": "ア",
                "value": "Studying",
                "error_type": "none",
            },
            {
                "label": "イ",
                "value": "Study",
                "error_type": "base_form",
            },
            {
                "label": "ウ",
                "value": "Studied",
                "error_type": "past_form",
            },
            {
                "label": "エ",
                "value": "Studies",
                "error_type": "third_person",
            },
        ],

        "answer": "ア",

        "explanation": (
            "「英語を勉強すること」を文の主語として使うため、"
            "動名詞 Studying を使います。"
        ),
    },
]


# =========================================================
# 問題取得
# =========================================================


def get_questions_for_batch(batch_number):
    """
    指定されたセットの問題を取得する。

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

    return QUESTION_BANK[start:end]


# =========================================================
# 問題番号取得
# =========================================================


def get_question_number(question):
    """
    実際の小問番号を返す。
    """

    return question.get(
        "question_number",
        0,
    )


# =========================================================
# 選択肢取得
# =========================================================


def get_option_by_label(
    question,
    label,
):
    """
    記号から選択肢を取得する。
    """

    for option in question["options"]:

        if option["label"] == label:

            return option

    return None


# =========================================================
# 回答判定
# =========================================================


def check_answer(
    question,
    user_answer,
):
    """
    選択式問題を判定する。

    user_answer は、
        ア
        イ
        ウ
        エ

    のいずれか。
    """

    correct_label = question[
        "answer"
    ]

    normalized_user = (
        str(user_answer).strip()
    )

    # -----------------------------------------------------
    # 未回答
    # -----------------------------------------------------

    if not normalized_user:

        return {
            "is_correct": False,
            "judgement": "未回答",
            "mistake_type": "unanswered",
            "feedback": (
                "この問題には回答がありません。"
            ),
        }

    # -----------------------------------------------------
    # 正解
    # -----------------------------------------------------

    if normalized_user == correct_label:

        return {
            "is_correct": True,
            "judgement": "正解",
            "mistake_type": "none",
            "feedback": (
                "正解です。\n\n"
                + question["explanation"]
            ),
        }

    # -----------------------------------------------------
    # 不正解
    # -----------------------------------------------------

    selected_option = (
        get_option_by_label(
            question,
            normalized_user,
        )
    )

    if selected_option:

        mistake_type = (
            selected_option.get(
                "error_type",
                "other",
            )
        )

    else:

        mistake_type = "invalid_answer"

    return {
        "is_correct": False,
        "judgement": "不正解",
        "mistake_type": mistake_type,
        "feedback": (
            "今回は正解ではありません。\n\n"
            + question["explanation"]
        ),
    }


# =========================================================
# 5問一括採点
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

        question_id = question["id"]

        user_answer = answers.get(
            question_id,
            "",
        )

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
    """
    1問分の学習履歴を作成する。
    """

    objective_id = question[
        "objective"
    ]

    objective = LEARNING_OBJECTIVES[
        objective_id
    ]

    correct_option = (
        get_option_by_label(
            question,
            question["answer"],
        )
    )

    selected_option = (
        get_option_by_label(
            question,
            user_answer,
        )
    )

    return {
        "timestamp": datetime.now().isoformat(
            timespec="seconds"
        ),

        "batch_number": (
            st.session_state.batch_number
            + 1
        ),

        "major_question": question[
            "major_question"
        ],

        "question_number": question[
            "question_number"
        ],

        "question_id": question[
            "id"
        ],

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

        "japanese": question[
            "japanese"
        ],

        "english": question[
            "english"
        ],

        "user_answer": user_answer,

        "user_answer_value": (
            selected_option["value"]
            if selected_option
            else ""
        ),

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
# 全体成績
# =========================================================


def calculate_overall_stats():

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


# =========================================================
# 学習目標別成績
# =========================================================


def calculate_objective_stats():

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
# 今回のセットの誤答内訳
# =========================================================


def calculate_batch_mistake_stats(
    batch_results,
):
    """
    今回の5問について、
    誤答タイプを内部的に集計する。
    """

    mistake_stats = {}

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
# 全体の誤答データ
# =========================================================


def calculate_all_mistake_stats():

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
# JSON保存
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
# JSON復元
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
    # 新しい状態バージョン
    # -----------------------------------------------------

    if current_version != STATE_VERSION:

        st.session_state.state_version = (
            STATE_VERSION
        )

        st.session_state.batch_number = 0

        st.session_state.history = []

        st.session_state.batch_results = None

        st.session_state.batch_submitted = (
            False
        )

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

            st.session_state.batch_submitted = (
                False
            )

    if (
        "student_name"
        not in st.session_state
    ):

        st.session_state.student_name = ""


initialize_state()


# =========================================================
# 現在の5問
# =========================================================


current_questions = (
    get_questions_for_batch(
        st.session_state.batch_number
    )
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
    "選択肢をクリックして答えてください。"
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
# 今回の学習目標
# =========================================================


st.markdown("---")

st.markdown(
    "### 🎯 今回の学習目標"
)

st.write(
    "**動名詞の基本を理解する**"
)

st.caption(
    "今回の問題では、動名詞の形と、"
    "like・enjoy・finish の後ろでの使い方を確認します。"
)


# =========================================================
# 大問1
# =========================================================


st.markdown("---")

st.markdown(
    "## 📄 大問1"
)

st.info(
    MAJOR_QUESTION_INSTRUCTION
)


# =========================================================
# 5問回答フォーム
# =========================================================


with st.form(
    f"major_question_1_batch_"
    f"{st.session_state.batch_number}"
):

    selected_answers = {}

    for index, question in enumerate(
        current_questions,
        start=1,
    ):

        # -------------------------------------------------
        # 小問番号
        # -------------------------------------------------

        st.markdown(
            f"### {index}."
        )

        # -------------------------------------------------
        # 日本語
        # -------------------------------------------------

        st.write(
            f"**{question['japanese']}**"
        )

        # -------------------------------------------------
        # 英文
        # -------------------------------------------------

        st.info(
            question["english"]
        )

        # -------------------------------------------------
        # 選択肢
        # -------------------------------------------------

        option_map = {
            option["label"]: option[
                "value"
            ]
            for option in question[
                "options"
            ]
        }

        selected_label = st.radio(
            "答えを選んでください",
            options=CHOICE_LABELS,
            format_func=lambda label: (
                f"{label}．"
                f"{option_map.get(label, '')}"
            ),
            key=(
                f"choice_"
                f"{st.session_state.batch_number}_"
                f"{question['id']}"
            ),
            index=None,
            horizontal=False,
            label_visibility="visible",
        )

        selected_answers[
            question["id"]
        ] = (
            selected_label
            if selected_label is not None
            else ""
        )

        if index < len(
            current_questions
        ):

            st.markdown("---")

    # -----------------------------------------------------
    # 一括採点
    # -----------------------------------------------------

    submit_batch = (
        st.form_submit_button(
            "5問をまとめて採点する 📝",
            type="primary",
        )
    )


# =========================================================
# 一括採点処理
# =========================================================


if submit_batch:

    batch_results = evaluate_batch(
        current_questions,
        selected_answers,
    )

    st.session_state.batch_results = (
        batch_results
    )

    st.session_state.batch_submitted = (
        True
    )

    # -----------------------------------------------------
    # 履歴へ追加
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
# 今回の結果
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
        for item in batch_results
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


    # =====================================================
    # 各小問の結果
    # =====================================================

    st.markdown(
        "### 🔍 各小問の結果"
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

        question_number = (
            question[
                "question_number"
            ]
        )

        # -------------------------------------------------
        # 正誤表示
        # -------------------------------------------------

        if result.get(
            "is_correct",
            False,
        ):

            st.success(
                f"{question_number}. 🟢 正解"
            )

        elif result.get(
            "mistake_type"
        ) == "unanswered":

            st.warning(
                f"{question_number}. ⚪ 未回答"
            )

        else:

            st.error(
                f"{question_number}. 🔴 不正解"
            )

        # -------------------------------------------------
        # 日本語
        # -------------------------------------------------

        st.write(
            f"**日本語：**"
            f"{question['japanese']}"
        )

        # -------------------------------------------------
        # 英文
        # -------------------------------------------------

        st.write(
            f"**英文：**"
            f"{question['english']}"
        )

        # -------------------------------------------------
        # 生徒の回答
        # -------------------------------------------------

        if user_answer:

            selected_option = (
                get_option_by_label(
                    question,
                    user_answer,
                )
            )

            if selected_option:

                st.write(
                    f"あなたの答え："
                    f"**{selected_option['label']}．"
                    f"{selected_option['value']}**"
                )

        else:

            st.write(
                "あなたの答え："
                "**未回答**"
            )

        # -------------------------------------------------
        # 正解
        # -------------------------------------------------

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

        # -------------------------------------------------
        # 解説
        # -------------------------------------------------

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
    # 今回の誤答内訳
    # =====================================================

    st.markdown(
        "### 🔎 今回の誤答内訳"
    )

    batch_mistakes = (
        calculate_batch_mistake_stats(
            batch_results
        )
    )

    if not batch_mistakes:

        st.success(
            "今回の5問では誤答はありませんでした。"
        )

    else:

        mistake_labels = {
            "base_form": (
                "原形を選択"
            ),
            "past_form": (
                "過去形を選択"
            ),
            "third_person": (
                "三単現の形を選択"
            ),
            "other": (
                "その他"
            ),
            "invalid_answer": (
                "無効な回答"
            ),
            "unanswered": (
                "未回答"
            ),
        }

        for (
            mistake_type,
            count,
        ) in sorted(
            batch_mistakes.items(),
            key=lambda item: item[1],
            reverse=True,
        ):

            label = mistake_labels.get(
                mistake_type,
                mistake_type,
            )

            st.write(
                f"- {label}："
                f"{count}問"
            )


    # =====================================================
    # 次の5問
    # =====================================================

    next_start = (
        (
            st.session_state.batch_number
            + 1
        )
        * QUESTIONS_PER_BATCH
    )

    if next_start < len(
        QUESTION_BANK
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

            st.rerun()

    else:

        st.markdown("---")

        st.success(
            "現在用意されている問題はすべて終了しました。"
        )


# =========================================================
# 学習状況
# =========================================================


if st.session_state.history:

    st.markdown("---")

    st.markdown(
        "## 📊 学習状況"
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


    # =====================================================
    # 学習目標別
    # =====================================================

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
            f"**{stat['name']}：** "
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


    # =====================================================
    # 詳細な学習履歴
    # =====================================================

    with st.expander(
        "📝 詳細な学習履歴"
    ):

        # -------------------------------------------------
        # 新しい順に表示するが、
        # 問題番号は実際の問題番号を使用する。
        # -------------------------------------------------

        for record in reversed(
            st.session_state.history
        ):

            question_number = record.get(
                "question_number",
                "",
            )

            batch_number = record.get(
                "batch_number",
                "",
            )

            is_correct = record.get(
                "is_correct",
                False,
            )

            mistake_type = record.get(
                "mistake_type",
                "",
            )

            if is_correct:

                status = "🟢 正解"

            elif mistake_type == (
                "unanswered"
            ):

                status = "⚪ 未回答"

            else:

                status = "🔴 不正解"

            st.markdown(
                f"### 第{question_number}問 "
                f"{status}"
            )

            st.caption(
                f"大問："
                f"{record.get('major_question', '')}"
                f"　"
                f"セット："
                f"{batch_number}"
            )

            st.caption(
                f"学習項目："
                f"{record.get('objective_name', '')}"
            )

            st.write(
                f"日本語："
                f"{record.get('japanese', '')}"
            )

            st.write(
                f"英文："
                f"{record.get('english', '')}"
            )

            # -------------------------------------------------
            # 生徒向け表示では技術的な誤答タイプを出さない
            # -------------------------------------------------

            user_answer = record.get(
                "user_answer",
                "",
            )

            user_answer_value = record.get(
                "user_answer_value",
                "",
            )

            if user_answer:

                if user_answer_value:

                    st.write(
                        f"あなたの答え："
                        f"**{user_answer}．"
                        f"{user_answer_value}**"
                    )

                else:

                    st.write(
                        f"あなたの答え："
                        f"**{user_answer}**"
                    )

            else:

                st.write(
                    "あなたの答え："
                    "**未回答**"
                )

            st.write(
                f"正解："
                f"**{record.get('correct_answer', '')}．"
                f"{record.get('correct_value', '')}**"
            )

            st.write(
                record.get(
                    "feedback",
                    "",
                )
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
# JSON保存
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
# JSON復元
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
        f"状態バージョン："
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
        "大問形式："
        "日本文に合う英文の空欄補充4択"
    )

    st.write(
        "選択肢：ア・イ・ウ・エ"
    )

    st.write(
        "回答方法：クリック式"
    )

    st.write(
        "日本語訳：各小問に表示"
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
        "誤答タイプ：内部データとして保存"
    )

    st.write(
        "学習履歴："
        "Streamlitセッション＋JSON"
    )
