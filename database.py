# database.py

# 从 sqlalchemy 导入创建数据库引擎的工具
from sqlalchemy import create_engine

# 从我们刚刚编写的 models.py 文件中，导入那个包含了所有表定义的 Base
from models import Base

# 定义我们的数据库文件路径。'sqlite:///briefings.db' 表示在当前目录下创建一个名为 briefings.db 的SQLite数据库
DATABASE_URL = "sqlite:///briefings.db"

# 创建一个数据库引擎。引擎是SQLAlchemy与数据库沟通的“翻译官”和“连接器”
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    """
    一个函数，用于创建数据库文件和我们在 Base 中定义的所有表。
    """
    print("Creating database and tables...")
    # Base.metadata.create_all 是一个神奇的命令。
    # SQLAlchemy会找到所有继承自 Base 的类，并根据它们的定义，在数据库中创建相应的表。
    # bind=engine 告诉它要在哪个数据库上执行这个操作。
    Base.metadata.create_all(bind=engine)
    print("Database and tables created successfully.")

# 这是Python脚本的一个标准写法。
# 它确保只有当这个文件被直接运行时(而不是被其他文件导入时)，下面的代码才会被执行。
if __name__ == "__main__":
    create_db_and_tables()