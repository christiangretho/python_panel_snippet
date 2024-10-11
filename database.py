import psycopg2
import psycopg2.extras
import os


DB = {
    "DEV_DB": {
        "HOSTNAME": "localhost",
        "DATABASE": "panel_playwrite_db_dev",
        "USERNAME": "admin",
        "PASSWORD": "password",
        "PORT_ID": 5432,
    },
    "TEST_DB": {
        "HOSTNAME": "localhost",
        "DATABASE": "panel_playwrite_db_test",
        "USERNAME": "admin",
        "PASSWORD": "password",
        "PORT_ID": 5432,
    },
}

env = os.getenv("DB_ENV", "DEV_DB")
print(env)
HOSTNAME, DATABASE, USERNAME, PASSWORD, PORT_ID = (
    DB[f"{env}"]["HOSTNAME"],
    DB[f"{env}"]["DATABASE"],
    DB[f"{env}"]["USERNAME"],
    DB[f"{env}"]["PASSWORD"],
    DB[f"{env}"]["PORT_ID"],
)
print(DATABASE)


class Database:
    def __init__(
        self,
        hostname=HOSTNAME,
        database=DATABASE,
        username=USERNAME,
        pwd=PASSWORD,
        port_id=PORT_ID,
    ):
        self.hostname = hostname
        self.database = database
        self.username = username
        self.pwd = pwd
        self.port_id = port_id
        self.conn = None

    def connect(self):
        with psycopg2.connect(
            host=self.hostname,
            dbname=self.database,
            user=self.username,
            password=self.pwd,
            port=self.port_id,
        ) as conn:
            self.conn = conn

    def close(self):
        if self.conn:
            self.conn.close()

    def query_db(self, query, record=None):
        try:
            with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(query, record)
                self.conn.commit()
        except psycopg2.DatabaseError as e:
            print(f"Database error: {e}")
        except psycopg2.OperationalError as e:
            print(f"Operational error: {e}")

    def select_db(self, query, record=None):
        try:
            with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(query, record)
                return cur.fetchall()
        except psycopg2.DatabaseError as e:
            print(f"Database error: {e}")
        except psycopg2.OperationalError as e:
            print(f"Operational error: {e}")

    def select_one_db(self, query, record=None):
        try:
            with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(query, record)
                return cur.fetchone()
        except psycopg2.DatabaseError as e:
            print(f"Database error: {e}")
        except psycopg2.OperationalError as e:
            print(f"Operational error: {e}")

    def create_snippet(self, title: str, language: str, code: str):
        insert_script = (
            "INSERT INTO snippet_table (title, language, code) VALUES( %s, %s, %s)"
        )
        record = (title, language, code)
        self.query_db(insert_script, record)
        return self.get_snippet(title)

    def get_snippet(self, title):
        query = f"SELECT * FROM snippet_table WHERE title='{title}'"

        result = self.select_one_db(query)
        return result

    def list_snippets(
        self,
    ):
        query = "SELECT * FROM snippet_table"

        result = self.select_db(query)
        return result

    def update_snippet(self, snippet_id, code):
        query = "UPDATE snippet_table SET code = %s WHERE snippet_id = %s"
        record = (code, snippet_id)
        self.query_db(query, record)

    def delete_snippet(self, snippet_id) -> None:
        query = f"DELETE FROM snippet_table WHERE snippet_id={snippet_id}"
        self.query_db(query)

    def create_tables(self):
        create_snippet_table = """CREATE TABLE IF NOT EXISTS snippet_table (
                snippet_id SERIAL PRIMARY KEY,
                title TEXT NOT NULL UNIQUE,
                code TEXT NOT NULL,
                language varchar(40)
            );"""
        self.query_db(create_snippet_table)

    def drop_tables(self):
        drop_snippet_table = "DROP TABLE IF EXISTS snippet_table"
        self.query_db(drop_snippet_table)


def __initialize_db__() -> None:
    db = Database()
    db.connect()
    db.drop_tables()
    db.create_tables()
    db.close()


if __name__ == "__main__":
    print("initializing DB")
    __initialize_db__()
