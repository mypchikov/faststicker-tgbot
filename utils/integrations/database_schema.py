SCHEMA_STATEMENTS = (
    """
    CREATE TABLE IF NOT EXISTS stickerpacks (
        tgId INTEGER NOT NULL,
        packName TEXT NOT NULL,
        createdAt INTEGER NOT NULL,
        packTitle TEXT NOT NULL,
        UNIQUE (tgId, packName)
    )
    """,
)


async def initialize_schema(db) -> None:
    for statement in SCHEMA_STATEMENTS:
        await db.execute(statement)
    await db.commit()
