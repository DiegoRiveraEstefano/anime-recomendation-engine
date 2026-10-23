from ctypes import cast
from pathlib import Path

import polars as pl

DATA_PATH = Path("data/")

ANIME_LIST = DATA_PATH / "anime_data.csv"

df_anime_data = pl.read_csv(
    ANIME_LIST,
    schema_overrides={
        "anime_id": pl.Float32,
        "mal_id": pl.Float32,
        "title": pl.String,
        "english_title": pl.String,
        "japanese_title": pl.String,
        "user_preferred_title": pl.String,
        "type": pl.String,  # to enum
        "episodes": pl.Float32,
        "duration": pl.Float32,
        "status": pl.String,  # to enum
        "source": pl.String,  # to enum
        "season": pl.String,  # WINTER 2025
        "season_year": pl.UInt16,
        "studios": pl.String,  # Aniplex;A-1 Pictures;Netmarble;D&C MEDIA;Kakao piccoma;Crunchyroll
        "main_studios": pl.String,
        "genres": pl.String,  # Action;Adventure;Fantasy
        "tags": pl.String,  # Urban Fantasy;Dungeon;Male Protagonist;Necromancy;Magic;Super Power;Cultivation;Creature Taming;Swordplay;Gore
        "rating": pl.String,  # Empty
        "score": pl.Float32,
        "mean_score": pl.Float32,
        "rank": pl.Float32,
        "popularity": pl.UInt32,
        "popularity_rank": pl.Float32,
        "members": pl.UInt32,
        "favorites": pl.UInt32,
        "watching": pl.UInt32,
        "completed": pl.UInt32,
        "on_hold": pl.UInt32,
        "dropped": pl.UInt32,
        "plan_to_watch": pl.UInt32,
        "start_date": pl.Date,
        "end_date": pl.Date,
        "synopsis": pl.String,
        "country_of_origin": pl.String,  # to enum
        "is_licensed": pl.Boolean,
        "hashtag": pl.String,
        "main_staff": pl.String,
        "main_characters": pl.String,
    },
    columns=[
        "anime_id",
        "mal_id",
        "title",
        "type",
        "episodes",
        "duration",
        "status",
        "source",
        "season",  # WINTER 2025
        "season_year",
        "studios",  # Aniplex;A-1 Pictures;Netmarble;D&C MEDIA;Kakao piccoma;Crunchyroll
        "main_studios",
        "genres",  # Action;Adventure;Fantasy
        "tags",  # Urban Fantasy;Dungeon;Male Protagonist;Necromancy;Magic;Super Power;Cultivation;Creature Taming;Swordplay;Gore
        "rating",  # Empty
        "score",
        "mean_score",
        "rank",
        "popularity",
        "popularity_rank",
        "members",
        "favorites",
        "watching",
        "completed",
        "on_hold",
        "dropped",
        "plan_to_watch",
        "start_date",
        "end_date",
        "synopsis",
        "country_of_origin",
        "is_licensed",
        "hashtag",
        "main_staff",
        "main_characters",
    ],
    infer_schema_length=10000,
)  # .lazy()


df_anime_data = df_anime_data.with_columns(
    (
        pl.col("anime_id").cast(pl.UInt32),
        pl.col("mal_id").cast(pl.UInt32),
        pl.col("duration").cast(pl.UInt32),
        pl.col("popularity_rank").cast(pl.UInt32),
        pl.col("score").cast(pl.UInt32),
        pl.col("mean_score").cast(pl.UInt32),
        pl.col("rank").cast(pl.UInt32),
        pl.col("status").cast(pl.Categorical),
        pl.col("country_of_origin").cast(pl.Categorical),
        pl.col("source").cast(pl.Categorical),
        pl.col("type").cast(pl.Categorical),
        pl.col("studios").str.split(";"),
        pl.col("genres").str.split(";"),
        pl.col("tags").str.split(";"),
        pl.col("main_staff").str.split(";"),
        pl.col("main_characters").str.split(";"),
        pl.col("season")
        .str.split(" ")
        .list.first()
        .cast(pl.Categorical)
        .alias("season_epoch"),
        pl.col("episodes").fill_null(1).fill_nan(1).cast(pl.UInt32),
        (pl.col("duration") * pl.col("episodes"))
        .alias("total_duration")
        .cast(pl.UInt32),
    ),
)

df_anime_data = df_anime_data.with_row_index(name="id")

df_features = df_anime_data.select(
    [
        "anime_id",
        "title",
        "score",
        "popularity",
        pl.concat_str(
            [
                pl.col("title"),
                pl.lit(". Type: "),
                pl.col("type").cast(pl.String).fill_null(""),
                pl.lit(". Source: "),
                pl.col("source").cast(pl.String).fill_null(""),
                pl.lit(". Genres: "),
                pl.col("genres").list.join(", ").fill_null(""),
                pl.lit(". Tags: "),
                pl.col("tags").list.join(", ").fill_null(""),
                pl.lit(". Synopsis: "),
                pl.col("synopsis").fill_null(""),
            ]
        ).alias("dense_text"),
    ]
)

print(df_anime_data.head)
