from collections.abc import Iterable
from os import environ

from sqlalchemy import MetaData, inspect, select, text, desc
from sqlalchemy.engine import Engine, create_engine, make_url


def reflect_tables(
    from_engine: Engine,
    to_engine: Engine,
    excluded_tables: Iterable[str] | None = None,
    include_schemas: Iterable[str] = None,
):
    """
    Загружает данные таблиц из одной БД в другую.
    Обратите внимание, что структуры таблиц должны совпадать между БД, в противном случае сначала загрузите миграции

    :param from_engine: engine БД, из которой берутся данные
    :param to_engine: engine БД, в которую зальются данные
    :param excluded_tables: Список таблиц, которые необходимо исключить из выгрузки
    """
    if excluded_tables is None:
        excluded_tables = tuple()

    meta = MetaData()
    inspector = inspect(to_engine)

    if include_schemas is None:
        include_schemas = filter(
            lambda schema: not schema.startswith("pg_") and not schema == "information_schema",
            inspector.get_schema_names(),
        )

    for schema in include_schemas:
        meta.reflect(from_engine, schema=schema)

    with from_engine.connect() as from_conn, to_engine.connect() as to_conn:
        sorted_tables = list(filter(lambda table: table.name not in excluded_tables, meta.sorted_tables))

        for table in sorted_tables:
            if not inspector.has_table(table_name=table.name, schema=table.schema):
                raise Exception(f"Not found {table.name} table")

            print(f'TRUNCATE "{table.schema}.{table.name}"')
            to_conn.execute(text(f"TRUNCATE {table.schema}.{table.name} CASCADE"))
            stmt = select(table)
            if any("is_group" == c.name for c in table.c):
                stmt = stmt.order_by(desc(table.c.is_group))
            if any("created_at" == c.name for c in table.c):
                stmt = stmt.order_by(table.c.created_at)

            with from_conn.execution_options(yield_per=10000).execute(stmt) as result:
                print(f'INSERT "{table.schema}.{table.name}"')
                for partition in result.mappings().partitions():
                    to_conn.execute(table.insert(), partition)
            to_conn.commit()


if __name__ == "__main__":
    from_url = make_url(environ.get("DATABASE_URL_PROD", ""))
    to_url = make_url(environ.get("DATABASE_URL", ""))

    if all(
        (
            from_url.host == to_url.host,
            from_url.database == to_url.database,
        )
    ):
        print("Database hosts match")
    else:
        reflect_tables(
            from_engine=create_engine(from_url),
            to_engine=create_engine(to_url),
            excluded_tables=("alembic_version", "logs"),
        )
