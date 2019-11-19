# -*- coding: utf-8 -*-
r"""
A command line script for building a word2word bilingual lexicon.

By default, builds from a (downloaded) OpenSubtitles2018 dataset;
 also supports building from a custom parallel corpus.

Usage:
    # Build with OpenSubtitles2018
    python make.py --lang1 en --lang2 es
    python make.py --lang1 ko --lang2 en
    # Build with a custom dataset
    python make.py --lang1 en --lang2 de --datapref data/europarl-v7.de-en

Authors:
    Kyubyong Park (kbpark.linguist@gmail.com), YJ Choe (yjchoe33@gmail.com), Dongwoo Kim (kimdwkimdw@gmail.com)
"""

import argparse

from word2word import Word2word


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang1', type=str, required=True,
                        help="ISO 639-1 code of language. "
                             "See `http://opus.nlpl.eu/OpenSubtitles2018.php`")
    parser.add_argument('--lang2', type=str, required=True,
                        help="ISO 639-1 code of language. "
                             "See `http://opus.nlpl.eu/OpenSubtitles2018.php`")
    parser.add_argument('--datapref', type=str, default=None,
                        help="data prefix to a custom parallel corpus. "
                             "builds a bilingual lexicon using OpenSubtitles2018 "
                             "unless this option is provided.")
    parser.add_argument('--cutoff', type=int, default=5000,
                        help="number of words that are used in calculating collocation")
    parser.add_argument('--vocab_lines', type=int, default=1000000,
                        help="New words are not added after some point to save memory")
    parser.add_argument('--cased', dest="cased", action="store_true",
                        help="Keep the case.")
    parser.add_argument('--width', default=100, type=int,
                        help="maximum collocates that we consider when reranking them")
    parser.add_argument('--n_translations', type=int, default=10,
                        help="number of final translations")
    parser.add_argument('--save_cooccurrence', dest="save_cooccurrence", action="store_true",
                        help="Save the cooccurrence results")
    parser.add_argument('--save_pmi', dest="save_pmi", action="store_true",
                        help="Save the pmi results")
    args = parser.parse_args()

    Word2word.make(**vars(args))


if __name__ == "__main__":
    main()
