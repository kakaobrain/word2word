'''
$ wget https://dl.fbaipublicfiles.com/arrival/dictionaries.tar.gz
ord$ tar -xzvf *.tar.gz
https://github.com/facebookresearch/MUSE/issues/34

'''
from urllib.request import urlopen
import pickle

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


def load_data(lang1, lang2, co=False):
    if co:
        fp = f"results/{lang1}-{lang2}_co.pkl"
    else:
        fp = f"results/{lang1}-{lang2}.pkl"
    word2x, y2word, x2ys = pickle.load(open(fp, 'rb'))
    return word2x, y2word, x2ys


def word2word(query, word2x, y2word, x2ys, n_best=1):
    if query in word2x and word2x[query] in x2ys:
        x = word2x[query]
        ys = x2ys[x]
        return [y2word[y] for y in ys][:n_best]
    else:
        return [query]

    # if query in word2x:
    #     x = word2x[query]
    #     if x in x2ys:
    #         ys = x2ys[x]
    #         return [y2word[y].lower() for y in ys][:n_best]
    #     else:
    #         return [query]
    # else:
    #     q_uppered = query[0].upper() + query[1:]
    #     if q_uppered in word2x:
    #         x = word2x[q_uppered]
    #         if x in x2ys:
    #             ys = x2ys[x]
    #             return [y2word[y].lower() for y in ys][:n_best]
    #         else:
    #             return [query]
    #     else:
    #         return [query]

def eval(query2target, word2x, y2word, x2ys, n_best=1):
    # not_in_word2x = []
    n_correct, n_wrong = 0, 0
    for query, target in query2target.items():
        translations = word2word(query, word2x, y2word, x2ys, n_best)

        if len(set(translations).intersection(set(target))) > 0:
            n_correct += 1
        else:
            # print(query)
            # print(target)
            # print(translations)
            # print()
            # input()
            n_wrong += 1

    return n_correct, n_wrong

if __name__ == "__main__":
    for langA, langB in (["en", "es"],
                         ["en", "fr"],
                         ["en", 'de'],
                         ['en', 'ru'],
                         ['en', 'zh_tw'],
                         # ['en', 'eo'],
                         ['en', 'it']):
        for lang1, lang2 in ([langA, langB], [langB, langA]):
            for co in (True, False):
                query2target = get_muse(lang1, lang2)
                word2x, y2word, x2ys = load_data(lang1, lang2, co)
                for n_best in (1, 5):
                    n_correct, n_wrong = eval(query2target, word2x, y2word, x2ys, n_best)
                    assert n_correct + n_wrong == 1500

                    precision = round(100*n_correct / 1500, 1)
                    if co:
                        print(f"{lang1}-{lang2}-co-P@{n_best}: {n_correct}:{precision}")
                    else:
                        print(f"{lang1}-{lang2}-word2word-P@{n_best}: {n_correct}:{precision}")

    # for langA, langB in (['en', 'th'],):
    #     for lang1, lang2 in ([langA, langB], [langB, langA]):
    #         # if lang1=="en": continue
    #         print(lang1, lang2)
    #         query2target = get_muse(lang1, lang2)
    #         # print(len(query2target), query2target)
    #         word2x, y2word, x2ys = load_data(lang1, lang2)
    #         print(2)
    #         for n_best in (1, 5):
    #             n_correct, n_wrong = eval(query2target, word2x, y2word, x2ys, n_best)
    #             # assert n_correct + n_wrong == 1500, n_correct + n_wrong
    #
    #             precision = n_correct / 1500
    #             print(f"{lang1}-{lang2}-P@{n_best}: {n_correct}:{precision}")