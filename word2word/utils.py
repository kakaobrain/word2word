# -*- coding: utf-8 -*-
import platform
import wget
import requests
import os
import pickle
from zipfile import ZipFile
from os.path import expanduser


def get_savedir(savedir=None):
    if savedir:
        os.makedirs(savedir, exist_ok=True)
        return savedir

    pf = platform.system()
    if pf == "Windows":
        savedir = "C:\word2word"
    else:
        homedir = expanduser("~")
        savedir = os.path.join(homedir, ".word2word")

    if not os.path.exists(savedir):
        os.makedirs(savedir, exist_ok=True)
    return savedir


def exists(path):
    r = requests.head(path)
    return r.status_code == requests.codes.ok


def get_download_url(lang1, lang2):
    filepath = os.path.dirname(os.path.abspath(__file__)) + '/supporting_languages.txt'
    for line in open(filepath, 'r'):
        l1, l2 = line.strip().split("-")
        if lang1 == l1 and lang2 == l2:
            return f"https://mk.kakaocdn.net/dn/kakaobrain/word2word/{lang1}-{lang2}.pkl"
    raise Exception(f"Language pair {lang1}-{lang2} is not supported.")


def download_or_load(lang1, lang2, custom_savedir):
    savedir = get_savedir(savedir=custom_savedir)
    fpath = os.path.join(savedir, f"{lang1}-{lang2}.pkl")
    if not os.path.exists(fpath):
        # download from cloud
        url = get_download_url(lang1, lang2)
        if url is None:
            raise ValueError(f"Dataset not found for {lang1}-{lang2}.")

        if not exists(url):
            raise ValueError("Sorry. There seems to be a problem with cloud access.")

        print("Downloading data ...")
        wget.download(url, fpath)
    word2x, y2word, x2ys = pickle.load(open(fpath, 'rb'))
    return word2x, y2word, x2ys


def download_os2018(lang1, lang2):
    """Download corpora from OpenSubtitles2018.

    :return (lang1_file, lang2_file)
    """
    datadir = "data"
    filepref = f"OpenSubtitles.{lang1}-{lang2}"
    if all(os.path.exists(os.path.join(datadir, f"{filepref}.{lang}"))
           for lang in [lang1, lang2]):
        print(f"Found existing {filepref} files. loading...")
    else:
        # Download and unzip parallel corpus
        url = f"http://opus.nlpl.eu/download.php?f=OpenSubtitles/v2018/moses/{lang1}-{lang2}.txt.zip"
        zipname = os.path.join(datadir, f"{lang1}-{lang2}.txt.zip")
        print(f"Downloading {filepref}...")
        wget.download(url, zipname)
        with ZipFile(zipname) as zf:
            for fname in zf.namelist():
                if fname.startswith(filepref):
                    zf.extract(fname, datadir)
        os.remove(zipname)
    lang1_file, lang2_file = [
        os.path.abspath(os.path.join(datadir, f"{filepref}.{lang}"))
        for lang in [lang1, lang2]
    ]
    return lang1_file, lang2_file
