# send_briefing.py

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone

import config
from database import DATABASE_URL
from models import BriefingItem
from email_sender import send_briefing_email, RECEIVER_EMAIL
from templating import create_html_content
from logger_config import logger

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def send_todays_briefing():
    """
    专门负责查询今日简报并执行发送任务的脚本。
    """
    logger.info("========================================================")
    logger.info("===== 开始执行'雅典娜'每日简报发送任务 =====")
    logger.info("========================================================")
    
    if not RECEIVER_EMAIL:
        logger.error("错误: RECEIVER_EMAIL 未在 .env 文件中配置，无法发送邮件。任务终止。")
        return

    db_session = SessionLocal()
    try:
        today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        todays_briefings = db_session.query(BriefingItem).filter(BriefingItem.created_at >= today_start).order_by(BriefingItem.created_at.desc()).all()

        if todays_briefings:
            logger.info(f"查询到 {len(todays_briefings)} 条今日简报，正在生成HTML...")
            html_content = create_html_content(todays_briefings)
            
            today_str_subject = datetime.now(timezone.utc).strftime('%Y年%m月%d日')
            subject = config.EMAIL_SUBJECT_TEMPLATE.format(date=today_str_subject)
            
            send_briefing_email(RECEIVER_EMAIL, subject, html_content)
        else:
            logger.info("数据库中没有找到今日的简报内容，无需发送邮件。")

    except Exception as e:
        logger.critical(f"发送简报邮件过程中发生严重错误: {e}", exc_info=True)
    finally:
        db_session.close()
        logger.info("数据库会话已关闭。")
        
    logger.info("===== '雅典娜'每日简报发送任务执行完毕 =====")
    logger.info("========================================================\n")


if __name__ == "__main__":
    send_todays_briefing()