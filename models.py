# models.py (Version 1.1 - Final Commented Edition)

# ==============================================================================
# 1. 导入工具箱 (Import necessary tools)
# ==============================================================================
from sqlalchemy import (
    Column,         # 用于定义数据库的列
    Integer,        # 整数类型
    String,         # 短字符串类型
    Text,           # 长文本类型
    DateTime,       # 日期和时间类型
    ForeignKey      # 用于定义外键，建立表之间的关联
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone

# ==============================================================================
# 2. 创建声明性基类 (Create the Declarative Base)
# ==============================================================================
# 这是所有数据模型类(即数据表)都必须继承的父类。
# SQLAlchemy通过它来识别和管理我们项目中的所有表。
Base = declarative_base()

# ==============================================================================
# 3. 定义数据模型/表 (Define Data Models / Tables)
# ==============================================================================

class BriefingItem(Base):
    """
    摘要信息表 (Briefings Table)
    这是我们系统的核心，存储AI生成的摘要和所有相关的元数据。
    每个 BriefingItem 对象在代码中就代表数据库中的一条摘要记录。
    """
    # __tablename__ 是一个特殊变量，用于明确指定这个Python类对应到数据库中的表名。
    __tablename__ = 'briefings'

    # --- 定义表中的列 (Columns) ---
    
    # id: 主键，每条记录的唯一标识符。
    # primary_key=True 表示它是主键，数据库会自动处理它的唯一性和索引。
    # 通常数据库会自动使其自增。
    id = Column(Integer, primary_key=True)
    
    # source_url: 存储原文的URL。
    # unique=True 是一个非常重要的约束，它确保了我们不会重复抓取和存储同一篇文章。
    # nullable=False 表示这一列不能为空，每条摘要都必须有来源。
    source_url = Column(String, unique=True, nullable=False)
    
    # summary_text: 存储AI生成的摘要内容。
    # 使用Text类型，因为它能存储比String更长的文本。
    summary_text = Column(Text, nullable=False)
    
    # source_name: 信源的名称，例如 '阮一峰的网络日志'。方便未来按来源进行筛选和展示。
    source_name = Column(String)
    
    # model_used: 记录生成这条摘要时使用的AI模型名称，例如 'hunyuan-turbo-latest'。
    # 这个元数据对于未来的调试、成本分析和效果对比至关重要。
    model_used = Column(String)
    
    # created_at: 记录这条数据被创建的时间戳。
    # default=lambda: datetime.now(timezone.utc) 是一个强大的功能：
    # 当我们创建一条新记录时，如果没提供这个字段，数据库会自动调用这个lambda函数，
    # 填入当前的、带UTC时区的标准时间。这修复了之前的DeprecationWarning。
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # --- 定义对象间的关系 (Relationships) ---
    
    # original_content: 这是一个“魔法”属性，它不在数据库的这张表中真实存在。
    # 它允许我们在Python代码中，通过一个BriefingItem对象(比如 a_briefing)，
    # 直接用 a_briefing.original_content 的方式，访问到与之关联的OriginalContent对象。
    # back_populates="briefing" 告诉SQLAlchemy，这个关系与OriginalContent类中的"briefing"属性是配对的。
    # uselist=False 表示这是一个“一对一”的关系（一条摘要只有一个原文）。
    # cascade="all, delete-orphan" 是一个级联操作：当我们删除一条摘要时，与之关联的原文也会被自动删除。
    original_content = relationship("OriginalContent", back_populates="briefing", uselist=False, cascade="all, delete-orphan")


class OriginalContent(Base):
    """
    原文备份表 (Original Contents Table)
    用于存储文章的完整原文，以防止源链接失效，并为未来的再处理提供数据基础。
    """
    __tablename__ = 'original_contents'

    id = Column(Integer, primary_key=True)
    
    # content_text: 存储从网页中提取出的、干净的纯文本内容。
    content_text = Column(Text, nullable=False)
    
    # briefing_id: 外键，这是实现两张表“一对一”关联的核心。
    # ForeignKey('briefings.id') 建立了一个数据库层面的约束：
    # 这一列的值，必须是 'briefings' 表中某条记录的 'id' 值。
    briefing_id = Column(Integer, ForeignKey('briefings.id'))

    # briefing: 与BriefingItem中的original_content配对的关系属性。
    # 它允许我们通过一个OriginalContent对象(比如 an_original_content)，
    # 用 an_original_content.briefing 的方式，反向访问到它所属的那个BriefingItem对象。
    briefing = relationship("BriefingItem", back_populates="original_content")