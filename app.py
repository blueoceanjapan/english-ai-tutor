import json
from datetime import datetime

import streamlit as st


# =========================================================
# 基本設定
# =========================================================

st.set_page_config(
    page_title="中2英語 個別学習支援ドリル",
    page_icon="📚",
    layout="centered",
)

APP_VERSION = "1.6.0-beta2"
STATE_VERSION = 8
QUESTIONS_PER_BATCH = 5

CHOICE_LABELS = ["ア", "イ", "ウ", "エ"]

MAJOR_QUESTION_INSTRUCTION = (
    "次の日本文に合うように、（　）にもっとも適するものを"
    "ア～エから1つ選び、記号で答えなさい。"
)

LEARNING_OBJECTIVES = {
    "gerund_basic": {
        "name": "動名詞の基本",
        "description": "動詞に -ing を付けて、動名詞として使える。",
    },
    "like_gerund": {
        "name": "like + 動名詞",
        "description": "like の後ろに動名詞を使える。",
    },
    "enjoy_gerund": {
        "name": "enjoy + 動名詞",
        "description": "enjoy の後ろに動名詞を使える。",
    },
    "finish_gerund": {
        "name": "finish + 動名詞",
        "description": "finish の後ろに動名詞を使える。",
    },
}


# =========================================================
# 問題データ
# =========================================================

