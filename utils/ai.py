from openai import OpenAI
import os
import json
from dotenv import load_dotenv
import re

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

def generate_dummy_answers(correct_answer):
    """正解に基づいて3つのダミーの答えを生成する関数。"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "以下に示すのは正しい答えです。この答えと関連はあるが、明確に間違っている3つの異なる答えを作成してください。答えは現実的で、一般的な誤解に基づくものであるべきです。また出力の形式は答えのリストであるべきです。"},
                {"role": "user", "content": correct_answer}
            ],
            max_tokens=60,
            temperature=0.7
        )
        print(response)
        correct_answer = [choice.message.content for choice in response.choices]
        print(f"ダミーの答えを生成しました: {correct_answer}")
        return correct_answer
    except Exception as e:
        print(f"ダミーの答えの生成中にエラーが発生しました: {e}")
        return []