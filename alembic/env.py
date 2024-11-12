import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy import pool
from alembic import context
from community_telegram_bot.database.models import Base, User  # Make sure to import your models

# Load the Alembic configuration
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Add your models' MetaData object here
target_metadata = Base.metadata

DATABASE_URL = config.get_main_option("sqlalchemy.url")
engine = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)

def run_migrations():
    """Run migrations in 'online' mode."""
    connectable = engine.connect()
    with connectable as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()

if __name__ == "__main__":
    asyncio.run(run_migrations())