QUESTION_BANK = [{'id': 'gerund_l1_001',
  'major_question': 1,
  'question_number': 1,
  'question_type': 'japanese_to_english_choice',
  'objective': 'gerund_basic',
  'difficulty': 1,
  'japanese': '泳ぐことは楽しいです。',
  'english': '（\u3000\u3000\u3000）is fun.',
  'options': [{'label': 'ア', 'value': 'Swim', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'Swimming', 'error_type': 'none'},
              {'label': 'ウ', 'value': 'Swims', 'error_type': 'third_person'},
              {'label': 'エ', 'value': 'Swam', 'error_type': 'past_form'}],
  'answer': 'イ',
  'explanation': '「泳ぐこと」を表す動名詞は、swim に -ing を付けた swimming です。',
  'level': 1,
  'level_name': 'レベル1：動名詞の基本習得'},
 {'id': 'gerund_l1_002',
  'major_question': 1,
  'question_number': 2,
  'question_type': 'japanese_to_english_choice',
  'objective': 'like_gerund',
  'difficulty': 1,
  'japanese': '私はテニスをすることが好きです。',
  'english': 'I like（\u3000\u3000\u3000）tennis.',
  'options': [{'label': 'ア', 'value': 'playing', 'error_type': 'none'},
              {'label': 'イ', 'value': 'play', 'error_type': 'base_form'},
              {'label': 'ウ', 'value': 'played', 'error_type': 'past_form'},
              {'label': 'エ', 'value': 'plays', 'error_type': 'third_person'}],
  'answer': 'ア',
  'explanation': '「テニスをすること」が好きです、と書いてあるので、「～すること」を表すために play に -ing を付け、playing とします。',
  'level': 1,
  'level_name': 'レベル1：動名詞の基本習得'},
 {'id': 'gerund_l1_003',
  'major_question': 1,
  'question_number': 3,
  'question_type': 'japanese_to_english_choice',
  'objective': 'like_gerund',
  'difficulty': 1,
  'japanese': '私は音楽を聴くことが好きです。',
  'english': 'I like（\u3000\u3000\u3000）to music.',
  'options': [{'label': 'ア', 'value': 'listen', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'listened', 'error_type': 'past_form'},
              {'label': 'ウ', 'value': 'listening', 'error_type': 'none'},
              {'label': 'エ', 'value': 'listens', 'error_type': 'third_person'}],
  'answer': 'ウ',
  'explanation': '「音楽を聴くこと」が好きです、と書いてあるので、「～すること」を表すために listen に -ing を付け、listening とします。',
  'level': 1,
  'level_name': 'レベル1：動名詞の基本習得'},
 {'id': 'gerund_l1_004',
  'major_question': 1,
  'question_number': 4,
  'question_type': 'japanese_to_english_choice',
  'objective': 'enjoy_gerund',
  'difficulty': 1,
  'japanese': '私は英語を勉強することを楽しんでいます。',
  'english': 'I enjoy（\u3000\u3000\u3000）English.',
  'options': [{'label': 'ア', 'value': 'study', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'studying', 'error_type': 'none'},
              {'label': 'ウ', 'value': 'studied', 'error_type': 'past_form'},
              {'label': 'エ', 'value': 'studies', 'error_type': 'third_person'}],
  'answer': 'イ',
  'explanation': '「英語を勉強すること」を楽しんでいます、と書いてあるので、「～すること」を表すために study に -ing を付け、studying とします。',
  'level': 1,
  'level_name': 'レベル1：動名詞の基本習得'},
 {'id': 'gerund_l1_005',
  'major_question': 1,
  'question_number': 5,
  'question_type': 'japanese_to_english_choice',
  'objective': 'finish_gerund',
  'difficulty': 1,
  'japanese': '私は宿題をすることを終えました。',
  'english': 'I finished（\u3000\u3000\u3000）my homework.',
  'options': [{'label': 'ア', 'value': 'do', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'did', 'error_type': 'past_form'},
              {'label': 'ウ', 'value': 'does', 'error_type': 'third_person'},
              {'label': 'エ', 'value': 'doing', 'error_type': 'none'}],
  'answer': 'エ',
  'explanation': '「宿題をすることを終えました」と書いてあるので、「～すること」を表すために do に -ing を付け、doing とします。',
  'level': 1,
  'level_name': 'レベル1：動名詞の基本習得'},
 {'id': 'gerund_l2_001',
  'major_question': 2,
  'question_number': 6,
  'level': 2,
  'level_name': 'レベル2：意味からの活用',
  'question_type': 'japanese_to_english_choice',
  'objective': 'like_gerund',
  'difficulty': 2,
  'japanese': '私は水泳が好きです。',
  'english': 'I like（\u3000\u3000\u3000）.',
  'options': [{'label': 'ア', 'value': 'swim', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'swimming', 'error_type': 'none'},
              {'label': 'ウ', 'value': 'swam', 'error_type': 'past_form'},
              {'label': 'エ', 'value': 'swims', 'error_type': 'third_person'}],
  'answer': 'イ',
  'explanation': '「水泳が好きです」は、「泳ぐことが好きです」という意味です。「泳ぐこと」を表すため、swim に -ing を付けて swimming とします。'},
 {'id': 'gerund_l2_002',
  'major_question': 2,
  'question_number': 7,
  'level': 2,
  'level_name': 'レベル2：意味からの活用',
  'question_type': 'japanese_to_english_choice',
  'objective': 'like_gerund',
  'difficulty': 2,
  'japanese': '彼は料理が好きです。',
  'english': 'He likes（\u3000\u3000\u3000）.',
  'options': [{'label': 'ア', 'value': 'cook', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'cooking', 'error_type': 'none'},
              {'label': 'ウ', 'value': 'cooked', 'error_type': 'past_form'},
              {'label': 'エ', 'value': 'cooks', 'error_type': 'third_person'}],
  'answer': 'イ',
  'explanation': '「料理が好きです」は、「料理をすることが好きです」という意味です。「すること」を表すため、cook に -ing を付けて cooking とします。'},
 {'id': 'gerund_l2_003',
  'major_question': 2,
  'question_number': 8,
  'level': 2,
  'level_name': 'レベル2：意味からの活用',
  'question_type': 'japanese_to_english_choice',
  'objective': 'enjoy_gerund',
  'difficulty': 2,
  'japanese': '私は料理を楽しんでいます。',
  'english': 'I enjoy（\u3000\u3000\u3000）.',
  'options': [{'label': 'ア', 'value': 'cook', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'cooking', 'error_type': 'none'},
              {'label': 'ウ', 'value': 'cooked', 'error_type': 'past_form'},
              {'label': 'エ', 'value': 'cooks', 'error_type': 'third_person'}],
  'answer': 'イ',
  'explanation': '「料理を楽しんでいます」は、「料理をすることを楽しんでいます」という意味です。「すること」を表すため、cook に -ing を付けて cooking '
                 'とします。'},
 {'id': 'gerund_l2_004',
  'major_question': 2,
  'question_number': 9,
  'level': 2,
  'level_name': 'レベル2：意味からの活用',
  'question_type': 'japanese_to_english_choice',
  'objective': 'finish_gerund',
  'difficulty': 2,
  'japanese': '私は宿題を終えました。',
  'english': 'I finished（\u3000\u3000\u3000）my homework.',
  'options': [{'label': 'ア', 'value': 'do', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'doing', 'error_type': 'none'},
              {'label': 'ウ', 'value': 'did', 'error_type': 'past_form'},
              {'label': 'エ', 'value': 'does', 'error_type': 'third_person'}],
  'answer': 'イ',
  'explanation': '「宿題を終えました」は、「宿題をすることを終えました」という意味です。「すること」を表すため、do に -ing を付けて doing とします。'},
 {'id': 'gerund_l2_005',
  'major_question': 2,
  'question_number': 10,
  'level': 2,
  'level_name': 'レベル2：意味からの活用',
  'question_type': 'japanese_to_english_choice',
  'objective': 'gerund_basic',
  'difficulty': 2,
  'japanese': '英語の勉強は大切です。',
  'english': '（\u3000\u3000\u3000）English is important.',
  'options': [{'label': 'ア', 'value': 'Study', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'Studying', 'error_type': 'none'},
              {'label': 'ウ', 'value': 'Studied', 'error_type': 'past_form'},
              {'label': 'エ', 'value': 'Studies', 'error_type': 'third_person'}],
  'answer': 'イ',
  'explanation': '「英語の勉強」は、「英語を勉強すること」という意味です。「勉強すること」を文の主語にするため、study に -ing を付けて Studying とします。'},
 {'id': 'gerund_l3_001',
  'major_question': 3,
  'question_number': 11,
  'level': 3,
  'level_name': 'レベル3：ルールの使い分け・干渉',
  'question_type': 'japanese_to_english_choice',
  'objective': 'like_gerund',
  'difficulty': 3,
  'japanese': '彼女は本を読むことが好きです。',
  'english': 'She likes（\u3000\u3000\u3000）books.',
  'options': [{'label': 'ア', 'value': 'reading', 'error_type': 'none'},
              {'label': 'イ', 'value': 'read', 'error_type': 'base_form'},
              {'label': 'ウ', 'value': 'reads', 'error_type': 'third_person'},
              {'label': 'エ', 'value': 'readed', 'error_type': 'other'}],
  'answer': 'ア',
  'explanation': '「本を読むこと」が好きなので、read に -ing を付けて reading とします。She '
                 'は三人称単数ですが、三単現のSを付けるのは主語のあとにある動詞です。ここでは likes '
                 'がすでに三単現の形になっているので、空欄では三単現のSではなく、「～すること」を表す動名詞の形に集中します。'},
 {'id': 'gerund_l3_002',
  'major_question': 3,
  'question_number': 12,
  'level': 3,
  'level_name': 'レベル3：ルールの使い分け・干渉',
  'question_type': 'japanese_to_english_choice',
  'objective': 'finish_gerund',
  'difficulty': 3,
  'japanese': '彼女は昼食を食べ終えました。',
  'english': 'She finished（\u3000\u3000\u3000）lunch.',
  'options': [{'label': 'ア', 'value': 'eating', 'error_type': 'none'},
              {'label': 'イ', 'value': 'eat', 'error_type': 'base_form'},
              {'label': 'ウ', 'value': 'eats', 'error_type': 'third_person'},
              {'label': 'エ', 'value': 'ate', 'error_type': 'past_form'}],
  'answer': 'ア',
  'explanation': '「昼食を食べることを終えました」という意味なので、eat に -ing を付けて eating とします。finished '
                 'はすでに過去形になっているので、空欄の動詞まで過去形にする必要はありません。ここでは finished の時制ではなく、finish '
                 'の後ろで「～すること」を表す形に注目します。'},
 {'id': 'gerund_l3_003',
  'major_question': 3,
  'question_number': 13,
  'level': 3,
  'level_name': 'レベル3：ルールの使い分け・干渉',
  'question_type': 'japanese_to_english_choice',
  'objective': 'enjoy_gerund',
  'difficulty': 3,
  'japanese': '彼はギターを弾くことを楽しんでいます。',
  'english': 'He enjoys（\u3000\u3000\u3000）the guitar.',
  'options': [{'label': 'ア', 'value': 'play', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'played', 'error_type': 'past_form'},
              {'label': 'ウ', 'value': 'plays', 'error_type': 'third_person'},
              {'label': 'エ', 'value': 'playing', 'error_type': 'none'}],
  'answer': 'エ',
  'explanation': '「ギターを弾くこと」を楽しんでいるので、play に -ing を付けて playing とします。He は三人称単数ですが、三単現のSは enjoys '
                 'がすでに処理しています。そのため空欄では plays ではなく、動名詞 playing を選びます。'},
 {'id': 'gerund_l3_004',
  'major_question': 3,
  'question_number': 14,
  'level': 3,
  'level_name': 'レベル3：ルールの使い分け・干渉',
  'question_type': 'japanese_to_english_choice',
  'objective': 'like_gerund',
  'difficulty': 3,
  'japanese': '彼女はテニスをすることが好きです。',
  'english': 'She likes（\u3000\u3000\u3000）tennis.',
  'options': [{'label': 'ア', 'value': 'play', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'playing', 'error_type': 'none'},
              {'label': 'ウ', 'value': 'plays', 'error_type': 'third_person'},
              {'label': 'エ', 'value': 'played', 'error_type': 'past_form'}],
  'answer': 'イ',
  'explanation': '「テニスをすること」が好きなので、play に -ing を付けて playing とします。likes '
                 'がすでに三単現の形なので、空欄では三単現のSを考えるのではなく、「～すること」を表す動名詞の形に集中します。'},
 {'id': 'gerund_l3_005',
  'major_question': 3,
  'question_number': 15,
  'level': 3,
  'level_name': 'レベル3：ルールの使い分け・干渉',
  'question_type': 'japanese_to_english_choice',
  'objective': 'finish_gerund',
  'difficulty': 3,
  'japanese': '彼は宿題をすることを終えました。',
  'english': 'He finished（\u3000\u3000\u3000）his homework.',
  'options': [{'label': 'ア', 'value': 'do', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'did', 'error_type': 'past_form'},
              {'label': 'ウ', 'value': 'does', 'error_type': 'third_person'},
              {'label': 'エ', 'value': 'doing', 'error_type': 'none'}],
  'answer': 'エ',
  'explanation': '「宿題をすることを終えました」なので、do に -ing を付けて doing とします。He は三人称単数ですが、三単現のSはここでは考えません。また '
                 'finished がすでに過去形なので、空欄を did にする必要もありません。空欄では、finish の後ろに置く「～すること」の形に集中します。'}]
