# data_collector.py (Version 2.1 - with Professional Logging)

# ==============================================================================
# 1. 导入工具箱 (Import necessary tools)
# ==============================================================================
import feedparser
import trafilatura
from tenacity import retry, stop_after_attempt, wait_exponential

# --- 核心改动: 从我们的新模块导入已配置好的logger实例 ---
from logger_config import logger

# ==============================================================================
# 2. 为网络请求函数包裹上重试"盔甲" (Retry-enabled network function)
# ==============================================================================
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    before_sleep=lambda retry_state: logger.warning(f"下载失败，正在进行第 {retry_state.attempt_number} 次重试...")
)
def fetch_url_with_retry(url: str):
    """
    一个带重试逻辑的网页下载函数。
    """
    logger.info(f"    ~ 正在下载: {url}")
    return trafilatura.fetch_url(url)


# ==============================================================================
# 3. 核心函数 (Core Function - Now using the central logger)
# ==============================================================================
def fetch_and_clean_articles(rss_url: str, max_articles: int = 5):
    """
    从给定的RSS源URL中获取、清洁并验证文章。(版本 2.1)
    """
    logger.info(f"开始处理RSS源: {rss_url}")
    
    feed = feedparser.parse(rss_url)
    
    if feed.bozo:
        logger.error(f"无法解析RSS源: {rss_url}. 异常: {feed.bozo_exception}")
        return []

    source_name = feed.feed.title if 'title' in feed.feed else "未知来源"
    logger.info(f"成功解析到信源: '{source_name}'")

    processed_articles = []
    
    for entry in feed.entries[:max_articles]:
        article_url = entry.link
        logger.info(f"  > ----------------------------------------------------")
        logger.info(f"  > 正在处理文章: {article_url}")

        try:
            downloaded_html = fetch_url_with_retry(article_url)
            
            if not downloaded_html:
                logger.warning(f"  - 下载成功但内容为空: {article_url}")
                continue

            clean_text = trafilatura.extract(downloaded_html)

            if not clean_text:
                logger.warning(f"  - 无法从HTML中提取正文: {article_url}")
                continue

            min_content_length = 200 # 应该从config.py导入，下一步可以优化
            if len(clean_text) < min_content_length:
                logger.warning(f"  - 内容太短 ({len(clean_text)} chars)，已跳过: {article_url}")
                continue

            logger.info(f"  + 内容验证通过。长度: {len(clean_text)} chars.")
            processed_articles.append({
                'url': article_url,
                'source_name': source_name,
                'clean_content': clean_text
            })

        except Exception as e:
            logger.error(f"  - 下载文章失败 (已重试3次): {article_url}, 错误: {e}")
            continue

    logger.info(f"RSS源处理完成。共获取到 {len(processed_articles)} 篇有效文章。")
    return processed_articles

# ==============================================================================
# 4. 测试代码 (Test Block - Now using the central logger)
# ==============================================================================
if __name__ == '__main__':
    test_rss_url = "http://www.ruanyifeng.com/blog/atom.xml"
    
    logger.info(f"--- 开始独立测试 data_collector (数据源: {test_rss_url}) ---")
    articles = fetch_and_clean_articles(test_rss_url)
    
    if articles:
        logger.info(f"\n成功获取到 {len(articles)} 篇文章。")
        
        first_article = articles[0]
        logger.info("\n--- 第一篇文章预览 ---")
        logger.info(f"URL: {first_article['url']}")
        logger.info(f"来源: {first_article['source_name']}")
        logger.info(f"内容预览 (前200字符): \n{first_article['clean_content'][:200]}...")
    else:
        logger.warning("\n未能获取到任何有效文章。请检查RSS链接或网络连接。")
        
    logger.info("\n--- 测试 data_collector 结束 ---")