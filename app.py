import json
import random
import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

import streamlit as st

JAPAN_TZ = ZoneInfo("Asia/Tokyo")

def now_japan():
    """日本時間の現在日時を返す。"""
    return datetime.now(JAPAN_TZ)


# =========================================================
# 基本設定
# =========================================================

st.set_page_config(
    page_title="中2英語 個別学習支援ドリル",
    page_icon="📚",
    layout="centered",
)

APP_VERSION = "1.6.0-beta24"
STATE_VERSION = 13
QUESTIONS_PER_BATCH = 5

CHOICE_LABELS = ["ア", "イ", "ウ", "エ"]

MAJOR_QUESTION_INSTRUCTION = (
    "次の日本文に合うように、（　）にもっとも適するものを"
    "ア～エから1つ選び、記号で答えなさい。"
)

LEARNING_OBJECTIVES = {
    "japanese_meaning": {
        "name": "動名詞ってなんだろう",
        "description": "日本語の中から「～すること」にあたる部分を見つける。",
    },
    "verb_form_choice": {
        "name": "文に合う動詞の形",
        "description": "文の意味に合う動詞の形を選ぶ。",
    },
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
  'explanation': '「泳ぐこと」が書いてあるので、「～すること」を表すために swim に -ing を付け、Swimming とします。',
  'level': 1,
  'level_name': 'レベル1：動名詞を見つけてみよう'},
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
  'level_name': 'レベル1：動名詞を見つけてみよう'},
 {'id': 'gerund_l1_003',
  'major_question': 1,
  'question_number': 3,
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
  'level_name': 'レベル1：動名詞を見つけてみよう'},
 {'id': 'gerund_l1_004',
  'major_question': 1,
  'question_number': 4,
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
  'level_name': 'レベル1：動名詞を見つけてみよう'},
 {'id': 'gerund_l1_005',
  'major_question': 1,
  'question_number': 5,
  'question_type': 'japanese_to_english_choice',
  'objective': 'like_gerund',
  'difficulty': 1,
  'japanese': '私たちは映画を見ることが好きです。',
  'english': 'We like（\u3000\u3000\u3000）movies.',
  'options': [{'label': 'ア', 'value': 'watch', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'watching', 'error_type': 'none'},
              {'label': 'ウ', 'value': 'watched', 'error_type': 'past_form'},
              {'label': 'エ', 'value': 'watches', 'error_type': 'third_person'}],
  'answer': 'イ',
  'explanation': '「映画を見ること」が好きです、と書いてあるので、「～すること」を表すために watch に -ing を付け、watching とします。',
  'level': 1,
  'level_name': 'レベル1：動名詞を見つけてみよう'},
 {'id': 'gerund_l1_006',
  'major_question': 1,
  'question_number': 6,
  'question_type': 'japanese_to_english_choice',
  'objective': 'finish_gerund',
  'difficulty': 1,
  'japanese': '彼女は昼食を食べることを終えました。',
  'english': 'She finished（\u3000\u3000\u3000）lunch.',
  'options': [{'label': 'ア', 'value': 'eat', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'eating', 'error_type': 'none'},
              {'label': 'ウ', 'value': 'eats', 'error_type': 'third_person'},
              {'label': 'エ', 'value': 'ate', 'error_type': 'past_form'}],
  'answer': 'イ',
  'explanation': '「昼食を食べることを終えました」と書いてあるので、「～すること」を表すために eat に -ing を付け、eating とします。',
  'level': 1,
  'level_name': 'レベル1：動名詞を見つけてみよう'},
 {'id': 'gerund_l1_007',
  'major_question': 1,
  'question_number': 7,
  'question_type': 'japanese_to_english_choice',
  'objective': 'enjoy_gerund',
  'difficulty': 1,
  'japanese': '彼はサッカーをすることを楽しんでいます。',
  'english': 'He enjoys（\u3000\u3000\u3000）soccer.',
  'options': [{'label': 'ア', 'value': 'play', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'played', 'error_type': 'past_form'},
              {'label': 'ウ', 'value': 'playing', 'error_type': 'none'},
              {'label': 'エ', 'value': 'plays', 'error_type': 'third_person'}],
  'answer': 'ウ',
  'explanation': '「サッカーをすること」を楽しんでいるので、「～すること」を表すために play に -ing を付け、playing とします。',
  'level': 1,
  'level_name': 'レベル1：動名詞を見つけてみよう'},
 {'id': 'gerund_l1_008',
  'major_question': 1,
  'question_number': 8,
  'question_type': 'japanese_to_english_choice',
  'objective': 'gerund_basic',
  'difficulty': 1,
  'japanese': '絵を描くことは楽しいです。',
  'english': '（\u3000\u3000\u3000）pictures is fun.',
  'options': [{'label': 'ア', 'value': 'Drawing', 'error_type': 'none'},
              {'label': 'イ', 'value': 'Draw', 'error_type': 'base_form'},
              {'label': 'ウ', 'value': 'Drew', 'error_type': 'past_form'},
              {'label': 'エ', 'value': 'Draws', 'error_type': 'third_person'}],
  'answer': 'ア',
  'explanation': '「絵を描くこと」が書いてあるので、draw に -ing を付けて Drawing とします。',
  'level': 1,
  'level_name': 'レベル1：動名詞を見つけてみよう'},
 {'id': 'gerund_l1_009',
  'major_question': 1,
  'question_number': 9,
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
  'explanation': '「音楽を聴くこと」が好きです、と書いてあるので、listen に -ing を付けて listening とします。',
  'level': 1,
  'level_name': 'レベル1：動名詞を見つけてみよう'},
 {'id': 'gerund_l1_010',
  'major_question': 1,
  'question_number': 10,
  'question_type': 'japanese_to_english_choice',
  'objective': 'finish_gerund',
  'difficulty': 1,
  'japanese': '私は部屋を掃除することを終えました。',
  'english': 'I finished（\u3000\u3000\u3000）my room.',
  'options': [{'label': 'ア', 'value': 'clean', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'cleaned', 'error_type': 'past_form'},
              {'label': 'ウ', 'value': 'cleans', 'error_type': 'third_person'},
              {'label': 'エ', 'value': 'cleaning', 'error_type': 'none'}],
  'answer': 'エ',
  'explanation': '「部屋を掃除することを終えました」と書いてあるので、clean に -ing を付けて cleaning とします。',
  'level': 1,
  'level_name': 'レベル1：動名詞を見つけてみよう'},
 {'id': 'gerund_l1_011',
  'major_question': 1,
  'question_number': 11,
  'question_type': 'japanese_to_english_choice',
  'objective': 'enjoy_gerund',
  'difficulty': 1,
  'japanese': '彼女は歌を歌うことを楽しんでいます。',
  'english': 'She enjoys（\u3000\u3000\u3000）songs.',
  'options': [{'label': 'ア', 'value': 'sing', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'singing', 'error_type': 'none'},
              {'label': 'ウ', 'value': 'sang', 'error_type': 'past_form'},
              {'label': 'エ', 'value': 'sings', 'error_type': 'third_person'}],
  'answer': 'イ',
  'explanation': '「歌を歌うこと」を楽しんでいるので、sing に -ing を付けて singing とします。',
  'level': 1,
  'level_name': 'レベル1：動名詞を見つけてみよう'},
 {'id': 'gerund_l1_012',
  'major_question': 1,
  'question_number': 12,
  'question_type': 'japanese_to_english_choice',
  'objective': 'gerund_basic',
  'difficulty': 1,
  'japanese': 'ギターを弾くことは楽しいです。',
  'english': '（\u3000\u3000\u3000）the guitar is fun.',
  'options': [{'label': 'ア', 'value': 'Play', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'Playing', 'error_type': 'none'},
              {'label': 'ウ', 'value': 'Played', 'error_type': 'past_form'},
              {'label': 'エ', 'value': 'Plays', 'error_type': 'third_person'}],
  'answer': 'イ',
  'explanation': '「ギターを弾くこと」が書いてあるので、play に -ing を付けて Playing とします。',
  'level': 1,
  'level_name': 'レベル1：動名詞を見つけてみよう'},
 {'id': 'gerund_l1_013',
  'major_question': 1,
  'question_number': 13,
  'question_type': 'japanese_to_english_choice',
  'objective': 'finish_gerund',
  'difficulty': 1,
  'japanese': '私は本を読むことを終えました。',
  'english': 'I finished（\u3000\u3000\u3000）the book.',
  'options': [{'label': 'ア', 'value': 'read', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'reads', 'error_type': 'third_person'},
              {'label': 'ウ', 'value': 'reading', 'error_type': 'none'},
              {'label': 'エ', 'value': 'readed', 'error_type': 'other'}],
  'answer': 'ウ',
  'explanation': '「本を読むことを終えました」と書いてあるので、read に -ing を付けて reading とします。',
  'level': 1,
  'level_name': 'レベル1：動名詞を見つけてみよう'},
 {'id': 'gerund_l1_014',
  'major_question': 1,
  'question_number': 14,
  'question_type': 'japanese_to_english_choice',
  'objective': 'like_gerund',
  'difficulty': 1,
  'japanese': '彼女はテニスをすることが好きです。',
  'english': 'She likes（\u3000\u3000\u3000）tennis.',
  'options': [{'label': 'ア', 'value': 'play', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'playing', 'error_type': 'none'},
              {'label': 'ウ', 'value': 'plays', 'error_type': 'third_person'},
              {'label': 'エ', 'value': 'played', 'error_type': 'past_form'}],
  'answer': 'イ',
  'explanation': '「テニスをすること」が好きなので、play に -ing を付けて playing とします。',
  'level': 1,
  'level_name': 'レベル1：動名詞を見つけてみよう'},
 {'id': 'gerund_l1_015',
  'major_question': 1,
  'question_number': 15,
  'question_type': 'japanese_to_english_choice',
  'objective': 'enjoy_gerund',
  'difficulty': 1,
  'japanese': '私たちは本を読むことを楽しんでいます。',
  'english': 'We enjoy（\u3000\u3000\u3000）books.',
  'options': [{'label': 'ア', 'value': 'reading', 'error_type': 'none'},
              {'label': 'イ', 'value': 'read', 'error_type': 'base_form'},
              {'label': 'ウ', 'value': 'reads', 'error_type': 'third_person'},
              {'label': 'エ', 'value': 'readed', 'error_type': 'other'}],
  'answer': 'ア',
  'explanation': '「本を読むこと」を楽しんでいるので、read に -ing を付けて reading とします。',
  'level': 1,
  'level_name': 'レベル1：動名詞を見つけてみよう'},
 {'id': 'gerund_l2_016',
  'major_question': 2,
  'question_number': 16,
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
  'explanation': '「水泳が好きです」は、「泳ぐことが好きです」という意味です。「泳ぐこと」を表すため、swim に -ing を付けて swimming とします。',
  'level': 2,
  'level_name': 'レベル2：動名詞を使ってみよう'},
 {'id': 'gerund_l2_017',
  'major_question': 2,
  'question_number': 17,
  'question_type': 'japanese_to_english_choice',
  'objective': 'enjoy_gerund',
  'difficulty': 2,
  'japanese': '映画鑑賞が好きです。',
  'english': 'I enjoy（\u3000\u3000\u3000）movies.',
  'options': [{'label': 'ア', 'value': 'watch', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'watching', 'error_type': 'none'},
              {'label': 'ウ', 'value': 'watched', 'error_type': 'past_form'},
              {'label': 'エ', 'value': 'watches', 'error_type': 'third_person'}],
  'answer': 'イ',
  'explanation': '「映画鑑賞」は、映画を見る活動を表しています。英語では「見ること」を表すため、watch に -ing を付けて watching とします。',
  'level': 2,
  'level_name': 'レベル2：動名詞を使ってみよう'},
 {'id': 'gerund_l2_018',
  'major_question': 2,
  'question_number': 18,
  'question_type': 'japanese_to_english_choice',
  'objective': 'gerund_basic',
  'difficulty': 2,
  'japanese': '英語の勉強は楽しいです。',
  'english': '（\u3000\u3000\u3000）English is fun.',
  'options': [{'label': 'ア', 'value': 'Study', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'Studying', 'error_type': 'none'},
              {'label': 'ウ', 'value': 'Studied', 'error_type': 'past_form'},
              {'label': 'エ', 'value': 'Studies', 'error_type': 'third_person'}],
  'answer': 'イ',
  'explanation': '「英語の勉強」は、英語を勉強する活動を表しています。「勉強すること」を文の主語にするため、study に -ing を付けて Studying とします。',
  'level': 2,
  'level_name': 'レベル2：動名詞を使ってみよう'},
 {'id': 'gerund_l2_019',
  'major_question': 2,
  'question_number': 19,
  'question_type': 'japanese_to_english_choice',
  'objective': 'finish_gerund',
  'difficulty': 2,
  'japanese': '私は昼食を食べるのを終えました。',
  'english': 'I finished（\u3000\u3000\u3000）lunch.',
  'options': [{'label': 'ア', 'value': 'eat', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'ate', 'error_type': 'past_form'},
              {'label': 'ウ', 'value': 'eating', 'error_type': 'none'},
              {'label': 'エ', 'value': 'eats', 'error_type': 'third_person'}],
  'answer': 'ウ',
  'explanation': '「昼食を食べるのを終えました」は、「昼食を食べることを終えました」という意味です。eat に -ing を付けて eating とします。',
  'level': 2,
  'level_name': 'レベル2：動名詞を使ってみよう'},
 {'id': 'gerund_l2_020',
  'major_question': 2,
  'question_number': 20,
  'question_type': 'japanese_to_english_choice',
  'objective': 'like_gerund',
  'difficulty': 2,
  'japanese': '私は料理が好きです。',
  'english': 'I like（\u3000\u3000\u3000）.',
  'options': [{'label': 'ア', 'value': 'cook', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'cooked', 'error_type': 'past_form'},
              {'label': 'ウ', 'value': 'cooking', 'error_type': 'none'},
              {'label': 'エ', 'value': 'cooks', 'error_type': 'third_person'}],
  'answer': 'ウ',
  'explanation': '「料理が好きです」は、「料理をすることが好きです」という意味です。「すること」を表すため、cook に -ing を付けて cooking とします。',
  'level': 2,
  'level_name': 'レベル2：動名詞を使ってみよう'},
 {'id': 'gerund_l2_021',
  'major_question': 2,
  'question_number': 21,
  'question_type': 'japanese_to_english_choice',
  'objective': 'enjoy_gerund',
  'difficulty': 2,
  'japanese': '音楽鑑賞を楽しんでいます。',
  'english': 'I enjoy（\u3000\u3000\u3000）to music.',
  'options': [{'label': 'ア', 'value': 'listen', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'listening', 'error_type': 'none'},
              {'label': 'ウ', 'value': 'listened', 'error_type': 'past_form'},
              {'label': 'エ', 'value': 'listens', 'error_type': 'third_person'}],
  'answer': 'イ',
  'explanation': '「音楽鑑賞」は、音楽を聴く活動を表しています。「聴くこと」を表すため、listen に -ing を付けて listening とします。',
  'level': 2,
  'level_name': 'レベル2：動名詞を使ってみよう'},
 {'id': 'gerund_l2_022',
  'major_question': 2,
  'question_number': 22,
  'question_type': 'japanese_to_english_choice',
  'objective': 'gerund_basic',
  'difficulty': 2,
  'japanese': '読書は楽しいです。',
  'english': '（\u3000\u3000\u3000）books is fun.',
  'options': [{'label': 'ア', 'value': 'Read', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'Reading', 'error_type': 'none'},
              {'label': 'ウ', 'value': 'Reads', 'error_type': 'third_person'},
              {'label': 'エ', 'value': 'Readed', 'error_type': 'other'}],
  'answer': 'イ',
  'explanation': '「読書」は、本を読む活動を表しています。「読むこと」を文の主語にするため、read に -ing を付けて Reading とします。',
  'level': 2,
  'level_name': 'レベル2：動名詞を使ってみよう'},
 {'id': 'gerund_l2_023',
  'major_question': 2,
  'question_number': 23,
  'question_type': 'japanese_to_english_choice',
  'objective': 'finish_gerund',
  'difficulty': 2,
  'japanese': '私は宿題をするのを終えました。',
  'english': 'I finished（\u3000\u3000\u3000）my homework.',
  'options': [{'label': 'ア', 'value': 'do', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'doing', 'error_type': 'none'},
              {'label': 'ウ', 'value': 'did', 'error_type': 'past_form'},
              {'label': 'エ', 'value': 'does', 'error_type': 'third_person'}],
  'answer': 'イ',
  'explanation': '「宿題をするのを終えました」は、「宿題をすることを終えました」という意味です。do に -ing を付けて doing とします。',
  'level': 2,
  'level_name': 'レベル2：動名詞を使ってみよう'},
 {'id': 'gerund_l2_024',
  'major_question': 2,
  'question_number': 24,
  'question_type': 'japanese_to_english_choice',
  'objective': 'like_gerund',
  'difficulty': 2,
  'japanese': '私は映画を見るのが好きです。',
  'english': 'I like（\u3000\u3000\u3000）movies.',
  'options': [{'label': 'ア', 'value': 'watch', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'watched', 'error_type': 'past_form'},
              {'label': 'ウ', 'value': 'watching', 'error_type': 'none'},
              {'label': 'エ', 'value': 'watches', 'error_type': 'third_person'}],
  'answer': 'ウ',
  'explanation': '「映画を見るのが好きです」は、映画を見る活動が好きだという意味です。「見ること」を表すため、watch に -ing を付けて watching とします。',
  'level': 2,
  'level_name': 'レベル2：動名詞を使ってみよう'},
 {'id': 'gerund_l2_025',
  'major_question': 2,
  'question_number': 25,
  'question_type': 'japanese_to_english_choice',
  'objective': 'enjoy_gerund',
  'difficulty': 2,
  'japanese': 'ギターの演奏を楽しんでいます。',
  'english': 'I enjoy（\u3000\u3000\u3000）the guitar.',
  'options': [{'label': 'ア', 'value': 'play', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'playing', 'error_type': 'none'},
              {'label': 'ウ', 'value': 'played', 'error_type': 'past_form'},
              {'label': 'エ', 'value': 'plays', 'error_type': 'third_person'}],
  'answer': 'イ',
  'explanation': '「ギターの演奏」は、ギターを弾く活動を表しています。「弾くこと」を表すため、play に -ing を付けて playing とします。',
  'level': 2,
  'level_name': 'レベル2：動名詞を使ってみよう'},
 {'id': 'gerund_l2_026',
  'major_question': 2,
  'question_number': 26,
  'question_type': 'japanese_to_english_choice',
  'objective': 'gerund_basic',
  'difficulty': 2,
  'japanese': '絵を描くのは楽しいです。',
  'english': '（\u3000\u3000\u3000）pictures is fun.',
  'options': [{'label': 'ア', 'value': 'Draw', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'Drawing', 'error_type': 'none'},
              {'label': 'ウ', 'value': 'Drew', 'error_type': 'past_form'},
              {'label': 'エ', 'value': 'Draws', 'error_type': 'third_person'}],
  'answer': 'イ',
  'explanation': '「絵を描くのは楽しいです」は、絵を描く活動が楽しいという意味です。「描くこと」を文の主語にするため、draw に -ing を付けて Drawing とします。',
  'level': 2,
  'level_name': 'レベル2：動名詞を使ってみよう'},
 {'id': 'gerund_l2_027',
  'major_question': 2,
  'question_number': 27,
  'question_type': 'japanese_to_english_choice',
  'objective': 'like_gerund',
  'difficulty': 2,
  'japanese': '私は音楽を聴くのが好きです。',
  'english': 'I like（\u3000\u3000\u3000）to music.',
  'options': [{'label': 'ア', 'value': 'listen', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'listening', 'error_type': 'none'},
              {'label': 'ウ', 'value': 'listened', 'error_type': 'past_form'},
              {'label': 'エ', 'value': 'listens', 'error_type': 'third_person'}],
  'answer': 'イ',
  'explanation': '「音楽を聴くのが好きです」は、音楽を聴く活動が好きだという意味です。「聴くこと」を表すため、listen に -ing を付けて listening とします。',
  'level': 2,
  'level_name': 'レベル2：動名詞を使ってみよう'},
 {'id': 'gerund_l2_028',
  'major_question': 2,
  'question_number': 28,
  'question_type': 'japanese_to_english_choice',
  'objective': 'finish_gerund',
  'difficulty': 2,
  'japanese': '私は部屋の掃除を終えました。',
  'english': 'I finished（\u3000\u3000\u3000）my room.',
  'options': [{'label': 'ア', 'value': 'clean', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'cleaned', 'error_type': 'past_form'},
              {'label': 'ウ', 'value': 'cleaning', 'error_type': 'none'},
              {'label': 'エ', 'value': 'cleans', 'error_type': 'third_person'}],
  'answer': 'ウ',
  'explanation': '「部屋の掃除を終えました」は、部屋を掃除する活動を終えたという意味です。「掃除すること」を表すため、clean に -ing を付けて cleaning '
                 'とします。',
  'level': 2,
  'level_name': 'レベル2：動名詞を使ってみよう'},
 {'id': 'gerund_l2_029',
  'major_question': 2,
  'question_number': 29,
  'question_type': 'japanese_to_english_choice',
  'objective': 'enjoy_gerund',
  'difficulty': 2,
  'japanese': '英語の勉強を楽しんでいます。',
  'english': 'I enjoy（\u3000\u3000\u3000）English.',
  'options': [{'label': 'ア', 'value': 'study', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'studying', 'error_type': 'none'},
              {'label': 'ウ', 'value': 'studied', 'error_type': 'past_form'},
              {'label': 'エ', 'value': 'studies', 'error_type': 'third_person'}],
  'answer': 'イ',
  'explanation': '「英語の勉強」は、英語を勉強する活動を表しています。「勉強すること」を表すため、study に -ing を付けて studying とします。',
  'level': 2,
  'level_name': 'レベル2：動名詞を使ってみよう'},
 {'id': 'gerund_l2_030',
  'major_question': 2,
  'question_number': 30,
  'question_type': 'japanese_to_english_choice',
  'objective': 'like_gerund',
  'difficulty': 2,
  'japanese': 'サッカーをするのが好きです。',
  'english': 'I like（\u3000\u3000\u3000）soccer.',
  'options': [{'label': 'ア', 'value': 'play', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'played', 'error_type': 'past_form'},
              {'label': 'ウ', 'value': 'plays', 'error_type': 'third_person'},
              {'label': 'エ', 'value': 'playing', 'error_type': 'none'}],
  'answer': 'エ',
  'explanation': '「サッカーをするのが好きです」は、サッカーをする活動が好きだという意味です。「すること」を表すため、play に -ing を付けて playing とします。',
  'level': 2,
  'level_name': 'レベル2：動名詞を使ってみよう'},
 {'id': 'gerund_l3_031',
  'major_question': 3,
  'question_number': 31,
  'question_type': 'japanese_to_english_choice',
  'objective': 'like_gerund',
  'difficulty': 3,
  'japanese': '彼女は本を読むことが好きです。',
  'english': 'She likes（\u3000\u3000\u3000）books.',
  'options': [{'label': 'ア', 'value': 'read', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'reads', 'error_type': 'third_person'},
              {'label': 'ウ', 'value': 'reading', 'error_type': 'none'},
              {'label': 'エ', 'value': 'readed', 'error_type': 'other'}],
  'answer': 'ウ',
  'explanation': '「本を読むこと」が好きなので、read に -ing を付けて reading とします。She に対応する三単現のSは likes '
                 'ですでに付いているので、空欄では reads ではなく reading を選びます。',
  'level': 3,
  'level_name': 'レベル3：動名詞の名人になってみよう'},
 {'id': 'gerund_l3_032',
  'major_question': 3,
  'question_number': 32,
  'question_type': 'japanese_to_english_choice',
  'objective': 'verb_form_choice',
  'difficulty': 3,
  'japanese': '彼女は毎日テニスをします。',
  'english': 'She（\u3000\u3000）tennis every day.',
  'options': [{'label': 'ア', 'value': 'playing', 'error_type': 'gerund'},
              {'label': 'イ', 'value': 'plays', 'error_type': 'none'},
              {'label': 'ウ', 'value': 'played', 'error_type': 'past_form'},
              {'label': 'エ', 'value': 'play', 'error_type': 'base_form'}],
  'answer': 'イ',
  'explanation': '「毎日テニスをします」は、いつものことを表しています。主語が She なので、play は plays になります。',
  'level': 3,
  'level_name': 'レベル3：動名詞の名人になってみよう'},
 {'id': 'gerund_l3_033',
  'major_question': 3,
  'question_number': 33,
  'question_type': 'japanese_to_english_choice',
  'objective': 'finish_gerund',
  'difficulty': 3,
  'japanese': '彼女は昼食を食べ終えました。',
  'english': 'She finished（\u3000\u3000\u3000）lunch.',
  'options': [{'label': 'ア', 'value': 'eat', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'eats', 'error_type': 'third_person'},
              {'label': 'ウ', 'value': 'ate', 'error_type': 'past_form'},
              {'label': 'エ', 'value': 'eating', 'error_type': 'none'}],
  'answer': 'エ',
  'explanation': '「昼食を食べることを終えました」という意味なので、eat に -ing を付けて eating とします。finished がすでに過去形なので、空欄を ate '
                 'にする必要はありません。She の三単現のSも、過去形の finished では処理済みなので、空欄では eating を選びます。',
  'level': 3,
  'level_name': 'レベル3：動名詞の名人になってみよう'},
 {'id': 'gerund_l3_034',
  'major_question': 3,
  'question_number': 34,
  'question_type': 'japanese_to_english_choice',
  'objective': 'verb_form_choice',
  'difficulty': 3,
  'japanese': '彼は昨日、映画を見ました。',
  'english': 'He（\u3000\u3000）a movie yesterday.',
  'options': [{'label': 'ア', 'value': 'watch', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'watching', 'error_type': 'gerund'},
              {'label': 'ウ', 'value': 'watched', 'error_type': 'none'},
              {'label': 'エ', 'value': 'watches', 'error_type': 'third_person'}],
  'answer': 'ウ',
  'explanation': 'yesterday は「昨日」という意味です。昨日のことなので watched を選びます。',
  'level': 3,
  'level_name': 'レベル3：動名詞の名人になってみよう'},
 {'id': 'gerund_l3_035',
  'major_question': 3,
  'question_number': 35,
  'question_type': 'japanese_to_english_choice',
  'objective': 'finish_gerund',
  'difficulty': 3,
  'japanese': '彼は宿題をするのを終えました。',
  'english': 'He finished（\u3000\u3000\u3000）his homework.',
  'options': [{'label': 'ア', 'value': 'do', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'did', 'error_type': 'past_form'},
              {'label': 'ウ', 'value': 'does', 'error_type': 'third_person'},
              {'label': 'エ', 'value': 'doing', 'error_type': 'none'}],
  'answer': 'エ',
  'explanation': '「宿題をすることを終えました」なので、do に -ing を付けて doing とします。finished が過去形なので空欄を did '
                 'にする必要はありません。また、He に対する三単現の形を考えても、空欄は does ではなく動名詞 doing です。',
  'level': 3,
  'level_name': 'レベル3：動名詞の名人になってみよう'},
 {'id': 'gerund_l3_036',
  'major_question': 3,
  'question_number': 36,
  'question_type': 'japanese_to_english_choice',
  'objective': 'enjoy_gerund',
  'difficulty': 3,
  'japanese': '彼女は歌うことを楽しんでいます。',
  'english': 'She enjoys（\u3000\u3000\u3000）songs.',
  'options': [{'label': 'ア', 'value': 'sing', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'sang', 'error_type': 'past_form'},
              {'label': 'ウ', 'value': 'sings', 'error_type': 'third_person'},
              {'label': 'エ', 'value': 'singing', 'error_type': 'none'}],
  'answer': 'エ',
  'explanation': '「歌うこと」を楽しんでいるので、sing に -ing を付けて singing とします。She に対応する三単現のSは enjoys '
                 'に付いているため、空欄では sings ではなく singing を選びます。',
  'level': 3,
  'level_name': 'レベル3：動名詞の名人になってみよう'},
 {'id': 'gerund_l3_037',
  'major_question': 3,
  'question_number': 37,
  'question_type': 'japanese_to_english_choice',
  'objective': 'verb_form_choice',
  'difficulty': 3,
  'japanese': '彼らは放課後にサッカーをします。',
  'english': 'They（\u3000\u3000）soccer after school.',
  'options': [{'label': 'ア', 'value': 'plays', 'error_type': 'third_person'},
              {'label': 'イ', 'value': 'playing', 'error_type': 'gerund'},
              {'label': 'ウ', 'value': 'play', 'error_type': 'none'},
              {'label': 'エ', 'value': 'played', 'error_type': 'past_form'}],
  'answer': 'ウ',
  'explanation': '主語が They（彼ら）なので、play のまま使います。',
  'level': 3,
  'level_name': 'レベル3：動名詞の名人になってみよう'},
 {'id': 'gerund_l3_038',
  'major_question': 3,
  'question_number': 38,
  'question_type': 'japanese_to_english_choice',
  'objective': 'like_gerund',
  'difficulty': 3,
  'japanese': '彼女はギターを弾くのが好きです。',
  'english': 'She likes（\u3000\u3000\u3000）the guitar.',
  'options': [{'label': 'ア', 'value': 'play', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'played', 'error_type': 'past_form'},
              {'label': 'ウ', 'value': 'plays', 'error_type': 'third_person'},
              {'label': 'エ', 'value': 'playing', 'error_type': 'none'}],
  'answer': 'エ',
  'explanation': '「ギターを弾くのが好きです」なので、play に -ing を付けて playing とします。She に対応する三単現のSは likes '
                 'に付いているので、空欄では plays ではなく playing を選びます。',
  'level': 3,
  'level_name': 'レベル3：動名詞の名人になってみよう'},
 {'id': 'gerund_l3_039',
  'major_question': 3,
  'question_number': 39,
  'question_type': 'japanese_to_english_choice',
  'objective': 'verb_form_choice',
  'difficulty': 3,
  'japanese': '彼女は毎日、英語を勉強します。',
  'english': 'She（\u3000\u3000）English every day.',
  'options': [{'label': 'ア', 'value': 'study', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'studied', 'error_type': 'past_form'},
              {'label': 'ウ', 'value': 'studying', 'error_type': 'gerund'},
              {'label': 'エ', 'value': 'studies', 'error_type': 'none'}],
  'answer': 'エ',
  'explanation': '「毎日、英語を勉強します」は、いつものことを表しています。主語が She なので、study は studies になります。',
  'level': 3,
  'level_name': 'レベル3：動名詞の名人になってみよう'},
 {'id': 'gerund_l3_040',
  'major_question': 3,
  'question_number': 40,
  'question_type': 'japanese_to_english_choice',
  'objective': 'enjoy_gerund',
  'difficulty': 3,
  'japanese': '彼はサッカーをすることを楽しんでいます。',
  'english': 'He enjoys（\u3000\u3000\u3000）soccer.',
  'options': [{'label': 'ア', 'value': 'play', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'played', 'error_type': 'past_form'},
              {'label': 'ウ', 'value': 'plays', 'error_type': 'third_person'},
              {'label': 'エ', 'value': 'playing', 'error_type': 'none'}],
  'answer': 'エ',
  'explanation': '「サッカーをすること」を楽しんでいるので、play に -ing を付けて playing とします。He に対応する三単現のSは enjoys '
                 'に付いているため、空欄では plays ではなく playing を選びます。',
  'level': 3,
  'level_name': 'レベル3：動名詞の名人になってみよう'},
 {'id': 'gerund_l3_041',
  'major_question': 3,
  'question_number': 41,
  'question_type': 'japanese_to_english_choice',
  'objective': 'like_gerund',
  'difficulty': 3,
  'japanese': '彼女は英語を勉強するのが好きです。',
  'english': 'She likes（\u3000\u3000\u3000）English.',
  'options': [{'label': 'ア', 'value': 'study', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'studied', 'error_type': 'past_form'},
              {'label': 'ウ', 'value': 'studies', 'error_type': 'third_person'},
              {'label': 'エ', 'value': 'studying', 'error_type': 'none'}],
  'answer': 'エ',
  'explanation': '「英語を勉強するのが好きです」なので、study に -ing を付けて studying とします。She に対応する三単現のSは likes '
                 'に付いているため、空欄では studies ではなく studying を選びます。',
  'level': 3,
  'level_name': 'レベル3：動名詞の名人になってみよう'},
 {'id': 'gerund_l3_042',
  'major_question': 3,
  'question_number': 42,
  'question_type': 'japanese_to_english_choice',
  'objective': 'verb_form_choice',
  'difficulty': 3,
  'japanese': '彼は昨日、テニスをしました。',
  'english': 'He（\u3000\u3000）tennis yesterday.',
  'options': [{'label': 'ア', 'value': 'plays', 'error_type': 'third_person'},
              {'label': 'イ', 'value': 'played', 'error_type': 'none'},
              {'label': 'ウ', 'value': 'playing', 'error_type': 'gerund'},
              {'label': 'エ', 'value': 'play', 'error_type': 'base_form'}],
  'answer': 'イ',
  'explanation': 'yesterday は「昨日」という意味です。昨日のことなので played を選びます。',
  'level': 3,
  'level_name': 'レベル3：動名詞の名人になってみよう'},
 {'id': 'gerund_l3_043',
  'major_question': 3,
  'question_number': 43,
  'question_type': 'japanese_to_english_choice',
  'objective': 'enjoy_gerund',
  'difficulty': 3,
  'japanese': '彼女は本を読むことを楽しんでいます。',
  'english': 'She enjoys（\u3000\u3000\u3000）books.',
  'options': [{'label': 'ア', 'value': 'read', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'readed', 'error_type': 'other'},
              {'label': 'ウ', 'value': 'reads', 'error_type': 'third_person'},
              {'label': 'エ', 'value': 'reading', 'error_type': 'none'}],
  'answer': 'エ',
  'explanation': '「本を読むこと」を楽しんでいるので、read に -ing を付けて reading とします。She に対応する三単現のSは enjoys '
                 'に付いているため、空欄では reads ではなく reading を選びます。',
  'level': 3,
  'level_name': 'レベル3：動名詞の名人になってみよう'},
 {'id': 'gerund_l3_044',
  'major_question': 3,
  'question_number': 44,
  'question_type': 'japanese_to_english_choice',
  'objective': 'verb_form_choice',
  'difficulty': 3,
  'japanese': '私は日曜日に映画を見ます。',
  'english': 'I（\u3000\u3000）movies on Sundays.',
  'options': [{'label': 'ア', 'value': 'watching', 'error_type': 'gerund'},
              {'label': 'イ', 'value': 'watches', 'error_type': 'third_person'},
              {'label': 'ウ', 'value': 'watch', 'error_type': 'none'},
              {'label': 'エ', 'value': 'watched', 'error_type': 'past_form'}],
  'answer': 'ウ',
  'explanation': '主語が I なので、watch をそのまま使います。',
  'level': 3,
  'level_name': 'レベル3：動名詞の名人になってみよう'},
 {'id': 'gerund_l3_045',
  'major_question': 3,
  'question_number': 45,
  'question_type': 'japanese_to_english_choice',
  'objective': 'finish_gerund',
  'difficulty': 3,
  'japanese': '彼女は本を読むのを終えました。',
  'english': 'She finished（\u3000\u3000\u3000）the book.',
  'options': [{'label': 'ア', 'value': 'read', 'error_type': 'base_form'},
              {'label': 'イ', 'value': 'reads', 'error_type': 'third_person'},
              {'label': 'ウ', 'value': 'readed', 'error_type': 'other'},
              {'label': 'エ', 'value': 'reading', 'error_type': 'none'}],
  'answer': 'エ',
  'explanation': '「本を読むことを終えました」なので、read に -ing を付けて reading とします。finished '
                 'がすでに過去形なので、空欄を過去形にする必要はありません。She に対応する三単現のSも finished の文では空欄に付けず、reading を選びます。',
  'level': 3,
  'level_name': 'レベル3：動名詞の名人になってみよう'}]
