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

APP_VERSION = "1.5.1"
STATE_VERSION = 7
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

QUESTION_BANK = [
    {
        "id": "gerund_001",
        "major_question": 1,
        "question_number": 1,
        "question_type": "japanese_to_english_choice",
        "objective": "gerund_basic",
        "difficulty": 1,
        "japanese": "泳ぐことは楽しいです。",
        "english": "（　　　）is fun.",
        "options": [
            {"label": "ア", "value": "Swim", "error_type": "base_form"},
            {"label": "イ", "value": "Swimming", "error_type": "none"},
            {"label": "ウ", "value": "Swims", "error_type": "third_person"},
            {"label": "エ", "value": "Swam", "error_type": "past_form"},
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
        "japanese": "私はテニスをすることが好きです。",
        "english": "I like（　　　）tennis.",
        "options": [
            {"label": "ア", "value": "playing", "error_type": "none"},
            {"label": "イ", "value": "play", "error_type": "base_form"},
            {"label": "ウ", "value": "played", "error_type": "past_form"},
            {"label": "エ", "value": "plays", "error_type": "third_person"},
        ],
        "answer": "ア",
        "explanation": (
            "今回の学習目標では、"
            "like の後ろに動名詞 playing を使います。"
        ),
    },
