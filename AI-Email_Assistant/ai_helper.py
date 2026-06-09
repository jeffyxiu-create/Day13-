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

def generate_email(user_prompt: str)-> str:
    """
    根据用户需求生成商务邮件
    :param user_prompt: 用户输入的邮件需求
    :return: AI生成的完整邮件文件
    """
    prompt = f"""
    你是一名专业企业邮件助手,请根据下方需求生成标准商务邮件:
    {user_prompt}
    严格遵守要求:
    1. 包含邮件标题、称呼、正文、结束、落款
    2. 语气忖业、礼貌、正式
    3. 排版整洁,段落清晰
    """
    response = client.chat.completions.create(
        model = MODEL,
        messages = [
            {"role":"user","content": prompt}
        ]
    )
    return response.choices[0].message.content