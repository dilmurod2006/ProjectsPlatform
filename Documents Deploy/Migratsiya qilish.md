<!-- FAST API ni Migratsiya qilish -->
# Migratsiya qilish
    1. alembic init
    2. alembic.ini fileni sozlash
    3. /migrations/env.py fileni sozlash
    4. alembic revision --autogenerate -m "initial migration"
    5. alembic upgrade head


# alembic.ini file:


    # A generic, single database configuration.

    [alembic]
    # path to migration scripts
    script_location = migrations

    # template used to generate migration file names; The default value is %%(rev)s_%%(slug)s
    # Uncomment the line below if you want the files to be prepended with date and time
    # see https://alembic.sqlalchemy.org/en/latest/tutorial.html#editing-the-ini-file
    # for all available tokens
    # file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s

    # sys.path path, will be prepended to sys.path if present.
    # defaults to the current working directory.
    prepend_sys_path = .

    # timezone to use when rendering the date within the migration file
    # as well as the filename.
    # If specified, requires the python>=3.9 or backports.zoneinfo library.
    # Any required deps can installed by adding `alembic[tz]` to the pip requirements
    # string value is passed to ZoneInfo()
    # leave blank for localtime
    # timezone =

    # max length of characters to apply to the
    # "slug" field
    # truncate_slug_length = 40

    # set to 'true' to run the environment during
    # the 'revision' command, regardless of autogenerate
    # revision_environment = false

    # set to 'true' to allow .pyc and .pyo files without
    # a source .py file to be detected as revisions in the
    # versions/ directory
    # sourceless = false

    # version location specification; This defaults
    # to migrations/versions.  When using multiple version
    # directories, initial revisions must be specified with --version-path.
    # The path separator used here should be the separator specified by "version_path_separator" below.
    # version_locations = %(here)s/bar:%(here)s/bat:migrations/versions

    # version path separator; As mentioned above, this is the character used to split
    # version_locations. The default within new alembic.ini files is "os", which uses os.pathsep.
    # If this key is omitted entirely, it falls back to the legacy behavior of splitting on spaces and/or commas.
    # Valid values for version_path_separator are:
    #
    # version_path_separator = :
    # version_path_separator = ;
    # version_path_separator = space
    version_path_separator = os  # Use os.pathsep. Default configuration used for new projects.

    # set to 'true' to search source files recursively
    # in each "version_locations" directory
    # new in Alembic version 1.10
    # recursive_version_locations = false

    # the output encoding used when revision files
    # are written from script.py.mako
    # output_encoding = utf-8

    sqlalchemy.url = postgresql://%(DB_USER)s:%(DB_PASSWORD)s@%(DB_HOST)s:%(DB_PORT)s/%(DB_NAME)s


    [post_write_hooks]
    # post_write_hooks defines scripts or Python functions that are run
    # on newly generated revision scripts.  See the documentation for further
    # detail and examples

    # format using "black" - use the console_scripts runner, against the "black" entrypoint
    # hooks = black
    # black.type = console_scripts
    # black.entrypoint = black
    # black.options = -l 79 REVISION_SCRIPT_FILENAME

    # lint with attempts to fix using "ruff" - use the exec runner, execute a binary
    # hooks = ruff
    # ruff.type = exec
    # ruff.executable = %(here)s/.venv/bin/ruff
    # ruff.options = --fix REVISION_SCRIPT_FILENAME

    # Logging configuration
    [loggers]
    keys = root,sqlalchemy,alembic

    [handlers]
    keys = console

    [formatters]
    keys = generic

    [logger_root]
    level = WARN
    handlers = console
    qualname =

    [logger_sqlalchemy]
    level = WARN
    handlers =
    qualname = sqlalchemy.engine

    [logger_alembic]
    level = INFO
    handlers =
    qualname = alembic

    [handler_console]
    class = StreamHandler
    args = (sys.stderr,)
    level = NOTSET
    formatter = generic

    [formatter_generic]
    format = %(levelname)-5.5s [%(name)s] %(message)s
    datefmt = %H:%M:%S



# migrations/env.py file:


    from logging.config import fileConfig

    from sqlalchemy import engine_from_config
    from sqlalchemy import pool

    from alembic import context

    from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
    from models.models import metadata

    # this is the Alembic Config object, which provides
    # access to the values within the .ini file in use.
    config = context.config

    section = config.config_ini_section
    config.set_section_option(section, "DB_NAME", DB_NAME)
    config.set_section_option(section, "DB_USER", DB_USER)
    config.set_section_option(section, "DB_PASSWORD", DB_PASSWORD)
    config.set_section_option(section, "DB_HOST", DB_HOST)
    config.set_section_option(section, "DB_PORT", DB_PORT)

    # Interpret the config file for Python logging.
    # This line sets up loggers basically.
    if config.config_file_name is not None:
        fileConfig(config.config_file_name)

    # add your model's MetaData object here
    # for 'autogenerate' support
    # from myapp import mymodel
    # target_metadata = mymodel.Base.metadata
    target_metadata = metadata

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
        """Run migrations in 'online' mode.

        In this scenario we need to create an Engine
        and associate a connection with the context.

        """
        connectable = engine_from_config(
            config.get_section(config.config_ini_section, {}),
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


# Modelni migratsiyalash har doim

    1. alembic revision --autogenerate -m "initial migration"
    2. alembic upgrade head