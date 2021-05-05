import sqlite3
import os

db_abs_path = os.path.dirname(os.path.realpath(__file__)) + '/safety.db'
conn = sqlite3.connect(db_abs_path)
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS monitor")
c.execute("DROP TABLE IF EXISTS department")
c.execute("DROP TABLE IF EXISTS position")
c.execute("DROP TABLE IF EXISTS reqs")
c.execute("DROP TABLE IF EXISTS procedures")
c.execute("DROP TABLE IF EXISTS comments")

c.execute("""CREATE TABLE department(
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    name            TEXT
)""")
c.execute("""CREATE TABLE position(
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    name            TEXT,
                    department_id    INTEGER,
                    FOREIGN KEY(department_id) REFERENCES department(id)
)""")
c.execute("""CREATE TABLE reqs(
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    name            TEXT
)""")
c.execute("""CREATE TABLE procedures(
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    name            TEXT,
                    req_id     INTEGER,
                    FOREIGN KEY(req_id) REFERENCES reqs(id)
)""")
c.execute("""CREATE TABLE monitor(
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    observe         INTEGER,
                    bad_case        INTEGER,
                    obs_period      TEXT,
                    req_id          INTEGER,
                    procedure_id    INTEGER,
                    department_id   INTEGER,
                    position_id     INTEGER,
                    FOREIGN KEY(req_id) REFERENCES reqs(id),
                    FOREIGN KEY(procedure_id) REFERENCES procedures(id),
                    FOREIGN KEY(department_id) REFERENCES department(id),
                    FOREIGN KEY(position_id) REFERENCES position(id)
)""")
c.execute("""CREATE TABLE comments(
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    content         TEXT,
                    monitor_id         INTEGER,
                    FOREIGN KEY(monitor_id) REFERENCES monitor(id)
)""")
reqs = [
    ("IPSG1",),
    ("IPSG2",),
    ("IPSG3",)
]

c.executemany("INSERT INTO reqs (name) VALUES (?)", reqs)

procedures = [
    ("Fruit", 1),
    ("Dairy product", 1),
    ("Cassette", 2),
    ("Phone", 2),
    ("TV", 2),
    ("Historical fiction", 3),
    ("Science fiction", 3)
]
c.executemany("INSERT INTO procedures (name, req_id) VALUES (?,?)", procedures)

conn.commit()
conn.close()

print("Database  safety.db is created and initialized.")
# print("You can see the tables with the show_tables.py script")
