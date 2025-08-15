# ai_core.py (Version 6.4 - Prompt Decoupling Final Production Edition)

# ==============================================================================
# 1. 导入工具箱 (Import necessary tools)
# ==============================================================================
import os
import logging
import json
import re
from openai import OpenAI
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from openai import APIConnectionError, RateLimitError, APIStatusError
from logger_config import logger

# ==============================================================================
# 2. 加载、验证配置与初始化客户端 (Load, Validate Configs & Initialize Client)
# ==============================================================================
load_dotenv(override=True)

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_API_BASE")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL")

if not api_key: raise ValueError("错误: OPENAI_API_KEY 未在 .env 文件中找到。")
if not DEFAULT_MODEL: raise ValueError("错误: DEFAULT_MODEL 未在 .env 文件中找到。")

client_params = {"api_key": api_key}
if base_url: client_params["base_url"] = base_url
client = OpenAI(**client_params)
logger.info(f"AI核心已初始化，将强制使用模型: '{DEFAULT_MODEL}'")

# ==============================================================================
# 3. 新增: Prompt加载函数 (NEW: Prompt Loading Function)
# ==============================================================================
def load_prompt(file_path: str) -> str:
    """从一个.prompt文件中加载Prompt模板。"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logger.critical(f"致命错误: Prompt文件未找到: {file_path}")
        raise
    except Exception as e:
        logger.critical(f"加载Prompt文件时发生致命错误: {e}")
        raise

# --- 在模块加载时，就读取好我们的Prompt模板 ---
PROMPT_TEMPLATE = load_prompt("prompts/summarizer_v1.prompt")
logger.info("摘要Prompt模板 'summarizer_v1.prompt' 加载成功。")


# ==============================================================================
# 4. 带重试的API调用函数 (Retry-enabled API call function)
# ==============================================================================
@retry(
    retry=retry_if_exception_type((APIConnectionError, RateLimitError, APIStatusError)),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    before_sleep=lambda retry_state: logger.warning(f"AI API调用失败，正在进行第 {retry_state.attempt_number} 次重试...")
)
def chat_completion_with_retry(**kwargs):
    logger.info("    ~ 正在调用AI API...")
    return client.chat.completions.create(**kwargs)


# ==============================================================================
# 5. 核心摘要函数 (Core Summarization Function - Now using the template)
# ==============================================================================
def summarize_article(article: dict):
    logger.info(f"  > ----------------------------------------------------")
    logger.info(f"  > 正在为文章生成摘要: {article['url']}")

    # --- 使用加载的模板和字符串的.format()方法来填充占位符 ---
    prompt = PROMPT_TEMPLATE.format(
        source_name=article['source_name'],
        clean_content=article['clean_content']
    )

    try:
        response = chat_completion_with_retry(
            model=DEFAULT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=500,
        )
        
        summary_text_raw = response.choices[0].message.content.strip()
        
        if not summary_text_raw:
             logger.warning(f"  - AI返回了空摘要: {article['url']}")
             return None

        text_no_br = re.sub(r'<br\s*/?>', ' ', summary_text_raw, flags=re.IGNORECASE)
        sanitized_summary = " ".join(text_no_br.split())
        
        logger.info(f"  + 摘要生成并深度净化成功。")
        
        database_ready_data = {
            'summary_data': {
                'source_url': article['url'],
                'summary_text': sanitized_summary,
                'source_name': article['source_name'],
                'model_used': DEFAULT_MODEL,
            },
            'original_content_data': {
                'content_text': article['clean_content']
            }
        }
        return database_ready_data

    except Exception as e:
        logger.error(f"  - AI API调用失败 (已重试3次): {article['url']}, 错误: {e}")
        return None

# ==============================================================================
# 6. 用于独立测试的入口 (Test Block)
# ==============================================================================
if __name__ == '__main__':
    sample_article = {
        'url': 'http://example.com/real-test-article',
        'source_name': '未来科技公报',
        'clean_content': " 探索一直在进行。今年暑期，上海静安区文化馆推出科普探索营，集结医疗、警务、消防、金融等领域专业人士，普及专业知识，或者提供沉浸式职业体验，为青少年打造既好玩又富有教育意义的体验活动。湖南长沙雨花区引导鼓励青少年走进超市，参与商品推荐、货架补货陈列、电商订单拣货以及蔬果区称重打包等环节，帮助孩子们感受课堂之外的广阔天地。开眼界、长见识、增本领，孩子开心、家长放心、社会安心。 "
    }

    logger.info(f"--- 开始独立测试 ai_core (强制使用模型: {DEFAULT_MODEL}) ---")
    
    summary_result = summarize_article(sample_article)

    if summary_result:
        logger.info("\n成功生成摘要数据:")
        # 使用json.dumps美化字典的打印输出，使其更易读
        logger.info(json.dumps(summary_result, indent=2, ensure_ascii=False))
    else:
        logger.error("\n生成摘要失败。请检查终端日志以及.env文件中的所有配置。")

    logger.info("\n--- 测试 ai_core 结束 ---")