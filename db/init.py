import sqlite3

def init_database(cursor):
    # query = """
    #     DROP TABLE "Events"
    #     """
    query = """
        CREATE TABLE IF NOT EXISTS "Events" (
        "id"	TEXT NOT NULL UNIQUE,
        "title"	TEXT NOT NULL,
        "day"	TEXT NOT NULL,
        "userId"	TEXT NOT NULL,
        "done"	BOOLEAN NOT NULL,
        PRIMARY KEY("id")
    )
    """
    cursor.execute(query)