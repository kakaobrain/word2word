import json
import argparse
from glob import glob
from itertools import chain
from collections import defaultdict

import numpy as np


def get_survey_summary_reference(survey_reference_base, l1, l2):
    # word, base, cpe, pmi
    basefile = survey_reference_base.format(l1, l2)
    rr = []
    with open(glob(basefile)[-1], "r") as f:
        for line in f:
            item = line.strip()
            trans = {'baseline': f.readline().strip().split("\t"),
                     'cpe': f.readline().strip().split("\t"),
                     'pmi': f.readline().strip().split("\t"),
                     }
            rr.append((item, trans))

    return rr


def convert_google_translate(item, level=2):
    ratings = ["Common translation", "Uncommon translation", "Rare translation"][:level]
    # Rare translation
    return [e[1].lower() for e in item['trans'] if e[0] in ratings]


def get_google_translate(gt, l1, l2, level=2):
    basefile = gt.format(l1, l2)
    rr = []
    with open(glob(basefile)[-1], "r") as f:
        for line in f:
            item = line.strip().split("\t")
            if len(item[0]) == 0:
                continue
            word = item[0]
            trans = json.loads(item[1])

            main_trans = trans[0]
            sub_trans = list(chain.from_iterable([convert_google_translate(tt, level=level) for tt in trans[1:]
                                                  if len(tt['trans']) > 0]))

            trans_dict = {
                "main": main_trans["trans"].lower(),
                "verified": main_trans["verified"],
                "subs": [word.lower() for word in sub_trans]
            }
            rr.append((word, trans_dict))

    return rr


language_map = {
    "ar": "Arabic",
    "en": "English",
    "es": "Spanish",
    "tr": "Turkish",
    "fr": "French",
    "fi": "Finnish",
    "de": "German",
    "zh-CN": "Chinese (Simplified)",
    "zh": "Chinese (Simplified)",
    "no": "Norwegian",
    "vi": "Vietnamese",
    "ms": "Malay",
    "ko": "Korean",
    "ja": "Japanese",
    "th": "Thai"}

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--l1', default='en',
                        help="""ISO 639-1 code of target language. \n
                        'See `http://opus.lingfil.uu.se/OpenSubtitles2016.php`""")
    parser.add_argument('--l2', default='es',
                        help="""ISO 639-1 code of target language. \n
                        'See `http://opus.lingfil.uu.se/OpenSubtitles2016.php`""")
    parser.add_argument('--wordfile', default='./word_list',
                        help="""list of words language l1""")
    parser.add_argument('--out', default='./google_translate.out',
                        help="""output text file""")
    parser.add_argument('--headless', default=False,
                        action="store_true")
    parser.add_argument('--survey', default="./csvs/survey_table_reference_{}_{}_*",
                        help="""survey reference file base""")
    parser.add_argument('--google', default="./google_translate_dump/google_translate.{}.{}.out",
                        help="""google translate file base""")

    args = parser.parse_args()
    l1, l2 = args.l1, args.l2

    survey_summary = get_survey_summary_reference(args.survey, l1, l2)

    google_translate = get_google_translate(args.google, l1, l2)

    precision_at1 = defaultdict(int)
    precision_at5 = defaultdict(int)
    total = 0

    # check same thing
    for (word, three_trans), (gword, g_trans) in zip(survey_summary, google_translate):
        try:
            assert word == gword
        except AssertionError as e:
            print(word, gword)
            raise e

        g_main = g_trans['main']
        verified = g_trans['verified']
        sub_trans = g_trans['subs']
        translate_words = [g_main] + sub_trans

        # print(word, g_main, verified)
        flags = [0, 0, 0]
        idx = 0
        for method in three_trans:
            # print("\t", key)
            assert translate_words[0] is not None
            assert len(translate_words) > 0

            trans = three_trans[method]
            precision_at1[method] += len(set(translate_words) & set(trans[:1])) > 0
            precision_at5[method] += len(set(translate_words) & set(trans[:5])) > 0

            idx += 1
        total += 1
        if flags[1] == 0 and flags[0] > 0 and flags[2] > 0:
            # print(word, three_trans)
            pass

    methods = ['baseline', 'cpe', 'pmi']
    for method in methods:
        precision_at1[method] /= total
        precision_at5[method] /= total
        precision_at1[method + '_se'] = \
            np.sqrt(precision_at1[method] * (1.0 - precision_at1[method]) / total)
        precision_at5[method + '_se'] = \
            np.sqrt(precision_at1[method] * (1.0 - precision_at5[method]) / total)

    print(total)
    top1 = precision_at1
    top5 = precision_at5
    print("[top1]")
    for method in methods:
        print(method, round(top1[method], 3), "+/-", round(top1[method + '_se'], 3))
    print("[top5]")
    for method in methods:
        print(method, round(top5[method], 3), "+/-", round(top5[method + '_se'], 3))

    # not a word
    # proper noun
    # suggestion - 정답적기

# partial
