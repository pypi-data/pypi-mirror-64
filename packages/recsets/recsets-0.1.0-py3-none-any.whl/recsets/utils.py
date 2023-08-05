from contextlib import contextmanager
from tqdm import tqdm
from urllib.request import urlretrieve
from pathlib import Path
from sklearn.preprocessing import LabelEncoder
import os
import tarfile
import zipfile
import logging
import shutil
import numpy as np
import pandas as pd

LOG = logging.getLogger()


class TqdmUpTo(tqdm):
    """Provides `update_to(n)` which uses `tqdm.update(delta_n)`."""

    def update_to(self, b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)  # will also set self.n = b * bsize


@contextmanager
def SameLinePrinter():
    class Printer:
        def __init__(self):
            self.first: bool = True
            self.prev_len = 1

        def __call__(self, value, **kwargs):
            self.print(value=value, **kwargs)

        def print(self, value, **kwargs):
            kwargs.update({"end": ""})

            if self.first:
                self.first = False
            else:
                value = "\r" + value
            print(" " * self.prev_len, **kwargs)
            print(value, **kwargs)
            self.prev_len = len(value)

    try:
        printer = Printer()
        yield printer
    finally:
        del printer


def download(
    url: str,
    target_dir: str = os.devnull,
    extract: bool = True,
    overwrite: bool = False,
) -> str:
    """Download a file"""
    filename = url.split("/")[-1]
    tqdm_kwds = dict(unit="B", unit_scale=True, miniters=1, desc=filename)

    if target_dir is None:
        destination_file = os.devnull
    else:
        assert os.path.isdir(target_dir), "Invalid target directory"
        destination_file = os.path.join(target_dir, filename)

    if not os.path.exists(destination_file):
        with TqdmUpTo(**tqdm_kwds) as t:
            urlretrieve(
                url, filename=destination_file, reporthook=t.update_to, data=None
            )
    else:
        LOG.info("File %s already downloaded." % filename)

    if extract:
        destination_dir = os.path.splitext(destination_file)[0]
        unzip = False
        if os.path.exists(destination_dir) and os.path.isdir(destination_dir):
            if overwrite:
                LOG.info("Overwriting files in %s." % destination_dir)
                shutil.rmtree(destination_dir)
                unzip = True
            else:
                LOG.info(
                    "File %s already extracted to %s." % (filename, destination_dir)
                )
        else:
            unzip = True
        if unzip:
            with SameLinePrinter() as echo:
                echo("Extracting files ...")
                if zipfile.is_zipfile(destination_file):
                    with zipfile.ZipFile(destination_file) as zipd:
                        zipd.extractall(target_dir)
                elif tarfile.is_tarfile(destination_file):
                    with tarfile.open(destination_file) as tard:
                        tard.extractall(target_dir)
                else:
                    raise Exception("Unknown file type")
                echo("Extracting files ... done")

        return destination_dir
    else:
        return destination_file


class DataEncoder:
    def __init__(self):
        self.encoders = {}

    def encode(self, key, values, encoder=None):
        should_fit = key not in self.encoders
        encoder = self.encoders.get(key, encoder or LabelEncoder())
        shapes = {
            LabelEncoder.__name__: (-1,),
        }
        enc_input_shape = shapes[encoder.__class__.__name__]
        values_all = values.values if isinstance(values, pd.Series) else values
        values_unique = (
            values.unique() if isinstance(values, pd.Series) else np.unique(values)
        )

        if isinstance(encoder, (LabelEncoder,)):
            values_all = values_all.reshape(enc_input_shape)
            values_unique = values_unique.reshape(enc_input_shape)

        if should_fit:
            encoder = encoder.fit(values_unique.reshape(enc_input_shape))
            self.encoders[key] = encoder

        encoded = encoder.transform(values_all)
        return encoded

    def decode(self, key, values):
        enc = self.encoders.get(key, None)
        if enc is None:
            raise ValueError("No encoder for %s" % key)
        else:
            return enc.inverse_transform(values)

    def encode_df(self, df, columns, inplace=False):
        df_copy = df if inplace else df.copy()

        for col in columns:
            if col not in df.columns:
                raise ValueError("%s is not a column in input DataFrame" % col)
            try:
                df_copy[col] = self.encode(col, df[col])
            except ValueError:
                pass
            except TypeError as e:
                message = str(e)
                if message == "argument must be a string or number":
                    raise TypeError(
                        f"{message}: Column {col} contains invalid or NaN values."
                    )

        return df_copy

    def decode_df(self, df, inplace=False):
        df_copy = df if inplace else df.copy()

        for col in df.columns:
            try:
                df_copy[col] = self.decode(col, df[col])
            except ValueError:
                pass

        return df_copy