# =========================================================
# レベル0：動名詞ってなんだろう
# 日本語の中から「～すること」にあたる部分を見つける問題。
# まずは「動作」と「動作を表すことば」の違いに意識を向ける。
# =========================================================

LEVEL0_QUESTION_BANK = [
    {
        "id": "gerund_l0_001", "major_question": 0, "question_number": 1,
        "question_type": "japanese_phrase_choice", "objective": "japanese_meaning",
        "difficulty": 0, "japanese": "泳ぐことは楽しいです。", "english": "",
        "options": [
            {"label": "ア", "value": "泳ぐこと", "error_type": "none"},
            {"label": "イ", "value": "泳ぐ", "error_type": "action_only"},
        ], "answer": "ア",
        "explanation": "この文で「～すること」にあたる部分は「泳ぐこと」です。",
        "level": 0, "level_name": "レベル0：動名詞ってなんだろう",
    },
    {
        "id": "gerund_l0_002", "major_question": 0, "question_number": 2,
        "question_type": "japanese_phrase_choice", "objective": "japanese_meaning",
        "difficulty": 0, "japanese": "本を読むことが好きです。", "english": "",
        "options": [
            {"label": "ア", "value": "読む", "error_type": "action_only"},
            {"label": "イ", "value": "読むこと", "error_type": "none"},
        ], "answer": "イ",
        "explanation": "「読むこと」が、好きなことを表しています。",
        "level": 0, "level_name": "レベル0：動名詞ってなんだろう",
    },
    {
        "id": "gerund_l0_003", "major_question": 0, "question_number": 3,
        "question_type": "japanese_phrase_choice", "objective": "japanese_meaning",
        "difficulty": 0, "japanese": "歌うことは楽しいです。", "english": "",
        "options": [
            {"label": "ア", "value": "歌う", "error_type": "action_only"},
            {"label": "イ", "value": "歌うこと", "error_type": "none"},
        ], "answer": "イ",
        "explanation": "この文で「～すること」にあたる部分は「歌うこと」です。",
        "level": 0, "level_name": "レベル0：動名詞ってなんだろう",
    },
    {
        "id": "gerund_l0_004", "major_question": 0, "question_number": 4,
        "question_type": "japanese_phrase_choice", "objective": "japanese_meaning",
        "difficulty": 0, "japanese": "料理することが好きです。", "english": "",
        "options": [
            {"label": "ア", "value": "料理すること", "error_type": "none"},
            {"label": "イ", "value": "料理する", "error_type": "action_only"},
        ], "answer": "ア",
        "explanation": "この文で「～すること」にあたる部分は「料理すること」です。",
        "level": 0, "level_name": "レベル0：動名詞ってなんだろう",
    },
    {
        "id": "gerund_l0_005", "major_question": 0, "question_number": 5,
        "question_type": "japanese_phrase_choice", "objective": "japanese_meaning",
        "difficulty": 0, "japanese": "絵を描くことはおもしろいです。", "english": "",
        "options": [
            {"label": "ア", "value": "描く", "error_type": "action_only"},
            {"label": "イ", "value": "描くこと", "error_type": "none"},
        ], "answer": "イ",
        "explanation": "この文で「～すること」にあたる部分は「描くこと」です。",
        "level": 0, "level_name": "レベル0：動名詞ってなんだろう",
    },
    {
        "id": "gerund_l0_006", "major_question": 0, "question_number": 6,
        "question_type": "japanese_phrase_choice", "objective": "japanese_meaning",
        "difficulty": 0, "japanese": "泳ぐことが好きです。", "english": "",
        "options": [
            {"label": "ア", "value": "泳ぐ", "error_type": "action_only"},
            {"label": "イ", "value": "泳ぐこと", "error_type": "none"},
        ], "answer": "イ",
        "explanation": "「泳ぐこと」が、好きなことを表しています。",
        "level": 0, "level_name": "レベル0：動名詞ってなんだろう",
    },
    {
        "id": "gerund_l0_007", "major_question": 0, "question_number": 7,
        "question_type": "japanese_phrase_choice", "objective": "japanese_meaning",
        "difficulty": 0, "japanese": "映画を見ることが好きです。", "english": "",
        "options": [
            {"label": "ア", "value": "見ること", "error_type": "none"},
            {"label": "イ", "value": "見る", "error_type": "action_only"},
        ], "answer": "ア",
        "explanation": "この文で「～すること」にあたる部分は「見ること」です。",
        "level": 0, "level_name": "レベル0：動名詞ってなんだろう",
    },
    {
        "id": "gerund_l0_008", "major_question": 0, "question_number": 8,
        "question_type": "japanese_phrase_choice", "objective": "japanese_meaning",
        "difficulty": 0, "japanese": "音楽を聴くことは楽しいです。", "english": "",
        "options": [
            {"label": "ア", "value": "聴く", "error_type": "action_only"},
            {"label": "イ", "value": "聴くこと", "error_type": "none"},
        ], "answer": "イ",
        "explanation": "この文で「～すること」にあたる部分は「聴くこと」です。",
        "level": 0, "level_name": "レベル0：動名詞ってなんだろう",
    },
    {
        "id": "gerund_l0_009", "major_question": 0, "question_number": 9,
        "question_type": "japanese_phrase_choice", "objective": "japanese_meaning",
        "difficulty": 0, "japanese": "ギターを弾くことが好きです。", "english": "",
        "options": [
            {"label": "ア", "value": "弾くこと", "error_type": "none"},
            {"label": "イ", "value": "弾く", "error_type": "action_only"},
        ], "answer": "ア",
        "explanation": "「弾くこと」が、好きなことを表しています。",
        "level": 0, "level_name": "レベル0：動名詞ってなんだろう",
    },
    {
        "id": "gerund_l0_010", "major_question": 0, "question_number": 10,
        "question_type": "japanese_phrase_choice", "objective": "japanese_meaning",
        "difficulty": 0, "japanese": "走ることは大切です。", "english": "",
        "options": [
            {"label": "ア", "value": "走る", "error_type": "action_only"},
            {"label": "イ", "value": "走ること", "error_type": "none"},
        ], "answer": "イ",
        "explanation": "この文で「～すること」にあたる部分は「走ること」です。",
        "level": 0, "level_name": "レベル0：動名詞ってなんだろう",
    },
    {
        "id": "gerund_l0_011", "major_question": 0, "question_number": 11,
        "question_type": "japanese_phrase_choice", "objective": "japanese_meaning",
        "difficulty": 0, "japanese": "料理することは楽しいです。", "english": "",
        "options": [
            {"label": "ア", "value": "料理する", "error_type": "action_only"},
            {"label": "イ", "value": "料理すること", "error_type": "none"},
        ], "answer": "イ",
        "explanation": "この文で「～すること」にあたる部分は「料理すること」です。",
        "level": 0, "level_name": "レベル0：動名詞ってなんだろう",
    },
    {
        "id": "gerund_l0_012", "major_question": 0, "question_number": 12,
        "question_type": "japanese_phrase_choice", "objective": "japanese_meaning",
        "difficulty": 0, "japanese": "英語を勉強することは大切です。", "english": "",
        "options": [
            {"label": "ア", "value": "勉強すること", "error_type": "none"},
            {"label": "イ", "value": "勉強する", "error_type": "action_only"},
        ], "answer": "ア",
        "explanation": "この文で「～すること」にあたる部分は「勉強すること」です。",
        "level": 0, "level_name": "レベル0：動名詞ってなんだろう",
    },
    {
        "id": "gerund_l0_013", "major_question": 0, "question_number": 13,
        "question_type": "japanese_phrase_choice", "objective": "japanese_meaning",
        "difficulty": 0, "japanese": "友だちと話すことが好きです。", "english": "",
        "options": [
            {"label": "ア", "value": "話す", "error_type": "action_only"},
            {"label": "イ", "value": "話すこと", "error_type": "none"},
        ], "answer": "イ",
        "explanation": "この文で「～すること」にあたる部分は「話すこと」です。",
        "level": 0, "level_name": "レベル0：動名詞ってなんだろう",
    },
    {
        "id": "gerund_l0_014", "major_question": 0, "question_number": 14,
        "question_type": "japanese_phrase_choice", "objective": "japanese_meaning",
        "difficulty": 0, "japanese": "音楽を聴くことが好きです。", "english": "",
        "options": [
            {"label": "ア", "value": "聴くこと", "error_type": "none"},
            {"label": "イ", "value": "聴く", "error_type": "action_only"},
        ], "answer": "ア",
        "explanation": "「聴くこと」が、好きなことを表しています。",
        "level": 0, "level_name": "レベル0：動名詞ってなんだろう",
    },
    {
        "id": "gerund_l0_015", "major_question": 0, "question_number": 15,
        "question_type": "japanese_phrase_choice", "objective": "japanese_meaning",
        "difficulty": 0, "japanese": "写真を撮ることは楽しいです。", "english": "",
        "options": [
            {"label": "ア", "value": "撮る", "error_type": "action_only"},
            {"label": "イ", "value": "撮ること", "error_type": "none"},
        ], "answer": "イ",
        "explanation": "この文で「～すること」にあたる部分は「撮ること」です。",
        "level": 0, "level_name": "レベル0：動名詞ってなんだろう",
    },
]

