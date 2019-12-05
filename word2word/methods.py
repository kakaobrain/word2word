# -*- coding: utf-8 -*-

"""
word2word/methods.py: bilingual lexicon extraction methods

Speed comparison using OpenSubtitles.en-eo (64,485 sentences):
    - rerank (single process): 105s
    - rerank_mp (multiprocessing), 8 CPUs: 33s (3.2x faster)
    - rerank_mp (multiprocessing), 16 CPUs: 26s (4.0x faster)
    - rerank_mp (multiprocessing), 32 CPUs: 47s (2.2x faster)

Optimal number of CPUs may differ depending on corpus size.
"""

import itertools as it
import numpy as np
import operator
from tqdm import tqdm


def rerank(x2ys, x2cnt, x2xs, width, n_trans):
    """Re-rank word translations by computing CPE scores.

    See paper for details about the CPE method."""
    x2ys_cpe = dict()
    for x, ys in tqdm(x2ys.items()):
        cntx = x2cnt[x]
        y_scores = []
        for y, cnty in sorted(ys.items(), key=operator.itemgetter(1), reverse=True)[:width]:
            ts = cnty / float(cntx)  # translation score: initial value
            if x in x2xs:
                for x2, cntx2 in x2xs[x].items():  # Collocates
                    p_x_x2 = cntx2 / float(cntx)
                    p_x2_y2 = 0
                    if x2 in x2ys:
                        p_x2_y2 = x2ys[x2].get(y, 0) / float(x2cnt[x2])
                    ts -= (p_x_x2 * p_x2_y2)
            y_scores.append((y, ts))
        _ys_ = sorted(y_scores, key=lambda y_score: y_score[1], reverse=True)[:n_trans]
        _ys_ = [each[0] for each in _ys_]
        x2ys_cpe[x] = _ys_

    return x2ys_cpe


def _rerank_mp(x_and_ys, shared_inputs):
    """Internal multiprocessing function for `rerank_fast()`."""
    x, ys = x_and_ys
    x2ys, x2cnt, x2xs, width, n_trans = shared_inputs

    sorted_ys = sorted(ys.items(),
                       key=operator.itemgetter(1),
                       reverse=True)[:width]
    if x not in x2xs:
        return x, [y for y, score in sorted_ys[:n_trans]]

    def _correction(y):
        return sum(
            cntx2 * x2ys[x2][y] / float(x2cnt[x2])
            for x2, cntx2 in x2xs[x].items() if x2 in x2ys and y in x2ys[x2]
        )

    y_scores = [(y, cnty - _correction(y)) for y, cnty in sorted_ys]
    y_scores = sorted(y_scores, key=operator.itemgetter(1), reverse=True)
    reranked_ys = [y for y, score in y_scores[:n_trans]]
    return x, reranked_ys


def rerank_mp(x2ys, x2cnt, x2xs, width, n_trans, num_workers):
    """Re-rank word translations by computing CPE scores.

    Uses multiprocessing to speed up computation (significantly).
    In Python 3.8+, shared_inputs can be implemented directly as shared_memory.

    See paper for details about the CPE method."""
    from multiprocessing import Pool

    shared_inputs = x2ys, x2cnt, x2xs, width, n_trans
    print(f"Entering multiprocessing with {num_workers} workers..."
          f" (#words={len(x2ys)})")
    with Pool(num_workers) as p:
        x2ys_cpe = dict(p.starmap(
            _rerank_mp,
            zip(x2ys.items(), it.repeat(shared_inputs)),
        ))
    return x2ys_cpe


def get_trans_co(x2ys, n_trans):
    """Use co-occurrences to compute scores."""
    x2ys_co = dict()
    for x, ys in x2ys.items():
        ys = [y for y, cnt in sorted(ys.items(), key=operator.itemgetter(1), reverse=True)[:n_trans]]
        x2ys_co[x] = ys
    return x2ys_co


def get_trans_pmi(x2ys, x2cnt, y2cnt, Nxy, Nx, Ny, width, n_trans):
    """Use pointwise mutual information to compute scores."""
    x2ys_pmi = dict()
    pmi_diff = -np.log2(Nxy) + np.log2(Nx) + np.log2(Ny)
    for x, ys in tqdm(x2ys.items()):
        l_scores = []
        for y, cnt in sorted(ys.items(), key=operator.itemgetter(1),
                             reverse=True)[:width]:
            pmi = np.log2(cnt) - np.log2(x2cnt[x]) - np.log2(y2cnt[y])
            pmi += pmi_diff
            l_scores.append((y, pmi))
        trans = sorted(l_scores, key=operator.itemgetter(1, 0), reverse=True)[:n_trans]
        trans = [each[0] for each in trans]
        x2ys_pmi[x] = trans

    return x2ys_pmi
