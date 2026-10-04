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

APP_VERSION = "1.2.0"
STATE_VERSION = 4


# =========================================================
# 教育設計
# =========================================================
#
# 第1段階では、
#
# 「空欄補充 × 4択」
#
# に限定する。
#
# 生徒は、
#
#   ア
#   イ
#   ウ
#   エ
#
# の記号で回答する。
#
# 選択肢そのものを入力した場合も受け付ける。
#
# AIは現段階では使用しない。
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
# すべて「空欄補充 × 4択」。
#
# answer:
#   正解の記号
#
# options:
#   ア・イ・ウ・エの4択
#
# =========================================================


QUESTION_BANK = [

    # -----------------------------------------------------
    # 動名詞の基本
    # -----------------------------------------------------

    {
        "id": "basic_001",
        "question_type": "fill_blank_choice",
        "objective": "gerund_basic",
        "difficulty": 1,
        "question": (
            "次の英文の空欄に入る最も適切な語を選びなさい。"
            "\n\n"
            "（　　　）is fun."
        ),
        "japanese": "「泳ぐことは楽しいです。」",
        "options": [
            {
                "label": "ア",
                "value": "Swim",
            },
            {
                "label": "イ",
                "value": "Swimming",
            },
            {
                "label": "ウ",
                "value": "Swims",
            },
            {
                "label": "エ",
                "value": "Swam",
            },
        ],
        "answer": "イ",
        "explanation": (
            "「泳ぐこと」を表す動名詞は "
            "swim に -ing を付けた Swimming です。"
        ),
    },

    {
        "id": "basic_002",
        "question_type": "fill_blank_choice",
        "objective": "gerund_basic",
        "difficulty": 1,
        "question": (
            "次の英文の空欄に入る最も適切な語を選びなさい。"
            "\n\n"
            "My hobby is（　　　）pictures."
        ),
        "japanese": "「私の趣味は絵を描くことです。」",
        "options": [
            {
                "label": "ア",
                "value": "draw",
            },
            {
                "label": "イ",
                "value": "drew",
            },
            {
                "label": "ウ",
                "value": "drawing",
            },
            {
                "label": "エ",
                "value": "draws",
            },
        ],
        "answer": "ウ",
        "explanation": (
            "「絵を描くこと」は動名詞 drawing で表します。"
        ),
    },

    # -----------------------------------------------------
    # like + 動名詞
    # -----------------------------------------------------

    {
        "id": "like_001",
        "question_type": "fill_blank_choice",
        "objective": "like_gerund",
        "difficulty": 1,
        "question": (
            "次の英文の空欄に入る最も適切な語を選びなさい。"
            "\n\n"
            "I like（　　　）tennis."
        ),
        "japanese": "「私はテニスをすることが好きです。」",
        "options": [
            {
                "label": "ア",
                "value": "playing",
            },
            {
                "label": "イ",
                "value": "play",
            },
            {
                "label": "ウ",
                "value": "played",
            },
            {
                "label": "エ",
                "value": "plays",
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
            "次の英文の空欄に入る最も適切な語を選びなさい。"
            "\n\n"
            "I like（　　　）to music."
        ),
        "japanese": "「私は音楽を聴くことが好きです。」",
        "options": [
            {
                "label": "ア",
                "value": "listen",
            },
            {
                "label": "イ",
                "value": "listening",
            },
            {
                "label": "ウ",
                "value": "listened",
            },
            {
                "label": "エ",
                "value": "listens",
            },
        ],
        "answer": "イ",
        "explanation": (
            "like の後ろに動名詞を使うので、"
            "listen → listening となります。"
        ),
    },

    {
        "id": "like_003",
        "question_type": "fill_blank_choice",
        "objective": "like_gerund",
        "difficulty": 2,
        "question": (
            "次の英文の空欄に入る最も適切な語を選びなさい。"
            "\n\n"
            "She likes（　　　）books."
        ),
        "japanese": "「彼女は本を読むことが好きです。」",
        "options": [
            {
                "label": "ア",
                "value": "read",
            },
            {
                "label": "イ",
                "value": "reads",
            },
            {
                "label": "ウ",
                "value": "reading",
            },
            {
                "label": "エ",
                "value": "readed",
            },
        ],
        "answer": "ウ",
        "explanation": (
            "like の後ろに動名詞 reading を使います。"
        ),
    },

    # -----------------------------------------------------
    # enjoy + 動名詞
    # -----------------------------------------------------

    {
        "id": "enjoy_001",
        "question_type": "fill_blank_choice",
        "objective": "enjoy_gerund",
        "difficulty": 1,
        "question": (
            "次の英文の空欄に入る最も適切な語を選びなさい。"
            "\n\n"
            "I enjoy（　　　）English."
        ),
        "japanese": "「私は英語を勉強することを楽しんでいます。」",
        "options": [
            {
                "label": "ア",
                "value": "study",
            },
            {
                "label": "イ",
                "value": "studying",
            },
            {
                "label": "ウ",
                "value": "studied",
            },
            {
                "label": "エ",
                "value": "studies",
            },
        ],
        "answer": "イ",
        "explanation": (
            "enjoy の後ろに動名詞 studying を使います。"
        ),
    },

    {
        "id": "enjoy_002",
        "question_type": "fill_blank_choice",
        "objective": "enjoy_gerund",
        "difficulty": 1,
        "question": (
            "次の英文の空欄に入る最も適切な語を選びなさい。"
            "\n\n"
            "I enjoy（　　　）."
        ),
        "japanese": "「私は料理をすることを楽しんでいます。」",
        "options": [
            {
                "label": "ア",
                "value": "cook",
            },
            {
                "label": "イ",
                "value": "cooked",
            },
            {
                "label": "ウ",
                "value": "cooks",
            },
            {
                "label": "エ",
                "value": "cooking",
            },
        ],
        "answer": "エ",
        "explanation": (
            "enjoy の後ろに動名詞 cooking を使います。"
        ),
    },

    {
        "id": "enjoy_003",
        "question_type": "fill_blank_choice",
        "objective": "enjoy_gerund",
        "difficulty": 2,
        "question": (
            "次の英文の空欄に入る最も適切な語を選びなさい。"
            "\n\n"
            "He enjoys（　　　）soccer."
        ),
        "japanese": "「彼はサッカーをすることを楽しんでいます。」",
        "options": [
            {
                "label": "ア",
                "value": "play",
            },
            {
                "label": "イ",
                "value": "playing",
            },
            {
                "label": "ウ",
                "value": "played",
            },
            {
                "label": "エ",
                "value": "plays",
            },
        ],
        "answer": "イ",
        "explanation": (
            "enjoys の後ろに動名詞 playing を使います。"
        ),
    },

    # -----------------------------------------------------
    # finish + 動名詞
    # -----------------------------------------------------

    {
        "id": "finish_001",
        "question_type": "fill_blank_choice",
        "objective": "finish_gerund",
        "difficulty": 1,
        "question": (
            "次の英文の空欄に入る最も適切な語を選びなさい。"
            "\n\n"
            "I finished（　　　）my homework."
        ),
        "japanese": "「私は宿題を終えました。」",
        "options": [
            {
                "label": "ア",
                "value": "do",
            },
            {
                "label": "イ",
                "value": "doing",
            },
            {
                "label": "ウ",
                "value": "did",
            },
            {
                "label": "エ",
                "value": "does",
            },
        ],
        "answer": "イ",
        "explanation": (
            "finish の後ろに動名詞 doing を使います。"
        ),
    },

    {
        "id": "finish_002",
        "question_type": "fill_blank_choice",
        "objective": "finish_gerund",
        "difficulty": 1,
        "question": (
            "次の英文の空欄に入る最も適切な語を選びなさい。"
            "\n\n"
            "She finished（　　　）lunch."
        ),
        "japanese": "「彼女は昼食を食べ終えました。」",
        "options": [
            {
                "label": "ア",
                "value": "eat",
            },
            {
                "label": "イ",
                "value": "eats",
            },
            {
                "label": "ウ",
                "value": "eating",
            },
            {
                "label": "エ",
                "value": "ate",
            },
        ],
        "answer": "ウ",
        "explanation": (
            "finish の後ろに動名詞 eating を使います。"
        ),
    },
]


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
    回答比較用の正規化。

    「ア」「ア。」「ア．」などを
    同じ回答として扱えるようにする。
    """

    if text is None:
        return ""

    text = str(text).strip()

    text = text.replace(
        "　",
        " ",
    )

    text = text.lower()

    # 選択記号の後ろについた句読点を除去
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
# 回答判定
# =========================================================


def check_answer(
    question,
    user_answer,
):
    """
    4択問題を判定する。

    例：

        ア
        イ
        ウ
        エ

    の記号で回答可能。

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
    # 記号で回答
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
    # 選択肢そのもので回答
    # -----------------------------------------------------

    if normalized_user == correct_value:

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

    return {
        "is_correct": False,
        "judgement": "要復習",
        "mistake_type": "answer_error",
        "feedback": (
            "今回は正解ではありません。\n\n"
            + question["explanation"]
        ),
    }


# =========================================================
# 学習履歴
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
        "correct_answer": (
            question["answer"]
        ),
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
# 学習目標別成績
# =========================================================


def calculate_objective_stats():
    """学習目標ごとの成績を計算する。"""

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
# 次の問題
# =========================================================
#
# 現段階では複雑な適応学習を入れず、
# 未回答の問題を順番に出す。
#
# =========================================================


def select_next_question():

    attempted_ids = {
        record.get(
            "question_id"
        )
        for record
        in st.session_state.history
    }

    # 未回答問題を探す
    for question in QUESTION_BANK:

        if question["id"] not in attempted_ids:

            return question

    # 全問終了したら最初に戻る
    return QUESTION_BANK[0]


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

        st.session_state.current_question_id = (
            QUESTION_BANK[0]["id"]
        )

        st.session_state.history = []

        st.session_state.feedback = None

        st.session_state.next_ready = False

        st.session_state.last_result = None

    # -----------------------------------------------------
    # 通常起動
    # -----------------------------------------------------

    else:

        if (
            "current_question_id"
            not in st.session_state
        ):

            st.session_state.current_question_id = (
                QUESTION_BANK[0]["id"]
            )

        if (
            "history"
            not in st.session_state
        ):

            st.session_state.history = []

        if (
            "feedback"
            not in st.session_state
        ):

            st.session_state.feedback = None

        if (
            "next_ready"
            not in st.session_state
        ):

            st.session_state.next_ready = False

        if (
            "last_result"
            not in st.session_state
        ):

            st.session_state.last_result = None

    if (
        "student_name"
        not in st.session_state
    ):

        st.session_state.student_name = ""


initialize_state()


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
    "この試験版では、まず空欄補充の4択問題で"
    "基礎を確認します。"
    "答えは「ア・イ・ウ・エ」の記号で入力できます。"
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
# 現在の問題
# =========================================================


question = get_current_question()

objective = LEARNING_OBJECTIVES[
    question["objective"]
]


st.markdown("---")


# =========================================================
# 学習目標
# =========================================================


st.markdown(
    "### 🎯 今回の学習目標"
)

st.write(
    f"**{objective['name']}**"
)

st.caption(
    objective["description"]
)


# =========================================================
# 問題
# =========================================================


st.markdown(
    "### 📌 問題"
)

st.caption(
    "問題形式：空欄補充・4択"
)

st.info(
    question["question"]
)


# =========================================================
# 選択肢
# =========================================================


st.markdown(
    "#### 選択肢"
)

for option in question["options"]:

    st.write(
        f"**{option['label']}．** "
        f"{option['value']}"
    )


st.caption(
    "答えは「ア・イ・ウ・エ」の記号で入力してください。"
)


# =========================================================
# 回答
# =========================================================


with st.form(
    "answer_form"
):

    user_answer = st.text_input(
        "あなたの答え",
        placeholder="例：イ",
    )

    submit_button = (
        st.form_submit_button(
            "回答する 🚀",
            type="primary",
        )
    )


# =========================================================
# 回答処理
# =========================================================


if submit_button:

    if not user_answer.strip():

        st.warning(
            "答えを入力してください。"
        )

    else:

        try:

            result = check_answer(
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

            st.session_state.feedback = (
                result
            )

            st.session_state.last_result = (
                result
            )

            st.session_state.next_ready = (
                True
            )

            st.rerun()

        except Exception as e:

            st.error(
                "回答の判定中にエラーが発生しました。"
            )

            with st.expander(
                "🔧 エラー詳細"
            ):

                st.code(
                    str(e),
                    language="text",
                )


# =========================================================
# フィードバック
# =========================================================


feedback_data = (
    st.session_state.get(
        "feedback"
    )
)


if (
    isinstance(
        feedback_data,
        dict,
    )
    and "is_correct"
    in feedback_data
):

    result = feedback_data

    st.markdown("---")

    if result.get(
        "is_correct",
        False,
    ):

        st.success(
            "🟢 正解です！"
        )

    else:

        st.error(
            "🔴 不正解です。"
        )

    st.markdown(
        "### 🔍 解説"
    )

    st.write(
        result.get(
            "feedback",
            "",
        )
    )

    # -----------------------------------------------------
    # 不正解の場合
    # -----------------------------------------------------

    if not result.get(
        "is_correct",
        False,
    ):

        correct_option = (
            get_option_by_label(
                question,
                question["answer"],
            )
        )

        if correct_option:

            st.markdown(
                "### 📖 正解"
            )

            st.write(
                f"**{correct_option['label']}．"
                f"{correct_option['value']}**"
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

    stats = (
        calculate_objective_stats()
    )

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

    col1, col2, col3 = (
        st.columns(3)
    )

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
            "正答率",
            f"{overall_accuracy:.1f}%",
        )


    # -----------------------------------------------------
    # 学習目標別
    # -----------------------------------------------------

    st.markdown(
        "### 🎯 学習目標別の学習状況"
    )

    for (
        objective_id,
        stat,
    ) in stats.items():

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

            if record.get(
                "is_correct",
                False,
            ):

                status = "🟢 正解"

            else:

                status = "🔴 不正解"

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
                f"正解："
                f"{record.get('correct_answer', '')}"
                f"（"
                f"{record.get('correct_value', '')}"
                f"）"
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
        f"現在の問題形式："
        f"{question['question_type']}"
    )

    st.write(
        f"問題数："
        f"{len(QUESTION_BANK)}問"
    )

    st.write(
        f"学習目標数："
        f"{len(LEARNING_OBJECTIVES)}"
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
        "AI問題生成：使用しない"
    )

    st.write(
        "AI採点：使用しない"
    )

    st.write(
        "正誤判定：Python"
    )

    st.write(
        "次問題選択：固定順"
    )

    st.write(
        "学習履歴："
        "Streamlitセッション＋JSON"
    )
