from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path
root_path = Path(__file__).resolve().parent.parent
env_path = root_path/".env"
load_dotenv(env_path)

API_KEY=os.getenv("API_KEY")
BASE_URL=os.getenv("BASE_URL")
MODEL="deepseek-ai/DeepSeek-V3"
if not all([API_KEY, BASE_URL, MODEL]):
    raise Exception("环境变量读取失败，请检查.evn 文件配置")

client = OpenAI(api_key = API_KEY, base_url = BASE_URL)

def generate_summary(text: str) -> str:
    """调用AI生成摘要"""
    prompt = f"""
请阅读以下PDF内容.
要求:
1. 提炼核心内容
2. 使用中文输出
3. 控制在300字以内
4. 使用项目符号展示
内容如下:
{text}
"""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages = [{"role":"user","content":prompt}],
            timeout = 20
            )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI调用失败:{str(e)}"
if __name__ == "__main__":
    test_text = "python是一门编和语言,广泛应用于数据分析,人工智能和自动人开发"
    res = generate_summary(test_text)
    print(res)