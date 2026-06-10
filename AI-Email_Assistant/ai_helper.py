from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
import os

root_path = Path(__file__).resolve().parent.parent
env_path = root_path/".env"
load_dotenv(env_path)

API_KEY=os.getenv("API_KEY")
BASE_URL=os.getenv("BASE_URL")
MODEL="deepseek-ai/DeepSeek-V3"

if not all([API_KEY, BASE_URL, MODEL]):
    raise Exception("环境变量读取失败，请检查.evn 文件配置")

client = OpenAI(api_key = API_KEY, base_url = BASE_URL)

def get_ai_email(prompt_text):
    """
    接收拼接好的提示词,返回AI结果
    出错则返回带ERROR 标记的字符串
    """
    try:
        response = client.chat.completions.create(
            model = MODEL,
            messages = [
            {"role":"user","content": prompt_text}
            ],
            temperature = 0.7
        )
        return response.choices[0].message.content.strip()

    except Exception as e :
        return f"ERROR:{str(e)}"