QUESTION_BANK = LEVEL0_QUESTION_BANK + QUESTION_BANK


def make_question_order(level):
    """レベルごとの問題順を作る。レベル3は各5問に-ing以外の正解を2問入れる。"""
    questions = [q for q in QUESTION_BANK if q.get("level") == level]
    if level == 3:
        non_ing = []
        ing = []
        for question in questions:
            correct_option = next(
                (option for option in question["options"] if option["label"] == question["answer"]),
                None,
            )
            value = str(correct_option.get("value", "")) if correct_option else ""
            if not value.lower().endswith("ing"):
                non_ing.append(question["id"])
            else:
                ing.append(question["id"])
        random.shuffle(non_ing)
        random.shuffle(ing)
        ordered_ids = []
        while non_ing or ing:
            batch = non_ing[:2] + ing[:3]
            del non_ing[:2]
            del ing[:3]
            random.shuffle(batch)
            ordered_ids.extend(batch)
        return ordered_ids

    ids = [q["id"] for q in questions]
    random.shuffle(ids)
    return ids

# =========================================================

def initialize_state():
    """初期化とバージョン更新時の状態移行。学習履歴は消さずに保持する。"""
    previous_version = st.session_state.get("state_version")

    st.session_state.setdefault("batch_number", 0)
    st.session_state.setdefault("history", [])
    st.session_state.setdefault("batch_results", None)
    st.session_state.setdefault("batch_submitted", False)
    st.session_state.setdefault("student_name", "")
    st.session_state.setdefault("student_name_input", st.session_state.student_name)
    st.session_state.setdefault("current_level", 1)
    st.session_state.setdefault("level_batch_number", 0)
    st.session_state.setdefault("learning_started", False)
    st.session_state.setdefault("selected_start_level", 0)
    st.session_state.setdefault("session_started_at", None)
    st.session_state.setdefault("session_ended_at", None)
    st.session_state.setdefault("learning_session_id", None)
    st.session_state.setdefault("question_order_by_level", {})
    st.session_state.setdefault("last_batch_question_ids", [])
    st.session_state.setdefault("batch_started_at", None)
    st.session_state.setdefault("active_batch_key", None)
    st.session_state.setdefault("attempt_counts", {})

    if previous_version != STATE_VERSION:
        # コード更新時に古い採点画面だけを解除し、過去の学習履歴は保持する。
        st.session_state.state_version = STATE_VERSION
        st.session_state.batch_results = None
        st.session_state.batch_submitted = False
        st.session_state.active_batch_key = None
        st.session_state.batch_started_at = None
        rebuilt_attempt_counts = {}
        for record in st.session_state.history:
            question_id = record.get("question_id")
            if question_id:
                rebuilt_attempt_counts[question_id] = max(
                    rebuilt_attempt_counts.get(question_id, 0),
                    int(record.get("attempt_number", 1) or 1),
                )
        st.session_state.attempt_counts = rebuilt_attempt_counts


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
    attempt_number=1,
    submitted_at=None,
    batch_elapsed_seconds=None,
    batch_question_number=None,
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

    if submitted_at is None:
        submitted_at = now_japan()

    return {
        "learning_session_id": st.session_state.get("learning_session_id"),
        "timestamp": submitted_at.isoformat(timespec="milliseconds"),
        "session_started_at": st.session_state.get("session_started_at"),
        "batch_started_at": st.session_state.get("batch_started_at"),
        "batch_ended_at": submitted_at.isoformat(timespec="milliseconds"),
        "submitted_at": submitted_at.isoformat(timespec="milliseconds"),
        "seconds_from_batch_display_to_submit": batch_elapsed_seconds,
        "attempt_number": attempt_number,
        "is_first_attempt": attempt_number == 1,

        # レポート上のセット番号は、現在のレベル内で表示したセット順にする。
        # 全体進行用 batch_number は画面遷移の操作に左右されるため使用しない。
        "batch_number": (
            int(st.session_state.get("level_batch_number", 0))
            + 1
        ),

        "major_question": question[
            "major_question"
        ],

        # セット内の実際の表示順を記録する。
        # question_number はストック番号なので、ここから小問番号を計算しない。
        "batch_question_number": (
            batch_question_number
            if batch_question_number is not None
            else None
        ),

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

        "english": question.get(
            "english", ""
        ),

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
                "batch_question_number",
                record.get("question_number", 0),
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
    session_started_at=None,
    session_ended_at=None,
):

    if not records:
        return ""

    records = sorted(
        records,
        key=lambda record: (
            record.get("submitted_at") or record.get("timestamp", ""),
            int(record.get("batch_question_number", record.get("question_number", 0)) or 0),
        ),
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
        "action_only": "「～こと」が付かない形を選んだ",
        "gerund": "動名詞の形を選んだ",
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

    if not session_started_at:
        session_started_at = next((r.get("session_started_at") for r in records if r.get("session_started_at")), "")
    submitted_values = [r.get("submitted_at") or r.get("timestamp", "") for r in records]
    parsed_submissions = []
    for value in submitted_values:
        if not value:
            continue
        try:
            parsed_submissions.append((datetime.fromisoformat(value), value))
        except (TypeError, ValueError):
            continue
    last_timestamp = max(parsed_submissions, key=lambda item: item[0])[1] if parsed_submissions else ""
    try:
        started_dt = datetime.fromisoformat(session_started_at) if session_started_at else None
    except (TypeError, ValueError):
        started_dt = None
    try:
        last_submit_dt = datetime.fromisoformat(last_timestamp) if last_timestamp else None
    except (TypeError, ValueError):
        last_submit_dt = None

    lines = [
        "【中2英語 個別学習支援ドリル｜今日の学習結果】",
        "※今日（日本時間）に採点された問題を対象としています。複数回の学習がある場合は、それらをまとめて記録します。",
        f"今日の最初の学習開始日時：{session_started_at or '記録なし'}",
        f"最終採点日時：{last_timestamp or '記録なし'}",
        (f"最初の学習開始から最終採点まで：{max(0, (last_submit_dt - started_dt).total_seconds()):.1f}秒（途中の休憩・中断時間を含む場合があります）" if last_submit_dt and started_dt else "所要時間：算出できません"),
        f"問題数：{total}問",
        f"正解：{correct}問",
        f"正答率：{accuracy:.1f}%",
    ]

    # セット単位の時刻を出力。開始は問題表示、終了は採点ボタン押下後の記録時点。
    batch_groups = {}
    for record in records:
        group_key = (
            record.get("learning_session_id", ""),
            record.get("level", ""),
            record.get("batch_number", ""),
            record.get("batch_started_at", ""),
        )
        if group_key not in batch_groups:
            batch_groups[group_key] = record

    lines.extend(["", "【セット別の開始・終了時刻】"])
    lines.append("※開始は5問セットが画面に表示された時点、終了は「採点する」を押して採点処理が記録された時点です。実際に考え始めた瞬間や、画面を見ていない時間までは判定できません。")
    for group_key, record in sorted(batch_groups.items(), key=lambda item: (str(item[1].get("submitted_at", "")), str(item[0]))):
        batch_number = record.get("batch_number", "")
        level_name = record.get("level_name", "")
        if level_name:
            lines.append(f"対象：{level_name}／セット{batch_number}")
        batch_start = record.get("batch_started_at") or "記録なし"
        batch_end = record.get("batch_ended_at") or record.get("submitted_at") or record.get("timestamp") or "記録なし"
        try:
            start_dt = datetime.fromisoformat(batch_start)
            end_dt = datetime.fromisoformat(batch_end)
            duration_text = f"{max(0.0, (end_dt - start_dt).total_seconds()):.1f}秒"
        except (TypeError, ValueError):
            duration_text = "算出できません"
        lines.extend([
            f"  開始日時：{batch_start}",
            f"  終了日時：{batch_end}",
            f"  セット所要時間：{duration_text}",
        ])

    lines.extend(["", "【学習項目別の結果】"])

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
            f"第{record.get('batch_question_number', record.get('question_number', ''))}問",
            f"セット：{record.get('batch_number', '')}",
            f"ストック番号：{record.get('question_number', '')}",
            f"問題ID：{record.get('question_id', '')}",
            f"レベル：{record.get('level_name') or ('レベル' + str(record.get('level', '')) if record.get('level', '') != '' else '記録なし')}",
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
        "【今回まちがえたこと】",
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

            "exported_at": now_japan().isoformat(timespec="seconds"),

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

    st.session_state.history = data["history"]
    rebuilt_attempt_counts = {}
    for record in st.session_state.history:
        question_id = record.get("question_id")
        if question_id:
            rebuilt_attempt_counts[question_id] = max(
                rebuilt_attempt_counts.get(question_id, 0),
                int(record.get("attempt_number", 1) or 1),
            )
    st.session_state.attempt_counts = rebuilt_attempt_counts

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
question_by_id = {q["id"]: q for q in QUESTION_BANK}
level_order = st.session_state.get("question_order_by_level", {}).get(str(current_level))
if level_order:
    current_level_questions = [question_by_id[qid] for qid in level_order if qid in question_by_id]
else:
    current_level_questions = [q for q in QUESTION_BANK if q.get("level") == current_level]
level_offset = st.session_state.get("level_batch_number", 0) * QUESTIONS_PER_BATCH
current_questions = current_level_questions[level_offset:level_offset + QUESTIONS_PER_BATCH]

# セットが切り替わった時点で開始時刻を記録する。
active_batch_key = f"{current_level}:{st.session_state.get('level_batch_number', 0)}"
if st.session_state.get("active_batch_key") != active_batch_key:
    now = now_japan()
    st.session_state.active_batch_key = active_batch_key
    st.session_state.batch_started_at = now.isoformat(timespec="milliseconds")
if st.session_state.get("session_started_at") is None and st.session_state.get("learning_started"):
    st.session_state.session_started_at = now_japan().isoformat(timespec="milliseconds")

# レベル外の問題が混入していないかを実行時にも確認します。
if current_questions and any(q.get("level") != current_level for q in current_questions):
    st.error("現在のレベルと問題データのレベルが一致していません。問題を表示せず停止します。")
    st.stop()


# =========================================================
# タイトル
# =========================================================

st.title(
    "📚 中2英語 個別学習支援ドリル"
)

if not st.session_state.learning_started:
    st.markdown("## 学習を始めよう")
    st.write("取り組むレベルを選んでください。")
    st.radio(
        "どこから始めますか？",
        options=[0, 1, 2, 3],
        format_func=lambda level: {
            0: "レベル0：動名詞ってなんだろう",
            1: "レベル1：動名詞を見つけてみよう",
            2: "レベル2：動名詞を使ってみよう",
            3: "レベル3：動名詞の名人になってみよう",
        }[level],
        key="selected_start_level",
    )
    st.text_input("名前または識別用の名前（任意）", key="student_name_input")
    if st.button("学習を始める", type="primary"):
        st.session_state.current_level = int(st.session_state.selected_start_level)
        st.session_state.level_batch_number = 0
        st.session_state.batch_number = 0
        st.session_state.student_name = st.session_state.get("student_name_input", "")
        now = now_japan()
        st.session_state.session_started_at = now.isoformat(timespec="milliseconds")
        st.session_state.session_ended_at = None
        st.session_state.learning_session_id = str(uuid.uuid4())
        order_by_level = {}
        for level in range(4):
            order_by_level[str(level)] = make_question_order(level)
        st.session_state.question_order_by_level = order_by_level
        st.session_state.last_batch_question_ids = []
        st.session_state.learning_started = True
        st.session_state.active_batch_key = None
        st.session_state.batch_started_at = None
        st.rerun()
    st.stop()

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

st.text_input(
    "名前または識別用の名前",
    key="student_name_input",
)
st.session_state.student_name = st.session_state.get(
    "student_name_input",
    st.session_state.student_name,
)


# =========================================================
# 学習目標
# =========================================================

st.markdown("---")

st.markdown(
    "## 🎯 今回の学習目標"
)

level_goals = {
    0: ("動名詞ってなんだろう", "日本語の中から「～すること」にあたる部分を見つけます。"),
    1: ("動名詞を見つけてみよう", "「～すること」を表す英語の形を見つけます。"),
    2: ("動名詞を使ってみよう", "日本語の意味を考えて、動名詞を使う場面を見つけます。"),
    3: ("動名詞の名人になってみよう", "ほかの文法のルールにも気をつけながら、動名詞を選びます。"),
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

if current_level == 0:
    st.info("問題：次の文の内、動名詞（〜すること）にあたる部分に合うものを選んでください。")
else:
    st.info(MAJOR_QUESTION_INSTRUCTION)


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

        batch_question_number = index

        st.markdown(
            f"### 第{batch_question_number}問"
        )

        st.write(
            f"**{question['japanese']}**"
        )

        if question.get("english"):
            st.info(question["english"])

        option_map = {
            option["label"]: option[
                "value"
            ]

            for option
            in question["options"]
        }

        selected_label = st.radio(
            "",

            options=[option["label"] for option in question["options"]],

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
            label_visibility="collapsed",
            disabled=st.session_state.batch_submitted,
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
            "採点する",
            type="primary",
            disabled=st.session_state.batch_submitted,
        )
    )


# =========================================================
# 採点処理
# =========================================================

if submit_batch:

    batch_results = evaluate_batch(current_questions, selected_answers)
    st.session_state.batch_results = batch_results
    st.session_state.batch_submitted = True
    st.session_state.last_batch_question_ids = [item["question"]["id"] for item in batch_results]

    submitted_at = now_japan()
    # セット終了時刻と今回の最終採点時刻は、「採点する」を押した時点で記録する。
    st.session_state.session_ended_at = submitted_at.isoformat(timespec="milliseconds")
    try:
        batch_started_at = datetime.fromisoformat(st.session_state.batch_started_at)
        batch_elapsed_seconds = max(0.0, (submitted_at - batch_started_at).total_seconds())
    except (TypeError, ValueError):
        batch_elapsed_seconds = None

    for batch_question_number, item in enumerate(batch_results, start=1):
        question_id = item["question"]["id"]
        attempt_counts = st.session_state.get("attempt_counts", {})
        attempt_number = int(attempt_counts.get(question_id, 0)) + 1
        attempt_counts[question_id] = attempt_number
        st.session_state.attempt_counts = attempt_counts

        st.session_state.history.append(
            create_history_record(
                item["question"],
                item["user_answer"],
                item["result"],
                attempt_number=attempt_number,
                submitted_at=submitted_at,
                batch_elapsed_seconds=batch_elapsed_seconds,
                batch_question_number=batch_question_number,
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
                f"{index}. "
                f"🟢 正解"
            )

        elif result.get(
            "mistake_type"
        ) == "unanswered":

            st.warning(
                f"{index}. "
                f"⚪ 未回答"
            )

        else:

            st.error(
                f"{index}. "
                f"🔴 不正解"
            )

        st.markdown(
            f"**日本語：** "
            f"{question['japanese']}"
        )

        if question.get("english"):
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
    # 今回まちがえたこと
    # =====================================================

    st.markdown(
        "### 🔎 今回まちがえたこと"
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
            "action_only": "「～こと」が付かない形を選んだ",
            "gerund": "動名詞の形を選択",
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
    # レベル進行・今日の学習結果コピー
    # =====================================================

    batch_is_perfect = (
        batch_correct == batch_total
        and batch_total == QUESTIONS_PER_BATCH
    )

    st.markdown("---")

    # 今日（日本時間）に採点された学習履歴を、レベルやセッションをまたいでまとめる。
    today = now_japan().date()
    today_records = []
    for record in st.session_state.history:
        timestamp_value = record.get("submitted_at") or record.get("timestamp", "")
        try:
            record_date = datetime.fromisoformat(timestamp_value).astimezone(JAPAN_TZ).date()
        except (TypeError, ValueError):
            continue
        if record_date == today:
            today_records.append(record)

    today_start_candidates = []
    for record in today_records:
        value = record.get("session_started_at")
        if value:
            try:
                today_start_candidates.append(datetime.fromisoformat(value))
            except (TypeError, ValueError):
                pass
    today_session_start = min(today_start_candidates).isoformat(timespec="milliseconds") if today_start_candidates else None
    today_submit_candidates = []
    for record in today_records:
        value = record.get("submitted_at") or record.get("timestamp", "")
        try:
            today_submit_candidates.append(datetime.fromisoformat(value))
        except (TypeError, ValueError):
            pass
    today_last_submit = max(today_submit_candidates).isoformat(timespec="milliseconds") if today_submit_candidates else None

    def reset_to_level_selection():
        st.session_state.show_log_save_dialog = False
        st.session_state.learning_started = False
        st.session_state.session_started_at = None
        st.session_state.session_ended_at = None
        st.session_state.learning_session_id = None
        st.session_state.batch_results = None
        st.session_state.batch_submitted = False
        st.session_state.active_batch_key = None
        st.session_state.batch_started_at = None

    report_text = create_session_copy_text(
        today_records,
        session_started_at=today_session_start,
        session_ended_at=today_last_submit,
    )
    report_js = json.dumps(report_text, ensure_ascii=False)

    def render_clipboard_save_button(key_suffix):
        # Streamlitの標準ボタンではクリックとブラウザのクリップボードAPIを
        # 同じユーザー操作に結び付けられないため、iframe内のボタンで直接コピーする。
        # コピー成功後、親画面の「レベルを選ぶ」を押して画面遷移する。
        html = f"""
        <div style="width:100%;font-family:inherit;">
          <button id="save-copy-{key_suffix}" style="
            width:100%; min-height:40px; padding:0.35rem 0.75rem;
            border:1px solid rgba(128,128,128,.55); border-radius:8px;
            background:#1769d2; color:#ffffff; font-size:14px;
            font-weight:700; cursor:pointer;">
            ほぞんする
          </button>
          <div id="save-status-{key_suffix}" style="font-size:12px; margin-top:4px; text-align:center;"></div>
        </div>
        <script>
        (() => {{
          const button = document.getElementById("save-copy-{key_suffix}");
          const status = document.getElementById("save-status-{key_suffix}");
          const reportText = {report_js};
          button.addEventListener("click", async () => {{
            button.disabled = true;
            try {{
              if (navigator.clipboard && navigator.clipboard.writeText) {{
                await navigator.clipboard.writeText(reportText);
              }} else {{
                const area = document.createElement("textarea");
                area.value = reportText;
                area.style.position = "fixed";
                area.style.opacity = "0";
                document.body.appendChild(area);
                area.focus();
                area.select();
                const ok = document.execCommand("copy");
                area.remove();
                if (!ok) throw new Error("clipboard copy failed");
              }}
              status.textContent = "学習ログをクリップボードに保存しました。画面はそのままです。";
              status.style.color = "#16a34a";
              button.disabled = false;
            }} catch (e) {{
              status.textContent = "コピーできませんでした。ブラウザの権限を確認して再試行してください。";
              status.style.color = "#dc2626";
              button.disabled = false;
            }}
          }});
        }})();
        </script>
        """
        st.components.v1.html(html, height=66, scrolling=False)

    if batch_is_perfect:
        st.success(f"{current_questions[0]['level_name']}のこのセットは満点です。")
        col_action, col_save = st.columns(2)
        with col_action:
            if current_level < 3:
                if st.button(f"レベル{current_level + 1}へ進む ➡️", type="primary", use_container_width=True):
                    st.session_state.current_level = current_level + 1
                    st.session_state.level_batch_number = 0
                    st.session_state.batch_results = None
                    st.session_state.batch_submitted = False
                    st.session_state.batch_number += 1
                    st.session_state.scroll_to_top = True
                    st.rerun()
            else:
                st.success("レベル3で満点を達成しました。動名詞を使う問題に、最後まで取り組めました。")
        with col_save:
            render_clipboard_save_button("perfect")
    else:
        st.warning(f"{current_questions[0]['level_name']}は満点ではありません。次のレベルへは進みません。")
        col_action, col_save = st.columns(2)
        with col_action:
            if st.button("もう一度がんばる", type="primary", use_container_width=True):
                next_offset = (st.session_state.get("level_batch_number", 0) + 1) * QUESTIONS_PER_BATCH
                if next_offset < len(current_level_questions):
                    st.session_state.level_batch_number += 1
                else:
                    # 全問題を一巡した場合は順番を組み替え、直前と同じ5問セットを避ける。
                    previous_ids = set(st.session_state.get("last_batch_question_ids", []))
                    ids = make_question_order(current_level)
                    for _ in range(30):
                        if set(ids[:QUESTIONS_PER_BATCH]) != previous_ids:
                            break
                        ids = make_question_order(current_level)
                    st.session_state.question_order_by_level[str(current_level)] = ids
                    st.session_state.level_batch_number = 0
                st.session_state.batch_number += 1
                st.session_state.batch_results = None
                st.session_state.batch_submitted = False
                st.session_state.active_batch_key = None
                st.session_state.batch_started_at = None
                st.session_state.scroll_to_top = True
                st.rerun()
        with col_save:
            render_clipboard_save_button("retry")

    # レベル選択へ戻る操作では、まず同じ学習ログをクリップボードにコピーする。
    # コピーが成功した場合のみ、隠したStreamlitボタンを押して画面遷移する。
    level_return_html = f"""
    <div style="width:100%;font-family:inherit;">
      <button id="copy-and-return-level" style="
        width:100%; min-height:40px; padding:0.35rem 0.75rem;
        border:1px solid #d9ae2c; border-radius:8px;
        background:#f2c94c; color:#202020; font-size:14px;
        font-weight:600; cursor:pointer;">
        レベルをえらぶ
      </button>
      <div id="level-return-status" style="font-size:12px;margin-top:4px;text-align:center;"></div>
    </div>
    <script>
    (() => {{
      const button = document.getElementById("copy-and-return-level");
      const status = document.getElementById("level-return-status");
      const reportText = {report_js};
      button.addEventListener("click", async () => {{
        button.disabled = true;
        try {{
          if (navigator.clipboard && navigator.clipboard.writeText) {{
            await navigator.clipboard.writeText(reportText);
          }} else {{
            const area = document.createElement("textarea");
            area.value = reportText;
            area.style.position = "fixed";
            area.style.opacity = "0";
            document.body.appendChild(area);
            area.focus();
            area.select();
            const ok = document.execCommand("copy");
            area.remove();
            if (!ok) throw new Error("clipboard copy failed");
          }}
          status.textContent = "学習ログを保存しました。レベル選択へ戻ります。";
          status.style.color = "#16a34a";
          setTimeout(() => {{
            try {{
              const buttons = Array.from(window.parent.document.querySelectorAll("button"));
              const target = buttons.find(b => b.innerText.trim() === "レベル選択へ戻る");
              if (target) target.click();
              else {{
                status.textContent = "コピー済みです。画面を戻せませんでした。";
                button.disabled = false;
              }}
            }} catch (e) {{
              status.textContent = "コピー済みです。画面を戻せませんでした。";
              button.disabled = false;
            }}
          }}, 150);
        }} catch (e) {{
          status.textContent = "コピーできませんでした。もう一度お試しください。";
          status.style.color = "#dc2626";
          button.disabled = false;
        }}
      }});
    }})();
    </script>
    """
    st.components.v1.html(level_return_html, height=66, scrolling=False)
    # iframe内ボタンから呼び出すStreamlit側の遷移ボタンは画面上では隠す。
    st.markdown(
        """<style>
        div[data-testid="stButton"]:last-of-type { display: none !important; }
        </style>""",
        unsafe_allow_html=True,
    )
    if st.button("レベル選択へ戻る", key="level_select_return_native"):
        reset_to_level_selection()
        st.rerun()


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
            batch_question_number = record.get(
                "batch_question_number",
                question_number,
            )
            question_id = record.get("question_id", "")

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
            attempt_number = record.get("attempt_number", 1)
            level_name = record.get("level_name", "")

            if is_correct:

                status = "🟢 正解"

            elif mistake_type == (
                "unanswered"
            ):

                status = "⚪ 未回答"

            else:

                status = "🔴 不正解"

            st.markdown(
                f"### 第{batch_question_number}問 "
                f"{status}"
            )
            st.caption(f"問題番号：{question_number}｜問題ID：{question_id}")

            if level_name:
                st.caption(f"{level_name}｜{attempt_number}回目の回答")

            elapsed = record.get("seconds_from_batch_display_to_submit")
            if isinstance(elapsed, (int, float)):
                st.caption(f"セットを表示してから採点するまで：約{elapsed:.1f}秒")

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

            if record.get("english"):
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


# 今日の学習結果コピーは、採点後の学習者向けボタンから実行します。
# 開発者向けのコピー欄と手動終了ボタンは学習画面から取り除きました。


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
