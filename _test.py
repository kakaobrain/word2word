'''
$ wget https://dl.fbaipublicfiles.com/arrival/dictionaries.tar.gz
ord$ tar -xzvf *.tar.gz
https://github.com/facebookresearch/MUSE/issues/34

'''
from urllib.request import urlopen
import pickle
from google_grader import get_google_translate
import regex

def get_muse(lang1, lang2):
    if lang1 == "zh_tw": lang1 = "zh"
    if lang2 == "zh_tw": lang2 = "zh"

    url = f"https://dl.fbaipublicfiles.com/arrival/dictionaries/{lang1}-{lang2}.5000-6500.txt"
    query2target = dict()
    for line in urlopen(url).read().decode('utf8').splitlines():
        query, target = line.strip().split()
        if query in query2target:
            query2target[query].append(target)
        else:
            query2target[query] = [target]

    return query2target


def load_data(lang1, lang2, model):
    fp = f"{model}/{lang1}-{lang2}.pkl"
    # fp = f"etc/w2w/results/{lang1}-{lang2}.pkl"
    # fp = f"w2w/{lang1}-{lang2}.pkl"
    word2x, y2word, x2ys = pickle.load(open(fp, 'rb'))
    return word2x, y2word, x2ys


def get_trans(query, word2x, y2word, x2ys, n_best=1):
    if query in word2x and word2x[query] in x2ys:
        x = word2x[query]
        ys = x2ys[x]
        return [y2word[y].replace("_", " ") for y in ys][:n_best]
    else:
        return [query]


def eval(query2target, word2x, y2word, x2ys, n_best=1):
    # not_in_word2x = []
    n_correct, n_wrong = 0, 0
    for query, target in query2target.items():
        translations = get_trans(query, word2x, y2word, x2ys, n_best)

        if len(set(translations).intersection(set(target))) > 0:
            n_correct += 1
            # print(query, target, translations, "correct")
        else:
            # print(query, target, translations, "wrong")
            # input()
            n_wrong += 1

    return n_correct, n_wrong


def get_google_results(lang1, lang2):
    fp = f"/data/public/rw/w2w/20190719_result/result_{lang1}-{lang2}"
    results = get_google_translate(fp, lang1, lang2, level=2)
    query2target = dict()
    for word, translations in results:
        equivs = translations["subs"]
        equivs.append(translations["main"])
        equivs = [regex.sub("\p{Punctuation}", "", e) for e in equivs]
        query2target[word] = equivs

    return query2target


if __name__ == "__main__":
    # for n_best in (1, 5):
    #     print(f"P@{n_best}")
    #     for model in ("co", "pmi", "w2w", ):
    #         scores = []
    #         for langA, langB in (["en", "es"],
    #                              ["en", "fr"],
    #                              ["en", 'de'],
    #                              ['en', 'ru'],
    #                              ['en', 'zh_tw'],
    #                              ['en', 'it']):
    #             for lang1, lang2 in ([langA, langB], [langB, langA]):
    #                 query2target = get_muse(lang1, lang2)
    #                 word2x, y2word, x2ys = load_data(lang1, lang2, model)
    #                 n_correct, n_wrong = eval(query2target, word2x, y2word, x2ys, n_best)
    #                 assert n_correct + n_wrong == 1500
    #
    #                 precision = round(100*n_correct / 1500, 1)
    #                 scores.append(str(precision))
    #         scores = " & ".join(scores)
    #         print(f"{model} & {scores}")

    for n_best in (1, 5):
        print(f"P@{n_best}")
        for model in ("co", "pmi", "w2w", ):
            scores = []
            for langA, langB in (["en", "zh_cn"],
                                 ["en", "ja"],
                                 ["en", 'ko'],
                                 ['en', 'vi'],
                                 ['en', 'th'],
                                 ['en', 'ar']):
                for lang1, lang2 in ([langA, langB], [langB, langA]):
                    query2target = get_google_results(lang1, lang2)
                    word2x, y2word, x2ys = load_data(lang1, lang2, model)
                    n_correct, n_wrong = eval(query2target, word2x, y2word, x2ys, n_best)
                    # assert n_correct + n_wrong == 1500, (n_correct, n_wrong)

                    precision = round(100*n_correct / 1500, 1)
                    scores.append(str(precision))
            scores = " & ".join(scores)
            print(f"{model} & {scores}")