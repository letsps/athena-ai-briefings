# alembic/env.py (SQLAlchemy 2.0 Compatible Final Edition)

from __future__ import with_statement

import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# ==============================================================================
# 核心修复: 确保Alembic能够找到我们的项目模块和Base对象
# ==============================================================================
# 将项目根目录添加到sys.path，这样Alembic在运行时就能找到models.py等文件。
# os.path.dirname(__file__) 是当前文件(env.py)的目录
# os.path.abspath(...) 得到绝对路径
# os.path.join(..., '..') 向上回退一级，即项目根目录
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 从我们项目的 models.py 文件中导入 Base 对象
# Base 包含了我们所有SQLAlchemy模型的元数据，Alembic需要它来检测Schema变化
from models import Base
target_metadata = Base.metadata # <--- 核心修改: Alembic现在需要的是Base的.metadata属性


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import Base
# target_metadata = Base.metadata # This is the original line that might cause issues

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}), # Added {} for safer access
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata, # <--- 核心修改: 现在这里直接使用我们上面定义的 target_metadata
            version_table_schema=connectable.dialect.default_schema_name, # Added this for explicit schema
            # include_schemas=True, # Often not needed with default_schema_name set
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()