import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from ..corpora.common.corpora_config import CorporaDbConfig

# this is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py, can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# Get the arguments passed in after running `alembic -x ...` to get the database's deployment stage.
command_line_arguments = context.get_x_argument(as_dictionary=True)
if "db" not in command_line_arguments:
    raise Exception(
        "We couldn't find `db` in the CLI argument when the `alembic -x` command was run. Please verify that the "
        "command was run as `alembic -x db=<db_name>` (e.g. `alembic -x db=dev upgrade head`)."
    )
database_deployment_stage = command_line_arguments["db"]


def run_migrations_offline():
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine, though an Engine is acceptable here as well.  By
    skipping the Engine creation we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the script output.
    """

    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Run migrations in 'online' mode.

    In this scenario we need to create an Engine and associate a connection with the context. We override the alembic
    config with the CorporaDbConfig information.
    """

    alembic_config = config.get_section(config.config_ini_section)
    db_config = config.get_section(database_deployment_stage)

    for key in db_config:
        alembic_config[key] = db_config[key]

    if os.environ["DEPLOYMENT_STAGE"] != database_deployment_stage:
        raise Exception(
            f"Deployment stage OS environ variable: {os.environ['DEPLOYMENT_STAGE']} and db deployment "
            f"stage specified through `db` argument: {database_deployment_stage} are different!"
        )

    alembic_config["sqlalchemy.url"] = CorporaDbConfig().database_uri

    connectable = engine_from_config(alembic_config, prefix="sqlalchemy.", poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()