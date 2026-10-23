import sqlite3

import sqlite_vec

db = sqlite3.connect(":memory:")
db.enable_load_extension(True)
sqlite_vec.load(db)
db.enable_load_extension(False)


SCHEMA = """

PRAGMA foreign_keys = ON;
PRAGMA cache_size = -64000;
PRAGMA synchronous = NORMAL;
PRAGMA temp_store = MEMORY;
PRAGMA journal_mode=WAL;

create table anime (
    id integer primary key,
    anime_id integer UNIQUE,
    mal_id integer UNIQUE,
    score NUMERIC(4, 2)
);

create table anime_titles(

    anime_id integer primary key,
    title VARCHAR(255) NOT NULL,
    english_title VARCHAR(255) UNIQUE,
    japanese_title VARCHAR(255) UNIQUE,

    FOREIGN KEY (anime_id) REFERENCES Employees(id)
);

create table anime_data(

    anime_id integer primary key,
    type               VARCHAR(50),
    episodes           INTEGER,
    duration           INTEGER,
    popularity_rank    INTEGER,
    season_year        SMALLINT,

    FOREIGN KEY (anime_id) REFERENCES Employees(id)
);

create table anime_info(
    anime_id integer primary key,
    tags TEXT
    genres TEXT
    dense_text TEXT,
    synopsis TEXT,
    FOREIGN KEY (anime_id) REFERENCES Employees(id)
);

create idx_anime_

"""
cursor = db.cursor()

cursor.executescript(SCHEMA)
print(
    cursor.execute("""SELECT name FROM sqlite_master
    WHERE type='table';""").fetchall()
)
