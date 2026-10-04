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


APP_VERSION = "1.1.0"
STATE_VERSION = 3


# =========================================================
# 教育設計
# =========================================================
#
# 第1段階では、
#
# ・問題形式：空欄補充
# ・AIによる問題生成：使用しない
# ・AIによる採点：使用しない
# ・正誤判定：Pythonで行う
#
# とする。
#
# まずは「簡単な問題から始める」という
# 教育設計そのものを検証する。
#


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
# 選択肢の記号
# =========================================================
#
# 今後、選択問題を追加するときは必ず
# ア・イ・ウ・エを使用する。
#
# 生徒は、
#
# ・「ア」
# ・「イ」
# ・「ウ」
# ・「エ」
#
# の記号だけで回答してもよい。
#


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
# question_type:
#
#   fill_blank
#       → 空欄補充
#
#   choice
#       → 選択問題
#
# 第1段階では fill_blank のみ使用する。
#
# 将来的に choice を追加する場合、
# options は必ず4択までとし、
# ア・イ・ウ・エを付ける。
#


QUESTION_BANK = [

    # -----------------------------------------------------
    # 動名詞の基本
    # -----------------------------------------------------

    {
        "id": "basic_001",
        "question_type": "fill_blank",
        "objective": "gerund_basic",
        "difficulty": 1,
        "question": (
            "次の英文の空欄に入る適切な語を書きなさい。\n\n"
            "______ is fun."
        ),
        "japanese": "「泳ぐことは楽しいです。」",
        "answer": "Swimming",
        "accepted_answers": [
            "Swimming",
            "swimming",
        ],
        "explanation": (
            "「泳ぐこと」を表す動名詞は "
            "swim に -ing を付けた Swimming です。"
        ),
    },

    {
        "id": "basic_002",
        "question_type": "fill_blank",
        "objective": "gerund_basic",
        "difficulty": 1,
        "question": (
            "次の英文の空欄に入る適切な語を書きなさい。\n\n"
            "I enjoy ______."
        ),
        "japanese": "「私は泳ぐことを楽しんでいます。」",
        "answer": "swimming",
        "accepted_answers": [
            "swimming",
            "Swimming",
        ],
        "explanation": (
            "enjoy の後ろでは、今回の学習目標として "
            "動名詞 swimming を使います。"
        ),
    },


    # -----------------------------------------------------
    # like + 動名詞
    # -----------------------------------------------------

    {
        "id": "like_001",
        "question_type": "fill_blank",
        "objective": "like_gerund",
        "difficulty": 1,
        "question": (
            "次の英文の空欄に入る適切な語を書きなさい。\n\n"
            "I like ______ tennis."
        ),
        "japanese": "「私はテニスをすることが好きです。」",
        "answer": "playing",
        "accepted_answers": [
            "playing",
        ],
        "explanation": (
            "like の後ろに動名詞を使うので、"
            "play → playing となります。"
        ),
    },

    {
        "id": "like_002",
        "question_type": "fill_blank",
        "objective": "like_gerund",
        "difficulty": 1,
        "question": (
            "次の英文の空欄に入る適切な語を書きなさい。\n\n"
            "I like ______ to music."
        ),
        "japanese": "「私は音楽を聴くことが好きです。」",
        "answer": "listening",
        "accepted_answers": [
            "listening",
        ],
        "explanation": (
            "like の後ろに動名詞を使うので、"
            "listen → listening となります。"
        ),
    },

    {
        "id": "like_003",
        "question_type": "fill_blank",
        "objective": "like_gerund",
        "difficulty": 2,
        "question": (
            "次の英文の空欄に入る適切な語を書きなさい。\n\n"
            "She likes ______ books."
        ),
        "japanese": "「彼女は本を読むことが好きです。」",
        "answer": "reading",
        "accepted_answers": [
            "reading",
        ],
        "explanation": (
            "read に -ing を付けて reading とします。"
            "また、主語が She なので like は likes になっています。"
        ),
    },


    # -----------------------------------------------------
    # enjoy + 動名詞
    # -----------------------------------------------------

    {
        "id": "enjoy_001",
        "question_type": "fill_blank",
        "objective": "enjoy_gerund",
        "difficulty": 1,
        "question": (
            "次の英文の空欄に入る適切な語を書きなさい。\n\n"
            "I enjoy ______ English."
        ),
        "japanese": "「私は英語を勉強することを楽しんでいます。」",
        "answer": "studying",
        "accepted_answers": [
            "studying",
        ],
        "explanation": (
            "enjoy の後ろに動名詞を使うので、"
            "study → studying となります。"
        ),
    },

    {
        "id": "enjoy_002",
        "question_type": "fill_blank",
        "objective": "enjoy_gerund",
        "difficulty": 1,
        "question": (
            "次の英文の空欄に入る適切な語を書きなさい。\n\n"
            "I enjoy ______."
        ),
        "japanese": "「私は料理をすることを楽しんでいます。」",
        "answer": "cooking",
        "accepted_answers": [
            "cooking",
        ],
        "explanation": (
            "cook に -ing を付けて cooking とします。"
        ),
    },

    {
        "id": "enjoy_003",
        "question_type": "fill_blank",
        "objective": "enjoy_gerund",
        "difficulty": 2,
        "question": (
            "次の英文の空欄に入る適切な語を書きなさい。\n\n"
            "He enjoys ______ soccer."
        ),
        "japanese": "「彼はサッカーをすることを楽しんでいます。」",
        "answer": "playing",
        "accepted_answers": [
            "playing",
        ],
        "explanation": (
            "play に -ing を付けて playing とします。"
        ),
    },


    # -----------------------------------------------------
    # finish + 動名詞
    # -----------------------------------------------------

    {
        "id": "finish_001",
        "question_type": "fill_blank",
        "objective": "finish_gerund",
        "difficulty": 1,
        "question": (
            "次の英文の空欄に入る適切な語を書きなさい。\n\n"
            "I finished ______ my homework."
        ),
        "japanese": "「私は宿題を終えました。」",
        "answer": "doing",
        "accepted_answers": [
            "doing",
        ],
        "explanation": (
            "finish の後ろに動名詞を使うので、"
            "do → doing となります。"
        ),
    },

    {
        "id": "finish_002",
        "question_type": "fill_blank",
        "objective": "finish_gerund",
        "difficulty": 1,
        "question": (
            "次の英文の空欄に入る適切な語を書きなさい。\n\n"
            "She finished ______ lunch."
        ),
        "japanese": "「彼女は昼食を食べ終えました。」",
        "answer": "eating",
        "accepted_answers": [
            "eating",
        ],
        "explanation": (
            "finish の後ろに動名詞を使うので、"
            "eat → eating となります。"
        ),
    },


    # =====================================================
    # 将来の選択問題のサンプル
    # =====================================================
    #
    # 現在は試験対象外。
    #
    # choice 形式では、必ず
    # ア・イ・ウ・エ
    # の記号を付ける。
    #
    # 生徒は「ア」だけを入力しても正解になる。
    #
    # =====================================================

    {
        "id": "choice_sample_001",
        "question_type": "choice",
        "objective": "like_gerund",
        "difficulty": 1,
        "enabled": False,
        "question": (
            "次の空欄に入る最も適切な語を選びなさい。\n\n"
            "I like ______ tennis."
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
        "accepted_answers": [
            "ア",
            "a",
            "A",
            "playing",
        ],
        "explanation": (
            "like の後ろに動名詞 playing を使います。"
        ),
    },
]


# =========================================================
# 有効な問題だけを取得
# =========================================================


def get_enabled_questions():
    """
    現在の試験で使用する問題だけを取得する。

    enabled が指定されていない問題は有効とする。
    enabled=False の問題は除外する。
    """

    return [
        question
        for question in QUESTION_BANK
        if question.get(
            "enabled",
            True,
        )
    ]


# =========================================================
# 問題取得
# =========================================================


def get_question(question_id):
    """問題IDから問題を取得する。"""

    for question in QUESTION_BANK:

        if question["id"] == question_id:

            return question

    enabled_questions = get_enabled_questions()

    if enabled_questions:

        return enabled_questions[0]

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
    回答比較用の最低限の正規化。

    ・前後の空白を削除
    ・連続した空白を1つにする
    ・大文字・小文字を統一
    ・全角・半角の大きな差をできるだけ吸収
    """

    text = str(text).strip()

    text = " ".join(
        text.split()
    )

    text = text.lower()

    return text


# =========================================================
# 選択肢の表示用
# =========================================================


def format_choices(question):
    """
    選択問題の選択肢を表示用文字列にする。

    必ず
    ア．
    イ．
    ウ．
    エ．
    の形式にする。
    """

    lines = []

    for option in question.get(
        "options",
        [],
    ):

        label = option["label"]

        value = option["value"]

        lines.append(
            f"{label}．{value}"
        )

    return "\n".join(lines)


# =========================================================
# 回答判定
# =========================================================


def check_answer(
    question,
    user_answer,
):
    """
    問題形式に応じて回答を判定する。

    fill_blank:
        入力された語を正解と比較。

    choice:
        ア・イ・ウ・エの記号、
        または選択肢の内容そのものを受け付ける。
    """

    question_type = question[
        "question_type"
    ]

    normalized_user = normalize_answer(
        user_answer
    )

    # -----------------------------------------------------
    # 空欄補充
    # -----------------------------------------------------

    if question_type == "fill_blank":

        accepted_answers = [
            normalize_answer(answer)
            for answer
            in question.get(
                "accepted_answers",
                [],
            )
        ]

        is_correct = (
            normalized_user
            in accepted_answers
        )

        if is_correct:

            return {
                "is_correct": True,
                "judgement": "正解",
                "feedback": (
                    "正解です。"
                    "\n\n"
                    + question["explanation"]
                ),
                "mistake_type": "none",
            }

        return {
            "is_correct": False,
            "judgement": "要復習",
            "feedback": (
                "今回は正解ではありません。"
                "\n\n"
                + question["explanation"]
            ),
            "mistake_type": "answer_error",
        }

    # -----------------------------------------------------
    # 選択問題
    # -----------------------------------------------------

    if question_type == "choice":

        correct_label = normalize_answer(
            question["answer"]
        )

        accepted_answers = [
            normalize_answer(answer)
            for answer
            in question.get(
                "accepted_answers",
                [],
            )
        ]

        # 記号でも選択肢そのものでも回答可能
        if (
            normalized_user
            in accepted_answers
        ):

            return {
                "is_correct": True,
                "judgement": "正解",
                "feedback": (
                    "正解です。"
                    "\n\n"
                    + question["explanation"]
                ),
                "mistake_type": "none",
            }

        return {
            "is_correct": False,
            "judgement": "要復習",
            "feedback": (
                "今回は正解ではありません。"
                "\n\n"
                + question["explanation"]
            ),
            "mistake_type": "answer_error",
        }

    # -----------------------------------------------------
    # 未対応の問題形式
    # -----------------------------------------------------

    raise ValueError(
        f"未対応の問題形式です："
        f"{question_type}"
    )


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
            question.get(
                "answer",
                "",
            )
            if question["question_type"]
            == "choice"
            else question.get(
                "answer",
                "",
            )
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
# 次の問題を選択
# =========================================================
#
# 第1段階では、AIによる適応判断をしない。
#
# まず未学習の問題を順番に出す。
#
# 問題形式・難易度・学習項目の
# 適応ロジックは今後の試験結果を見て改善する。
#


def select_next_question():
    """
    次の問題をルールベースで選択する。
    """

    enabled_questions = (
        get_enabled_questions()
    )

    attempted_ids = {
        record.get(
            "question_id"
        )
        for record
        in st.session_state.history
    }

    # -----------------------------------------------------
    # 未回答の問題を優先
    # -----------------------------------------------------

    unattempted = [
        question
        for question
        in enabled_questions
        if question["id"]
        not in attempted_ids
    ]

    if unattempted:

        # 難易度の低いものから
        unattempted.sort(
            key=lambda question: (
                question[
                    "difficulty"
                ],
                question["id"],
            )
        )

        return unattempted[0]

    # -----------------------------------------------------
    # 全問終了後
    # -----------------------------------------------------
    #
    # 現段階では最初の問題に戻る。
    #
    # 今後、
    # 「間違えた問題を再出題」
    # 「弱点項目を優先」
    # などに発展させる。
    #

    return enabled_questions[0]


# =========================================================
# 学習履歴エクスポート
# =========================================================


def create_export_data():
    """学習履歴をJSON形式にする。"""

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
    """保存済みJSONを読み込む。"""

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
    """
    セッション状態を初期化する。

    バージョンが変わった場合、
    古い問題形式との混在を避けるため、
    現在の一時状態をリセットする。
    """

    current_version = (
        st.session_state.get(
            "state_version"
        )
    )

    if current_version != STATE_VERSION:

        st.session_state.state_version = (
            STATE_VERSION
        )

        st.session_state.current_question_id = (
            "basic_001"
        )

        st.session_state.history = []

        st.session_state.feedback = None

        st.session_state.next_ready = False

        st.session_state.last_result = None

    else:

        if (
            "current_question_id"
            not in st.session_state
        ):

            st.session_state.current_question_id = (
                "basic_001"
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
    "第1段階：動名詞・空欄補充"
)

st.info(
    "現在は、まず基礎的な空欄補充問題で"
    "学習の流れを検証しています。"
    "選択問題・語句整序・英作文は今後段階的に追加します。"
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


# 問題形式表示
if question["question_type"] == "fill_blank":

    st.caption(
        "問題形式：空欄補充"
    )

elif question["question_type"] == "choice":

    st.caption(
        "問題形式：選択問題"
    )


st.info(
    question["question"]
)


# 日本語訳を学習者に見せるかどうかは
# 今後の教育設計で検討する。
#
# 現段階では、問題理解のために表示する。
#

if question.get(
    "japanese"
):

    st.caption(
        f"日本語："
        f"{question['japanese']}"
    )


# =========================================================
# 回答入力
# =========================================================


with st.form(
    "answer_form"
):

    # -----------------------------------------------------
    # 空欄補充
    # -----------------------------------------------------

    if question[
        "question_type"
    ] == "fill_blank":

        user_answer = st.text_input(
            "空欄に入る語を入力してください",
            placeholder="英語を入力してください",
        )

    # -----------------------------------------------------
    # 選択問題
    # -----------------------------------------------------

    elif question[
        "question_type"
    ] == "choice":

        st.markdown(
            "#### 選択肢"
        )

        st.markdown(
            format_choices(
                question
            )
        )

        user_answer = st.text_input(
            "答えを入力してください",
            placeholder=(
                "例：ア"
            ),
        )

        st.caption(
            "選択肢の記号（ア・イ・ウ・エ）"
            "で答えても構いません。"
        )

    else:

        st.error(
            "未対応の問題形式です。"
        )

        user_answer = ""

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
            "回答を入力してください。"
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
            "🔴 もう一度確認しましょう。"
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

    if not result.get(
        "is_correct",
        False,
    ):

        st.markdown(
            "### 📖 正解"
        )

        st.code(
            question.get(
                "answer",
                "",
            )
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

                status = "🔴 要復習"

            st.markdown(
                f"**第{question_number}問** "
                f"{status}"
            )

            st.caption(
                f"問題形式："
                f"{record.get('question_type', '')}"
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
                f"正解：\n"
                f"{record.get('correct_answer', '')}"
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
        f"有効な問題数："
        f"{len(get_enabled_questions())}"
    )

    st.write(
        f"登録問題総数："
        f"{len(QUESTION_BANK)}"
    )

    st.write(
        f"学習目標数："
        f"{len(LEARNING_OBJECTIVES)}"
    )

    st.write(
        "AI問題生成：現在は使用しない"
    )

    st.write(
        "AI採点：現在は使用しない"
    )

    st.write(
        "問題選択：ルールベース"
    )

    st.write(
        "回答判定：Python"
    )

    st.write(
        "学習履歴："
        "Streamlitセッション＋JSON"
    )

    st.write(
        "選択問題の回答："
        "ア・イ・ウ・エの記号に対応"
    )
