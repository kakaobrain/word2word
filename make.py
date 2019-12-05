# -*- coding: utf-8 -*-
r"""
A command line script for building a word2word bilingual lexicon.

By default, builds from a (downloaded) OpenSubtitles2018 dataset;
 also supports building from a custom parallel corpus.

Usage:
    # Build with OpenSubtitles2018
    python make.py --lang1 en --lang2 es
    # Save files to a custom location (also see Word2word.load)
    python make.py --lang1 ko --lang2 en --savedir ko-en.w2w
    # Build with a custom dataset
    python make.py --lang1 en --lang2 fr --datapref data/pubmed.en-fr

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
    parser.add_argument('--n_lines', type=int, default=100000000,
                        help="number of parallel sentences used")
    parser.add_argument('--cutoff', type=int, default=5000,
                        help="number of words that are used in calculating collocates within each language")
    parser.add_argument('--rerank_width', default=100, type=int,
                        help="maximum number of target-side collocates considered for reranking")
    parser.add_argument('--rerank_impl', default="multiprocessing", type=str,
                        help="choice of reranking implementation: simple, multiprocessing (default)")
    parser.add_argument('--cased', dest="cased", action="store_true",
                        help="Keep the case.")
    parser.add_argument('--n_translations', type=int, default=10,
                        help="number of final word2word translations kept")
    parser.add_argument('--save_cooccurrence', dest="save_cooccurrence", action="store_true",
                        help="Save the cooccurrence results")
    parser.add_argument('--save_pmi', dest="save_pmi", action="store_true",
                        help="Save the pmi results")
    parser.add_argument('--savedir', type=str, default=None,
                        help="location to store bilingual lexicons."
                             "make sure to use this input when loading from "
                             "a custom-bulit lexicon.")
    parser.add_argument('--num_workers', default=16, type=int,
                        help="number of workers used for multiprocessing")
    args = parser.parse_args()

    Word2word.make(**vars(args))


if __name__ == "__main__":
    main()
