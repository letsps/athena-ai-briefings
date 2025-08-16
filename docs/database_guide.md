## 🗄️ 数据库管理指南

“雅典娜”项目使用 SQLite 数据库 (`briefings.db`) 进行数据持久化，并通过 SQLAlchemy (ORM) 进行交互。为了实现数据库结构的平滑演进和数据的安全维护，我们采用了 **Alembic** 作为数据库迁移工具，并构建了定制的 **`manage.py`** 脚本。

### 1. 数据库版本管理 (使用 Alembic)

Alembic 允许我们像管理代码一样管理数据库的结构（Schema）。每次数据库结构的变更（例如，新增表、增加列、修改列类型等），都将通过生成并应用一个“迁移脚本”来完成。

**核心理念：**
*   **版本化**: 数据库的Schema有版本，每次修改都会生成一个新的版本。
*   **非破坏性**: 大部分操作旨在保留现有数据的前提下修改结构。
*   **可追溯与回滚**: 可以清晰查看Schema演变历史，并在需要时回滚到旧版本。

**基本流程：**

1.  **修改您的数据模型 (`models.py`)**：
    当您需要对数据库结构进行任何修改时（例如，在 `models.py` 的 `BriefingItem` 类中增加一个新列 `published_at`），请直接修改 `models.py` 文件中的对应Python类定义。

2.  **生成迁移脚本**：
    在修改 `models.py` 之后，回到您的项目根目录，在终端中运行以下命令。Alembic 会自动检测 `models.py` 和当前数据库Schema之间的差异，并生成一个包含这些变更的Python迁移脚本。
    ```bash
    alembic revision --autogenerate -m "描述本次变更的内容"
    # 示例：alembic revision --autogenerate -m "Add published_at column to BriefingItem"
    ```
    成功后，您会在 `alembic/versions/` 目录下看到一个新的 `.py` 文件。

3.  **审查迁移脚本（🚨 关键人工介入点 🚨）**：
    **这是最重要的一步。** 在应用任何迁移之前，**请务必打开 `alembic/versions/` 目录下新生成的 `.py` 文件，仔细审查其内容。**
    *   检查 `upgrade()` 函数中，Alembic生成的SQL操作 (`op.add_column`, `op.create_table` 等) 是否准确反映了您的意图。
    *   检查 `downgrade()` 函数（用于回滚）是否也正确。
    *   **为什么重要？** 尽管 `autogenerate` 很智能，但它并非完美。有时，Alembic可能无法完全理解复杂的Schema变更，或者可能生成一些您不期望的操作。人工审查可以防止数据丢失或意外的结构变更。

4.  **应用迁移**：
    审查确认无误后，在终端中运行以下命令，将本次Schema变更应用到您的 `briefings.db` 数据库中。
    ```bash
    alembic upgrade head
    ```
    这会将您的数据库结构升级到最新的版本。

5.  **查看迁移历史 (可选)**：
    您可以随时查看数据库的Schema演变历史。
    ```bash
    alembic history
    ```

### 2. 数据库数据管理 (使用 `manage.py`)

`manage.py` 脚本是您的数据库“瑞士军刀”，提供了一系列命令来管理数据库中的数据内容。

**基本命令：**

*   **查看数据库状态**
    ```bash
    python manage.py db status
    ```
    这个命令会显示数据库文件是否存在、包含哪些表，以及 `briefings` 和 `original_contents` 表中的记录数量。

*   **清理近期数据（用于测试或重新抓取）**
    ```bash
    python manage.py db clean
    # 默认清理最近1天（即今天）产生的数据。
    ```
    ```bash
    python manage.py db clean --days 3
    # 清理最近3天内产生的所有数据。
    ```
    **注意：** 此命令会删除匹配条件的**所有摘要记录及其关联的原文内容**。在执行前会要求您输入 `yes` 进行确认。

*   **重置整个数据库（删除所有数据）**
    ```bash
    python manage.py db reset
    ```
    **🚨 极其危险的操作！** 这个命令会删除 `briefings.db` 中所有表的所有数据，然后重建空的表结构。它将使您的数据库恢复到刚初始化时的空白状态。
    **您需要精确输入 `RESET ALL DATA` 进行双重确认才能执行。请务必谨慎使用。**

---

这份文档现在已经准备就绪。它将成为“雅典娜”项目的一个核心组成部分。