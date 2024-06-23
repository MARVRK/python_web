# alembic/env.py

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# This is the Alembic Config object, which provides access to the values within the .ini file in use.
from . import models, db  # Replace with your actual application setup

config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Connect to the database using the SQLAlchemy URL from alembic.ini
engine = engine_from_config(
    config.get_section(config.config_ini_section),
    prefix='sqlalchemy.',
    poolclass=pool.NullPool)

# Ensure to add the target metadata for autogeneration of migrations
target_metadata = database.Base.metadata  # Replace `Base.metadata` with your actual metadata

# Add this line to enable Alembic to work with the database
context.configure(
    url=config.get_main_option("sqlalchemy.url"),
    target_metadata=target_metadata,
    literal_binds=True)

# When using 'autogenerate', Alembic compares the database schema as defined by 'target_metadata' against the current state of the database
# and generates the necessary changes to make the current database schema match the desired one.
