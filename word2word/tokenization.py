# -*- coding: utf-8 -*-

from collections import Counter, defaultdict
from itertools import chain, islice, product, repeat
from multiprocessing import Pool
import operator
import re
from tqdm import tqdm


def load_tokenizer(lang):
    if lang == "ko":
        from konlpy.tag import Mecab
        tokenizer = Mecab()
    elif lang == "ja":
        import Mykytea
        opt = "-model jp-0.4.7-1.mod"
        tokenizer = Mykytea.Mykytea(opt)
    elif lang == "zh_cn":
        import Mykytea
        opt = "-model ctb-0.4.0-1.mod"
        tokenizer = Mykytea.Mykytea(opt)
    elif lang == "zh_tw":
        import jieba
        tokenizer = jieba
    elif lang == "vi":
        from pyvi import ViTokenizer
        tokenizer = ViTokenizer
    elif lang == "th":
        from pythainlp.tokenize import word_tokenize
        tokenizer = word_tokenize
    elif lang == "ar":
        import pyarabic.araby as araby
        tokenizer = araby
    # elif lang=="en":
    #     from nltk import word_tokenize
    #     tokenizer = word_tokenize
    else:
        from nltk.tokenize import ToktokTokenizer
        tokenizer = ToktokTokenizer()

    return tokenizer


def word_segment(sent, lang, tokenizer):
    if lang == 'ko':
        words = [word for word, _ in tokenizer.pos(sent)]
    elif lang == 'ja':
        words = [elem for elem in tokenizer.getWS(sent)]
    elif lang == 'th':
        words = tokenizer(sent, engine='mm')
    elif lang == 'vi':
        words = tokenizer.tokenize(sent).split()
    elif lang == 'zh_cn':
        words = [elem for elem in tokenizer.getWS(sent)]
    elif lang == "zh_tw":
        words = list(tokenizer.cut(sent, cut_all=False))
    elif lang == "ar":
        words = tokenizer.tokenize(sent)
    # elif lang=="en":
    #     words = tokenizer(sent)
    else:  # Most european languages
        sent = re.sub("([A-Za-z])(\.[ .])", r"\1 \2", sent)
        words = tokenizer.tokenize(sent)

    return words


def process_line(line, lang, tokenizer, cased):
    """Strip, uncase (optionally), and tokenize line.

    multiprocessing helper for get_sents()."""
    line = line.strip() if cased else line.strip().lower()
    return word_segment(line, lang, tokenizer)


def get_sents(fin, lang, tokenizer, cased, n_lines, num_workers=8):
    """Load parallel corpus and segment words using multiprocessing."""

    with open(fin, encoding='utf-8') as f:
        lines = islice(f, n_lines)
        if num_workers <= 1:
            return [process_line(line, lang, tokenizer, cased)
                    for line in lines]
        else:
            print(f"Entering multiprocessing with {num_workers} workers...")
            with Pool(num_workers) as p:
                return p.starmap(
                    process_line,
                    zip(lines, repeat(lang), repeat(tokenizer), repeat(cased))
                )


def get_vocab(sents):
    word2idx, idx2word, idx2cnt = dict(), dict(), dict()

    word2cnt = Counter(tqdm(list(chain.from_iterable(sents)))).most_common()
    word2cnt.sort(key=operator.itemgetter(1, 0), reverse=True)
    for idx, (word, cnt) in enumerate(tqdm(word2cnt)):
        word2idx[word] = idx
        idx2word[idx] = word
        idx2cnt[idx] = cnt

    return word2idx, idx2word, idx2cnt


def update_dicts(sents1, sents2, vocab1, vocab2, cutoff):
    """Get monolingual and cross-lingual count dictionaries.

    'cutoff' determines how many collocates are considered in each language.
    """

    def u2_iter(t1, t2, same_ignore=False, cut_t2=None):
        for _ in product(t1, t2):
            if (not same_ignore or _[0] != _[1]) and (not cut_t2 or _[1] < cut_t2):
                yield _

    def build_ddi():
        return defaultdict(lambda: defaultdict(int))

    x_x_dict = build_ddi()
    y_y_dict = build_ddi()
    x_y_dict = build_ddi()
    y_x_dict = build_ddi()

    for sent1, sent2 in tqdm(zip(sents1, sents2), total=len(sents1)):
        xs = [vocab1[wx] for wx in sent1 if wx in vocab1]
        ys = [vocab2[wy] for wy in sent2 if wy in vocab2]

        for xx1, xx2 in u2_iter(xs, xs, same_ignore=True, cut_t2=cutoff):
            x_x_dict[xx1][xx2] += 1
        for yy1, yy2 in u2_iter(ys, ys, same_ignore=True, cut_t2=cutoff):
            y_y_dict[yy1][yy2] += 1
        for xx, yy in u2_iter(xs, ys, same_ignore=False):
            x_y_dict[xx][yy] += 1
            y_x_dict[yy][xx] = x_y_dict[xx][yy]

    # convert to ordinary dicts for pickling
    def ddi2dict(ddi):
        return {k: dict(v) for k, v in ddi.items()}

    return tuple(ddi2dict(ddi)
                 for ddi in [x_x_dict, y_y_dict, x_y_dict, y_x_dict])
