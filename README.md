# Database Migrations with Alembic and FastAPI: A Comprehensive Guide Using Poetry

**By polymorphisma**

In web development, maintaining a growing and consistent database schema is essential. As applications expand, new features are added, performance is optimized, and errors are addressed, leading to frequent changes in the database schema. Although there are many tools available for database migrations, Alembic is one of the most popular and useful options for handling these modifications.

This article will explain how to configure and use Alembic for database migrations in a FastAPI project. Whether you're just starting out or looking to improve your existing setup, this guide will provide a clear path forward.

For more details, you can read the full article [here](https://adex.ltd/database-migrations-with-alembic-and-fastapi-a-comprehensive-guide-using-poetry).

---

## What is Alembic?

Alembic is a lightweight database migration tool that allows users to manage changes in the database schema in a version-controlled way. It provides a systematic approach for creating, managing, and applying changes using SQLAlchemy as the underlying engine.

---

## Why Use Alembic with FastAPI?

FastAPI is a modern, high-performance Python framework that is both fast and simple to use. Combining FastAPI with Alembic allows developers to handle database migrations while ensuring the database schema remains consistent with the application's data models.

---

## Steps to Set Up Alembic with FastAPI

### 1. Setting Up Your FastAPI Project

To get started, create a new FastAPI project. If you don’t already have one, set up a project directory and initialize Poetry:

```bash
mkdir fastapi-alembic-demo
cd fastapi-alembic-demo
poetry init
```

Follow the prompts to set up your project. Then, add FastAPI and Uvicorn as dependencies:

```bash
poetry add fastapi uvicorn
```

Activate the Poetry environment:

```bash
poetry shell
```

Next, create a basic FastAPI application in `main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

You can test your FastAPI app by running:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1
```

Open your browser and navigate to `localhost:8000`. You should see:

```json
{"Hello": "World"}
```

---

### 2. Adding SQLAlchemy and Alembic

Next, add SQLAlchemy and Alembic as dependencies:

```bash
poetry add sqlalchemy alembic
```

Create a new directory for your database models:

```bash
mkdir app
touch app/__init__.py
touch app/models.py
```

In `app/models.py`, define a simple SQLAlchemy model:

```python
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
```

---

### 3. Initializing Alembic

To initialize Alembic in your project, run:

```bash
alembic init alembic
```

This will create an `alembic/` directory with a configuration file (`alembic.ini`) and a migrations environment script (`env.py`).

---

### 4. Configuring Alembic

Edit the `alembic.ini` file to point to your database. Update the `sqlalchemy.url` configuration:

```ini
sqlalchemy.url = sqlite:///./test.db
```

In `alembic/env.py`, import your SQLAlchemy `Base` and set up the target metadata:

```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.models import Base

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

---

### 5. Creating and Applying Migrations

Generate your first migration script:

```bash
alembic revision --autogenerate -m "Create users table"
```

Alembic will inspect your `Base` metadata and generate a migration script in the `alembic/versions/` directory. Review the generated script to ensure it accurately represents your changes.

After the migration file is generated, apply the migration to the database:

```bash
alembic upgrade head
```

You can also integrate this process into your FastAPI project by creating a script to run the migration programmatically:

```python
# app/alembic_runner.py
import alembic.config

def run_migration():
    alembicArgs = [
        '--raiseerr',
        'upgrade', 'head',
    ]
    alembic.config.main(argv=alembicArgs)
```

Now, you can call `run_migration()` whenever you need to apply the latest migrations, such as during application startup.

---

### Example: Adding a New Column

If you want to add a new column to the `User` model, first update the model in `app/models.py`:

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    age = Column(Integer)  # New column
```

Generate a new migration:

```bash
alembic revision --autogenerate -m "Add age column to users table"
```

Review the generated migration script and then apply the migration:

```bash
alembic upgrade head
```

Alternatively, you can run the migration through the Python script:

```python
from app.alembic_runner import run_migration

run_migration()
```

---

## Conclusion

Alembic provides a robust solution for managing database migrations in web applications. By following this guide, you can now set up Alembic, generate migrations, and apply them. As you continue to develop and scale your FastAPI projects, Alembic will help you maintain database consistency.

Happy coding!

---