# =========================================================

def initialize_state():

    if st.session_state.get(
        "state_version"
    ) != STATE_VERSION:

        st.session_state.state_version = (
            STATE_VERSION
        )

        st.session_state.batch_number = 0

        st.session_state.history = []

        st.session_state.batch_results = None

        st.session_state.batch_submitted = False

        st.session_state.student_name = ""
        st.session_state.current_level = 1
        st.session_state.level_batch_number = 0

        return

    st.session_state.setdefault(
        "batch_number",
        0,
    )

    st.session_state.setdefault(
        "history",
        [],
    )

    st.session_state.setdefault(
        "batch_results",
        None,
    )

    st.session_state.setdefault(
        "batch_submitted",
        False,
    )

    st.session_state.setdefault(
        "student_name",
        "",
    )

    st.session_state.setdefault(
        "current_level",
        1,
    )

    st.session_state.setdefault(
        "level_batch_number",
        0,
    )


initialize_state()


# =========================================================
# ページ先頭へのスクロール
# =========================================================
#
# st.rerun() だけでは、ブラウザのスクロール位置は
# 必ずしもページ先頭へ移動しません。
#
# そこで、JavaScriptを実行できるHTMLコンポーネントから
# Streamlit本体のスクロール領域を直接先頭へ移動します。
# width をバッチ番号に応じて変えることで、
# 「次の5問へ」を押すたびにコンポーネントを再実行します。
# =========================================================

