# manage.py

import argparse
import logging
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, timezone

from database import DATABASE_URL
from models import Base, BriefingItem, OriginalContent
from logger_config import logger

# ==============================================================================
# "雅典娜"项目数据库管理工具
#
# 这个脚本提供了一个命令行接口，用于执行常见的数据库维护任务。
# ==============================================================================

# --- 初始化数据库连接 ---
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ==============================================================================
# --- 定义各个子命令的功能函数 ---
# ==============================================================================

def db_status():
    """显示数据库的当前状态。"""
    logger.info("--- 正在检查数据库状态 ---")
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if not tables:
            logger.info("数据库文件存在，但内部为空（没有表）。")
            logger.info("请运行 'python database.py' 来初始化表结构。")
            return

        logger.info(f"数据库连接成功: {DATABASE_URL}")
        logger.info(f"包含的表: {', '.join(tables)}")

        db_session = SessionLocal()
        try:
            briefing_count = db_session.query(BriefingItem).count()
            content_count = db_session.query(OriginalContent).count()
            logger.info(f"表 'briefings' 中有 {briefing_count} 条记录。")
            logger.info(f"表 'original_contents' 中有 {content_count} 条记录。")
        finally:
            db_session.close()

    except Exception as e:
        logger.error(f"连接或检查数据库时发生错误: {e}")
        logger.error("请确保数据库文件 'briefings.db' 存在且未损坏。")

def db_clean(days: int):
    """清理指定天数内的数据库记录。"""
    if days < 0:
        logger.error("天数必须是一个非负整数。")
        return
        
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    logger.info(f"--- 准备清理 {cutoff_date.strftime('%Y-%m-%d %H:%M:%S')} 之后的所有记录 ---")
    
    db_session = SessionLocal()
    try:
        # 查询需要被删除的记录
        items_to_delete = db_session.query(BriefingItem).filter(BriefingItem.created_at >= cutoff_date).all()
        
        if not items_to_delete:
            logger.info("没有找到需要清理的记录。")
            return

        count = len(items_to_delete)
        logger.warning(f"即将删除 {count} 条摘要记录及其关联的原文内容。")
        
        # 征求用户确认
        confirm = input("您确定要继续吗？ (yes/no): ")
        if confirm.lower() != 'yes':
            logger.info("操作已取消。")
            return

        # 执行删除
        for item in items_to_delete:
            db_session.delete(item) # SQLAlchemy的级联设置会自动删除关联的原文
        
        db_session.commit()
        logger.info(f"成功删除了 {count} 条记录。")

    except Exception as e:
        logger.error(f"清理数据库时发生错误: {e}")
        db_session.rollback()
    finally:
        db_session.close()

def db_reset():
    """危险操作：删除所有表并重建。"""
    logger.warning("="*50)
    logger.warning("这是一个危险操作！它将删除数据库中的所有数据！")
    logger.warning("="*50)
    
    confirm = input("请再次确认，输入 'RESET ALL DATA' 来继续: ")
    if confirm != 'RESET ALL DATA':
        logger.info("确认字符串不匹配，操作已取消。")
        return
        
    try:
        logger.info("正在删除所有表...")
        Base.metadata.drop_all(bind=engine)
        logger.info("正在重建所有表...")
        Base.metadata.create_all(bind=engine)
        logger.info("数据库已成功重置。")
    except Exception as e:
        logger.error(f"重置数据库时发生错误: {e}")

# ==============================================================================
# --- 主程序入口：解析命令行参数 ---
# ==============================================================================
if __name__ == "__main__":
    # 创建主解析器
    parser = argparse.ArgumentParser(description="'雅典娜'项目数据库管理工具。")
    subparsers = parser.add_subparsers(dest="command", help="可用的命令")

    # 创建 'db' 子命令的解析器
    db_parser = subparsers.add_parser("db", help="数据库相关操作")
    db_subparsers = db_parser.add_subparsers(dest="db_command", help="数据库命令")

    # 定义 'db status' 命令
    db_status_parser = db_subparsers.add_parser("status", help="显示数据库状态")
    
    # 定义 'db clean' 命令
    db_clean_parser = db_subparsers.add_parser("clean", help="清理近期数据")
    db_clean_parser.add_argument("--days", type=int, default=1, help="要清理的最近天数 (默认为1，即今天)")

    # 定义 'db reset' 命令
    db_reset_parser = db_subparsers.add_parser("reset", help="重置整个数据库（删除所有数据）")

    # 解析参数
    args = parser.parse_args()

    # 根据解析出的命令，调用对应的函数
    if args.command == "db":
        if args.db_command == "status":
            db_status()
        elif args.db_command == "clean":
            db_clean(args.days)
        elif args.db_command == "reset":
            db_reset()
        else:
            db_parser.print_help()
    else:
        parser.print_help()