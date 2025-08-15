# main.py (Version 3.0 - Data Pipeline Only)

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone

import config
from database import DATABASE_URL
from models import BriefingItem, OriginalContent
from data_collector import fetch_and_clean_articles
from ai_core import summarize_article
from logger_config import logger

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def run_data_pipeline():
    """
    执行纯粹的数据处理流水线：采集 -> ETL -> 增强 -> 持久化。
    """
    logger.info("========================================================")
    logger.info("===== 开始执行'雅典娜'数据处理流水线 =====")
    logger.info("========================================================")
    
    db_session = SessionLocal()
    new_items_count = 0
    try:
        all_articles = []
        for feed_url in config.RSS_FEEDS:
            articles_from_feed = fetch_and_clean_articles(
                feed_url, 
                max_articles=config.MAX_ARTICLES_PER_FEED
            )
            all_articles.extend(articles_from_feed)
        
        logger.info(f"所有RSS源处理完毕，共获取到 {len(all_articles)} 篇有效文章。")

        if all_articles:
            for article in all_articles:
                exists = db_session.query(BriefingItem).filter(BriefingItem.source_url == article['url']).first()
                if exists:
                    logger.info(f"文章已存在于数据库中，跳过: {article['url']}")
                    continue
                
                processed_data = summarize_article(article)
                
                if processed_data:
                    try:
                        new_briefing = BriefingItem(**processed_data['summary_data'])
                        new_content = OriginalContent(**processed_data['original_content_data'])
                        new_briefing.original_content = new_content
                        db_session.add(new_briefing)
                        db_session.commit()
                        new_items_count += 1
                        logger.info(f"成功存入新摘要: {article['url']}")
                    except IntegrityError:
                        db_session.rollback()
                        logger.warning(f"数据库完整性错误，可能文章已存在（并发），已回滚: {article['url']}")
                    except Exception as e:
                        db_session.rollback()
                        logger.error(f"存入数据库时发生未知错误: {e}", exc_info=True)
    except Exception as e:
        logger.critical(f"数据处理流水线执行过程中发生严重错误: {e}", exc_info=True)
    finally:
        db_session.close()
        logger.info("数据库会话已关闭。")

    logger.info(f"===== '雅典娜'数据处理流水线执行完毕，共存入 {new_items_count} 条新数据 =====")
    logger.info("========================================================\n")

if __name__ == "__main__":
    run_data_pipeline()