if st.session_state.get(
    "scroll_to_top",
    False,
):

    import streamlit.components.v1 as components

    scroll_component_width = (
        1
        + (
            st.session_state.batch_number
            % 2
        )
    )

    components.html(
        """
        <script>
        (function () {
            function scrollToTop() {
                try {
                    const parentDocument = window.parent.document;

                    const main =
                        parentDocument.querySelector('section.main') ||
                        parentDocument.querySelector('[data-testid="stMain"]') ||
                        parentDocument.querySelector('[data-testid="stAppViewMain"]');

                    if (main) {
                        main.scrollTop = 0;
                        if (typeof main.scrollTo === 'function') {
                            main.scrollTo({
                                top: 0,
                                left: 0,
                                behavior: 'auto'
                            });
                        }
                    }

                    if (parentDocument.scrollingElement) {
                        parentDocument.scrollingElement.scrollTop = 0;
                    }

                    parentDocument.documentElement.scrollTop = 0;
                    parentDocument.body.scrollTop = 0;
                    window.parent.scrollTo(0, 0);
                } catch (e) {
                    try {
                        window.parent.scrollTo(0, 0);
                    } catch (_) {
                        // Ignore browser-specific scroll errors.
                    }
                }
            }

            // Streamlitが再描画を完了した後にも実行するため、
            // 少し間隔を空けて複数回実行します。
            setTimeout(scrollToTop, 0);
            setTimeout(scrollToTop, 100);
            setTimeout(scrollToTop, 300);
            setTimeout(scrollToTop, 700);
        })();
        </script>
        """,
        width=scroll_component_width,
        height=1,
        scrolling=False,
    )

    st.session_state.scroll_to_top = False


