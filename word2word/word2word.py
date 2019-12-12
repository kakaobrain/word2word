# -*- coding: utf-8 -*-

import os
import pickle
from time import time

from word2word.utils import (
    download_or_load, download_os2018, get_savedir
)
from word2word.tokenization import (
    load_tokenizer, get_sents, get_vocab, update_dicts
)
from word2word.methods import (
    rerank, rerank_mp, get_trans_co, get_trans_pmi
)


class Word2word:
    """The word2word class.

    Usage:
        from word2word import Word2word

        # Download and load a pre-computed bilingual lexicon
        en2fr = Word2word("en", "fr")
        print(en2fr("apple"))
        # out: ['pomme', 'pommes', 'pommier', 'tartes', 'fleurs']

        # Build a custom bilingual lexicon
        # (requires two aligned files, e.g., my_corpus.en, my_corpus.fr)
        my_en2fr = Word2word.make("en", "fr", "my_corpus")
    """

    def __init__(self, lang1, lang2,
                 word2x=None, y2word=None, x2ys=None, custom_savedir=None):
        self.lang1 = lang1
        self.lang2 = lang2

        if all(d is not None for d in [word2x, y2word, x2ys]):
            # load a custom-built word2word bilingual lexicon
            self.word2x, self.y2word, self.x2ys = word2x, y2word, x2ys
        elif any(d is not None for d in [word2x, y2word, x2ys]):
            raise ValueError(
                f"custom bilingual lexicon is only partially provided. "
                f"use Word2word.make() or Word2word.load() to "
                f"properly build or load custom lexicons.")
        else:
            # default: download/load the word2word dataset
            self.word2x, self.y2word, self.x2ys = download_or_load(
                lang1, lang2, custom_savedir
            )

        # lazily keep summary statistics of the learned bilingual lexicon
        self.summary = {}

    def __call__(self, query, n_best=5):
        """Retrieve top-k word translations for the query word."""
        try:
            x = self.word2x[query]
            ys = self.x2ys[x]
            words = [self.y2word[y] for y in ys]
        except KeyError:
            raise KeyError(
                f"query word {query} not found in the bilingual lexicon."
            )
        return words[:n_best]

    def __len__(self):
        """Return the number of source words for which translation exists."""
        return len(self.x2ys)

    def compute_summary(self):
        """Compute basic summaries for the bilingual lexicon."""
        n_unique_ys = len(set([y for ys in self.x2ys.values() for y in ys]))
        n_ys = [len(ys) for ys in self.x2ys.values()]
        self.summary = {
            "n_valid_words": len(self),
            "n_valid_targets": n_unique_ys,
            "n_total_words": len(self.word2x),
            "n_total_targets": len(self.y2word),
            "n_translations_per_word": sum(n_ys) / len(n_ys),
            "n_sentences": None,  # original file required
        }
        return self.summary

    @classmethod
    def make(
            cls,
            lang1: str,
            lang2: str,
            datapref: str = None,
            n_lines: int = 100000000,
            cutoff: int = 5000,
            rerank_width: int = 100,
            rerank_impl: str = "multiprocessing",
            cased: bool = True,
            n_translations: int = 10,
            save_cooccurrence: bool = False,
            save_pmi: bool = False,
            savedir: str = None,
            num_workers: int = 16,
    ):
        """Build a bilingual lexicon using a parallel corpus."""

        print("Step 0. Check files")
        lang1, lang2 = sorted([lang1, lang2])
        if datapref:
            lang1_file, lang2_file = [
                f"{datapref}.{lang}" for lang in [lang1, lang2]
            ]
            assert os.path.exists(lang1_file), \
                f"custom parallel corpus file missing at {datapref}.{lang1}"
            assert os.path.exists(lang2_file), \
                f"custom parallel corpus file missing at {datapref}.{lang2}"
        else:
            lang1_file, lang2_file = download_os2018(lang1, lang2)

        print("Step 1. Load tokenizer")
        tokenizer1 = load_tokenizer(lang1)
        tokenizer2 = load_tokenizer(lang2)

        t0 = time()
        print("Step 2. Constructing sentences")
        sents1 = get_sents(
            lang1_file, lang1, tokenizer1, cased, n_lines, num_workers
        )
        sents2 = get_sents(
            lang2_file, lang2, tokenizer2, cased, n_lines, num_workers
        )
        print(f"Time taken for step 2: {time() - t0:.2f}s")

        assert len(sents1) == len(sents2), (
            f"{lang1} and {lang2} files must have the same number of lines.\n"
            f"({lang1}: {len(sents1)} lines, {lang2}: {len(sents2)} lines)"
        )

        # input savedir if provided, else datapref (custom data location);
        # system default otherwise
        savedir = get_savedir(savedir if savedir else datapref)

        print("Step 3. Compute vocabularies")
        # word <-> index
        word2x, x2word, x2cnt = get_vocab(sents1)
        word2y, y2word, y2cnt = get_vocab(sents2)

        print("Step 4. Update count dictionaries")
        # monolingual and cross-lingual dictionaries
        x2xs, y2ys, x2ys, y2xs = update_dicts(
            sents1, sents2, word2x, word2y, cutoff
        )

        t0 = time()
        print("Step 5. Translation using CPE scores")
        if rerank_impl == "simple":
            x2ys_cpe = rerank(x2ys, x2cnt, x2xs, rerank_width, n_translations)
            y2xs_cpe = rerank(y2xs, y2cnt, y2ys, rerank_width, n_translations)
        elif rerank_impl == "multiprocessing":
            x2ys_cpe = rerank_mp(
                x2ys, x2cnt, x2xs, rerank_width, n_translations, num_workers
            )
            y2xs_cpe = rerank_mp(
                y2xs, y2cnt, y2ys, rerank_width, n_translations, num_workers
            )
        else:
            raise ValueError("unrecognized --rerank_impl argument. "
                             "Options: simple, multiprocessing")
        print(f"Time taken for step 5: {time() - t0:.2f}s")

        print("Saving...")
        Word2word.save(lang1, lang2, savedir, word2x, word2y, x2word,
                       x2ys_cpe, y2word, y2xs_cpe)

        if save_cooccurrence:
            print("Step 5-1. Translation using co-occurrence counts")
            subdir = os.path.join(savedir, "co")
            os.makedirs(subdir, exist_ok=True)

            x2ys_co = get_trans_co(x2ys, n_translations)
            y2xs_co = get_trans_co(y2xs, n_translations)
            Word2word.save(lang1, lang2, subdir, word2x, word2y, x2word,
                           x2ys_co, y2word, y2xs_co)

        if save_pmi:
            print("Step 5-2. Translation using PMI scores")
            subdir = os.path.join(savedir, "pmi")
            os.makedirs(subdir, exist_ok=True)

            seqlens1 = [len(sent) for sent in sents1]
            seqlens2 = [len(sent) for sent in sents2]
            Nx = sum(seqlens1)
            Ny = sum(seqlens2)
            Nxy = sum([seqlen_x * seqlen_y
                       for seqlen_x, seqlen_y in zip(seqlens1, seqlens2)])

            x2ys_pmi = get_trans_pmi(x2ys, x2cnt, y2cnt, Nxy, Nx, Ny,
                                     rerank_width, n_translations)
            y2xs_pmi = get_trans_pmi(y2xs, y2cnt, x2cnt, Nxy, Ny, Nx,
                                     rerank_width, n_translations)

            Word2word.save(lang1, lang2, subdir, word2x, word2y, x2word,
                           x2ys_pmi, y2word, y2xs_pmi)

        print("Done!")
        return cls(lang1, lang2, word2x, y2word, x2ys_cpe)

    @staticmethod
    def save(lang1, lang2, savedir, word2x, word2y, x2word, x2ys, y2word, y2xs):
        with open(os.path.join(savedir, f"{lang1}-{lang2}.pkl"), "wb") as f:
            pickle.dump((word2x, y2word, x2ys), f)
        with open(os.path.join(savedir, f"{lang2}-{lang1}.pkl"), "wb") as f:
            pickle.dump((word2y, x2word, y2xs), f)

    @classmethod
    def load(cls, lang1, lang2, savedir):
        """Loads this object with a custom-built bilingual lexicon.

        savedir is the directory containing {lang1}-{lang2}.pkl files
        built from the make function.
        """
        path = os.path.join(savedir, f"{lang1}-{lang2}.pkl")
        assert os.path.exists(path), \
            f"processed lexicon file not found at {path}"
        with open(path, "rb") as f:
            word2x, y2word, x2ys = pickle.load(f)
        print(f"Loaded word2word custom bilingual lexicon from {path}")
        return cls(lang1, lang2, word2x, y2word, x2ys)
