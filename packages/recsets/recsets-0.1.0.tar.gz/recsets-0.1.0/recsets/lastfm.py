import pandas as pd
from .utils import SameLinePrinter, DataEncoder, download
from pathlib import Path

LastFM1K = "http://mtg.upf.edu/static/datasets/last.fm/lastfm-dataset-1K.tar.gz"


def download_lastfm1k(directory):
    return download(url=LastFM1K, target_dir=directory)


def load_lastfm1k(
    directory, cols_keep=None, cols_encode=None, cols_dropna=None
) -> pd.DataFrame:
    echo = SameLinePrinter().__enter__()  # pylint: disable=no-member
    cols_keep = cols_keep or [
        "user_id",
        "gender",
        "age",
        "country",
        "artist_id",
        "track_id",
    ]
    cols_encode = cols_keep or ["user_id", "gender", "country", "artist_id", "track_id"]
    cols_dropna = cols_keep or ["user_id", "artist_id", "track_id", "country"]

    directory = directory if isinstance(directory, Path) else Path(directory)

    echo("Reading user profiles ...")
    profiles_df = pd.read_csv(
        directory.joinpath("userid-profile.tsv"), sep="\t"
    ).rename(columns={"#id": "user_id"})

    echo("Reading user interactions ...")
    interactions_df = pd.read_csv(
        directory.joinpath("userid-timestamp-artid-artname-traid-traname.tsv"),
        sep="\t",
        names=[
            "user_id",
            "timestamp",
            "artist_id",
            "artist_name",
            "track_id",
            "track_name",
        ],
    )

    echo("Merging user profiles and interactions ...")
    interactions_df = pd.merge(
        left=interactions_df, right=profiles_df, on="user_id", how="left"
    )

    echo("Droping duplicates and filtering columns ...")
    interactions_df = interactions_df[cols_keep].dropna(subset=cols_dropna)

    echo("Filling missing genders ...")
    if "gender" in interactions_df.columns:
        interactions_df["gender"] = interactions_df["gender"].fillna("u")

    echo("Filling missing ages ...")
    if "age" in interactions_df.columns:
        median_age = interactions_df["age"].median()
        interactions_df["age"] = interactions_df["age"].fillna(median_age).astype(int)

    echo("Label encoding columns  ...")
    encoder = DataEncoder()
    interactions_df = encoder.encode_df(interactions_df, columns=cols_encode)

    echo("Loaded LastFM 1K dataset")
    return interactions_df
