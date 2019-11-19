#-*- coding: utf-8 -*-

import codecs
from collections import Counter
from itertools import chain
import re
from tqdm import tqdm


def load_tokenizer(lang):
    if lang=="ko":
        from konlpy.tag import Mecab
        tokenizer = Mecab()
    elif lang=="ja":
        import Mykytea
        opt="-model jp-0.4.7-1.mod"
        tokenizer = Mykytea.Mykytea(opt)
    elif lang=="zh_cn":
        import Mykytea
        opt = "-model ctb-0.4.0-1.mod"
        tokenizer = Mykytea.Mykytea(opt)
    elif lang=="zh_tw":
        import jieba
        tokenizer = jieba
    elif lang=="vi":
        from pyvi import ViTokenizer
        tokenizer = ViTokenizer
    elif lang=="th":
        from pythainlp.tokenize import word_tokenize
        tokenizer = word_tokenize
    elif lang=="ar":
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
    elif lang=='ja':
        words = [elem for elem in tokenizer.getWS(sent)]
    elif lang=='th':
        words = tokenizer(sent, engine='mm')
    elif lang=='vi':
        words = tokenizer.tokenize(sent).split()
    elif lang=='zh_cn':
        words = [elem for elem in tokenizer.getWS(sent)]
    elif lang=="zh_tw":
        words = list(tokenizer.cut(sent, cut_all=False))
    elif lang=="ar":
        words = tokenizer.tokenize(sent)
    # elif lang=="en":
    #     words = tokenizer(sent)
    else:  # Most european languages
        sent = re.sub("([A-Za-z])(\.[ .])", r"\1 \2", sent)
        words = tokenizer.tokenize(sent)

    return words


def get_sents(fin, lang, tokenizer, cased):
    sents = []  # list of lists

    text = codecs.open(fin, 'r', 'utf-8').read()
    lines = text.replace("\u0085", "").splitlines() # \u0085: erroneous control char.

    for line in tqdm(lines):
        if not cased:
            line = line.lower()
        words = word_segment(line.strip(), lang, tokenizer)
        sents.append(words)
    return sents


def get_vocab(sents):
    word2idx, idx2word, idx2cnt = dict(), dict(), dict()

    word2cnt = Counter(tqdm(list(chain.from_iterable(sents))))
    for idx, (word, cnt) in enumerate(word2cnt.most_common(len(word2cnt))):
        word2idx[word] = idx
        idx2word[idx] = word
        idx2cnt[idx] = cnt

    return word2idx, idx2word, idx2cnt


def update_monolingual_dict(xs, x2xs, cutoff):
    # x2cnt = Counter(xs)

    for x in set(xs):
        for col in set(xs):  # col: collocate
            if x == col: continue
            if col > cutoff: continue  # Cut off infrequent words to save memory
            if x not in x2xs: x2xs[x] = dict()
            if col not in x2xs[x]: x2xs[x][col] = 0
            # cnt = x2cnt[col]
            # x2xs[x][col] += cnt
            x2xs[x][col] += 1
    return x2xs