# =========================================================
# 問題・選択肢関連
# =========================================================

def get_questions_for_batch(
    batch_number,
):

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


def get_option_by_label(
    question,
    label,
):

    for option in question[
        "options"
    ]:

        if option[
            "label"
        ] == label:

            return option

    return None


def check_answer(
    question,
    user_answer,
):

    user_answer = str(
        user_answer
    ).strip()

    correct_label = question[
        "answer"
    ]

    if not user_answer:

        return {
            "is_correct": False,
            "judgement": "未回答",
            "mistake_type": "unanswered",
            "feedback": (
                "この問題には回答がありません。"
            ),
        }

    if user_answer == correct_label:

        return {
            "is_correct": True,
            "judgement": "正解",
            "mistake_type": "none",
            "feedback": (
                "正解です。\n\n"
                + question[
                    "explanation"
                ]
            ),
        }

    option = get_option_by_label(
        question,
        user_answer,
    )

    if option:

        mistake_type = option.get(
            "error_type",
            "other",
        )

    else:

        mistake_type = (
            "invalid_answer"
        )

    return {
        "is_correct": False,
        "judgement": "不正解",
        "mistake_type": mistake_type,
        "feedback": (
            "今回は正解ではありません。\n\n"
            + question[
                "explanation"
            ]
        ),
    }


