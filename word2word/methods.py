#-*- coding: utf-8 -*-

import numpy as np
import operator
from tqdm import tqdm


def rerank(x2ys, x2cnt, x2xs, width, n_trans):
    """Re-rank word translations by correcting scores using the CPE method.

    See paper for details."""
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
        _ys_ = sorted(y_scores, key=lambda x: x[1], reverse=True)[:n_trans]
        _ys_ = [each[0] for each in _ys_]
        x2ys_cpe[x] = _ys_

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