def evaluate_batch(
    questions,
    answers,
):

    results = []

    for question in questions:

        user_answer = answers.get(
            question["id"],
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
# 履歴関連
# =========================================================

def create_history_record(
    question,
    user_answer,
    result,
):

    objective_id = question[
        "objective"
    ]

    objective = (
        LEARNING_OBJECTIVES[
            objective_id
        ]
    )

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

        "level": question.get("level", ""),
        "level_name": question.get("level_name", ""),

        "japanese": question[
            "japanese"
        ],

        "english": question[
            "english"
        ],

        "user_answer": user_answer,

        "user_answer_value": (
            selected_option[
                "value"
            ]
            if selected_option
            else ""
        ),

        "correct_answer": question[
            "answer"
        ],

        "correct_value": (
            correct_option[
                "value"
            ]
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
# ★ 詳細履歴の並び順
# =========================================================
#
# ここが今回の重要な修正です。
#
# history の保存順には依存しません。
#
# まずセット番号で並べ、
# 同じセットの中では小問番号で並べます。
#
# したがって、
#
# 第1問
# 第2問
# 第3問
# 第4問
# 第5問
#
# の順で必ず表示されます。
#
# =========================================================

def history_sort_key(
    record,
):

    try:

        batch_number = int(
            record.get(
                "batch_number",
                0,
            )
        )

    except (
        TypeError,
        ValueError,
    ):

        batch_number = 0

    try:

        question_number = int(
            record.get(
                "question_number",
                0,
            )
        )

    except (
        TypeError,
        ValueError,
    ):

        question_number = 0

    return (
        batch_number,
        question_number,
    )


def get_sorted_history():

    return sorted(
        st.session_state.history,
        key=history_sort_key,
    )


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
        if total
        else 0
    )

    return {
        "total": total,
        "correct": correct,
        "accuracy": accuracy,
    }


def calculate_objective_stats():

    stats = {
        objective_id: {
            "name": objective[
                "name"
            ],
            "total": 0,
            "correct": 0,
            "accuracy": 0.0,
        }

        for (
            objective_id,
            objective,
        ) in LEARNING_OBJECTIVES.items()
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

    for stat in stats.values():

        if stat["total"]:

            stat["accuracy"] = (
                stat["correct"]
                / stat["total"]
                * 100
            )

    return stats


def calculate_batch_mistake_stats(
    batch_results,
):

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


def create_session_copy_text(
    records,
):

    if not records:
        return ""

    records = sorted(
        records,
        key=history_sort_key,
    )

    total = len(records)
    correct = sum(
        1
        for record in records
        if record.get("is_correct", False)
    )
    accuracy = (
        correct / total * 100
        if total
        else 0
    )

    mistake_labels = {
        "base_form": "原形を選択",
        "past_form": "過去形を選択",
        "third_person": "三単現の形を選択",
        "other": "その他",
        "invalid_answer": "無効な回答",
        "unanswered": "未回答",
    }

    mistake_counts = {}
    objective_counts = {}

    for record in records:
        objective_name = record.get(
            "objective_name",
            record.get("objective", ""),
        )

        if objective_name:
            if objective_name not in objective_counts:
                objective_counts[objective_name] = {
                    "total": 0,
                    "correct": 0,
                }

            objective_counts[objective_name]["total"] += 1

            if record.get("is_correct", False):
                objective_counts[objective_name]["correct"] += 1

        if record.get("is_correct", False):
            continue

        mistake_type = record.get(
            "mistake_type",
            "other",
        )
        mistake_counts[mistake_type] = (
            mistake_counts.get(mistake_type, 0) + 1
        )

    first_timestamp = records[0].get("timestamp", "")
    last_timestamp = records[-1].get("timestamp", "")

    lines = [
        "【中2英語 個別学習支援ドリル｜現在の学習セッション結果】",
        "※現在のStreamlitセッション内で記録された全問題を対象としています。",
        f"実施開始時刻（記録上）：{first_timestamp}",
        f"直近記録時刻（記録上）：{last_timestamp}",
        f"問題数：{total}問",
        f"正解：{correct}問",
        f"正答率：{accuracy:.1f}%",
        "",
        "【学習項目別の結果】",
    ]

    if not objective_counts:
        lines.append("データなし")
    else:
        for objective_name, stat in objective_counts.items():
            objective_accuracy = (
                stat["correct"] / stat["total"] * 100
                if stat["total"]
                else 0
            )
            lines.append(
                f"- {objective_name}："
                f"{stat['correct']}/{stat['total']}問正解 "
                f"（{objective_accuracy:.1f}%）"
            )

    lines.extend([
        "",
        "【問題・解答・分析材料】",
    ])

    for record in records:
        is_correct = record.get("is_correct", False)
        judgement = record.get(
            "judgement",
            "",
        )
        mistake_type = record.get(
            "mistake_type",
            "",
        )
        mistake_label = mistake_labels.get(
            mistake_type,
            mistake_type,
        )

        lines.extend([
            "",
            f"第{record.get('question_number', '')}問",
            f"セット：{record.get('batch_number', '')}",
            f"問題ID：{record.get('question_id', '')}",
            f"学習項目：{record.get('objective_name', '')}",
            f"難易度：{record.get('difficulty', '')}",
            f"日本語：{record.get('japanese', '')}",
            f"英文：{record.get('english', '')}",
            f"選択した答え：{record.get('user_answer', '')}．{record.get('user_answer_value', '')}",
            f"正解：{record.get('correct_answer', '')}．{record.get('correct_value', '')}",
            f"判定：{judgement}",
            f"誤答タイプ：{mistake_label}",
            f"フィードバック：{record.get('feedback', '')}",
        ])

    lines.extend([
        "",
        "【セッション全体の誤答内訳】",
    ])

    if not mistake_counts:
        lines.append("誤答なし")
    else:
        for mistake_type, count in sorted(
            mistake_counts.items(),
            key=lambda item: item[1],
            reverse=True,
        ):
            lines.append(
                f"- {mistake_labels.get(mistake_type, mistake_type)}：{count}問"
            )

    lines.extend([
        "",
        "【分析上の注意】",
        "このデータは現在のStreamlitセッション内の学習結果をまとめたものです。",
        "誤答タイプは選択肢に設定された機械的な分類であり、根本原因の診断ではありません。",
        "複数セッションのデータがない段階では、恒常的な学習上の弱点や根本原因を断定しません。",
    ])

    return "\n".join(lines)


# =========================================================
# JSON保存・復元
# =========================================================

def create_export_data():

    return json.dumps(
        {
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
        },

        ensure_ascii=False,

        indent=2,
    )


def import_history(
    uploaded_file,
):

    raw = uploaded_file.read()

    data = json.loads(
        raw.decode("utf-8")
    )

    if not isinstance(
        data.get("history"),
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
    ) is not None:

        st.session_state.student_name = (
            data["student_name"]
        )

    st.session_state.batch_results = (
        None
    )

    st.session_state.batch_submitted = (
        False
    )


# =========================================================
# 現在の問題
# =========================================================

current_level = st.session_state.get("current_level", 1)
current_level_questions = [q for q in QUESTION_BANK if q.get("level") == current_level]
level_offset = st.session_state.get("level_batch_number", 0) * QUESTIONS_PER_BATCH
current_questions = current_level_questions[level_offset:level_offset + QUESTIONS_PER_BATCH]


# =========================================================
# タイトル
# =========================================================

st.title(
    "📚 中2英語 個別学習支援ドリル"
)

st.caption(
    f"仮バージョン｜レベル{current_level}：{current_questions[0]['level_name']}"
)

st.info(
    "各レベルは5問を1セットとして実施します。"
    "この仮バージョンでは、各レベルで5問すべて正解した場合のみ次のレベルへ進みます。"
)


# =========================================================
# 学習者
# =========================================================

st.markdown(
    "### 👤 学習者"
)

st.session_state.student_name = (
    st.text_input(
        "名前または識別用の名前",
        value=(
            st.session_state.student_name
        ),
    )
)


# =========================================================
# 学習目標
# =========================================================

st.markdown("---")

st.markdown(
    "## 🎯 今回の学習目標"
)

level_goals = {
    1: ("動名詞の基本を習得する", "日本語に「～すること」を明示し、動名詞の基本的な形を確認します。"),
    2: ("習得した動名詞を意味から活用する", "日本語に「～すること」を明示せず、意味から動名詞を選べるか確認します。"),
    3: ("既習ルールの干渉があっても動名詞を選択する", "三人称単数や過去形などの干渉条件を置き、必要なルールを使い分けられるか確認します。"),
}
goal_title, goal_description = level_goals[current_level]
st.write(f"**{goal_title}**")
st.caption(goal_description)


# =========================================================
# 大問1
# =========================================================

st.markdown("---")

st.markdown(
    f"## 📄 レベル{current_level}・第{st.session_state.get('level_batch_number', 0) + 1}セット"
)

st.info(
    MAJOR_QUESTION_INSTRUCTION
)


# =========================================================
# 5問回答
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

        global_question_number = question[
            "question_number"
        ]

        st.markdown(
            f"### 第{global_question_number}問"
        )

        st.write(
            f"**{question['japanese']}**"
        )

        st.info(
            question["english"]
        )

        option_map = {
            option["label"]: option[
                "value"
            ]

            for option
            in question["options"]
        }

        selected_label = st.radio(
            "答えを選んでください",

            options=CHOICE_LABELS,

            format_func=(
                lambda label,
                option_map=option_map:
                f"{label}．"
                f"{option_map.get(label, '')}"
            ),

            key=(
                f"choice_"
                f"{st.session_state.batch_number}_"
                f"{question['id']}"
            ),

            index=None,
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

    submit_batch = (
        st.form_submit_button(
            "5問をまとめて採点する 📝",
            type="primary",
        )
    )


# =========================================================
# 採点処理
# =========================================================

if submit_batch:

    batch_results = (
        evaluate_batch(
            current_questions,
            selected_answers,
        )
    )

    st.session_state.batch_results = (
        batch_results
    )

    st.session_state.batch_submitted = (
        True
    )

    for item in batch_results:

        st.session_state.history.append(
            create_history_record(
                item["question"],
                item["user_answer"],
                item["result"],
            )
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
        if batch_total
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

        if result.get(
            "is_correct",
            False,
        ):

            st.success(
                f"{question['question_number']}. "
                f"🟢 正解"
            )

        elif result.get(
            "mistake_type"
        ) == "unanswered":

            st.warning(
                f"{question['question_number']}. "
                f"⚪ 未回答"
            )

        else:

            st.error(
                f"{question['question_number']}. "
                f"🔴 不正解"
            )

        st.markdown(
            f"**日本語：** "
            f"{question['japanese']}"
        )

        st.markdown(
            f"**英文：** "
            f"{question['english']}"
        )

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
                "あなたの答え：**未回答**"
            )

        correct_option = (
            get_option_by_label(
                question,
                question["answer"],
            )
        )

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
            "base_form": "原形を選択",
            "past_form": "過去形を選択",
            "third_person": "三単現の形を選択",
            "other": "その他",
            "invalid_answer": "無効な回答",
            "unanswered": "未回答",
        }

        for (
            mistake_type,
            count,
        ) in sorted(
            batch_mistakes.items(),
            key=lambda item: item[1],
            reverse=True,
        ):

            st.write(
                f"- "
                f"{mistake_labels.get(mistake_type, mistake_type)}："
                f"{count}問"
            )


    # =====================================================
    # レベル進行
    # =====================================================

    batch_is_perfect = (
        batch_correct == batch_total
        and batch_total == QUESTIONS_PER_BATCH
    )

    st.markdown("---")

    if batch_is_perfect:
        st.success(f"レベル{current_level}のこのセットは満点です。")
        if current_level < 3:
            if st.button(f"レベル{current_level + 1}へ進む ➡️", type="primary"):
                st.session_state.current_level = current_level + 1
                st.session_state.level_batch_number = 0
                st.session_state.batch_results = None
                st.session_state.batch_submitted = False
                st.session_state.batch_number += 1
                st.session_state.scroll_to_top = True
                st.rerun()
        else:
            st.success("レベル3で満点を達成しました。この仮バージョンでは、習得した知識を干渉条件のある問題でも活用できたと記録します。")
    else:
        st.warning(f"レベル{current_level}は満点ではありません。次のレベルへは進みません。")
        next_offset = (st.session_state.get("level_batch_number", 0) + 1) * QUESTIONS_PER_BATCH
        if next_offset < len(current_level_questions):
            if st.button("同じレベルの次セットへ ➡️", type="primary"):
                st.session_state.level_batch_number += 1
                st.session_state.batch_number += 1
                st.session_state.batch_results = None
                st.session_state.batch_submitted = False
                st.session_state.scroll_to_top = True
                st.rerun()
        else:
            st.info("この仮バージョンでは、未達時の類題自動生成はまだ実装していません。")


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


# =========================================================
# 詳細な学習履歴
# =========================================================

if st.session_state.history:

    with st.expander(
        "📝 詳細な学習履歴"
    ):

        # -------------------------------------------------
        # 重要：
        # 保存された順番ではなく、
        # セット番号 → 小問番号の順に並べ替える。
        #
        # ここで「reversed()」は使用しない。
        # -------------------------------------------------

        sorted_history = (
            get_sorted_history()
        )

        for record in sorted_history:

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

            st.markdown(
                f"**日本語：** "
                f"{record.get('japanese', '')}"
            )

            st.markdown(
                f"**英文：** "
                f"{record.get('english', '')}"
            )

            user_answer = record.get(
                "user_answer",
                "",
            )

            user_answer_value = record.get(
                "user_answer_value",
                "",
            )

            if (
                user_answer
                and user_answer_value
            ):

                st.write(
                    f"あなたの答え："
                    f"**{user_answer}．"
                    f"{user_answer_value}**"
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
# 開発者向け：直近セッション結果のコピー
# =========================================================

if st.session_state.history:

    with st.expander(
        "🧪 開発者向け：学習セッション結果をコピー",
        expanded=False,
    ):

        current_session_records = get_sorted_history()

        st.caption(
            "現在のStreamlitセッション内で記録された全問題をまとめます。"
            "5問ごとのセットではなく、10問なら10問分を一括で取得できます。"
            "下のコード欄のコピー機能で、このチャットへ貼り付けてください。"
        )

        session_copy_text = create_session_copy_text(
            current_session_records
        )

        st.code(
            session_copy_text,
            language="text",
        )


# =========================================================
# JSON保存
# =========================================================

if st.session_state.history:

    st.download_button(
        label="📥 学習履歴を保存",

        data=create_export_data(),

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

    st.write("レベル構成：レベル1・レベル2・レベル3")
    st.write("進級条件：各レベルの1セット5問すべて正解")

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
