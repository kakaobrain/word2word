[![image](https://img.shields.io/pypi/v/word2word.svg)](https://pypi.org/project/word2word/)
[![image](https://img.shields.io/pypi/l/word2word.svg)](https://pypi.org/project/word2word/)
[![image](https://img.shields.io/pypi/pyversions/word2word.svg)](https://pypi.org/project/word2word/)
[![image](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/kimdwkimdw)

# word2word

Easy-to-use word-to-word translations for 3,564 language pairs.

## Key Features

* A large collection of freely & publicly available word-to-word translations 
    **for 3,564 language pairs across 62 unique languages.** 
* Easy-to-use Python interface.
* Constructed using an efficient approach that is quantitatively examined by 
    proficient bilingual human labelers.

## Usage

First, install the package using `pip`:
```bash
pip install word2word
```

OR

```
git clone https://github.com/Kyubyong/word2word.git
python setup.py install
```

Then, in Python, download the model and retrieve top-5 word translations 
of any given word to the desired language:
```python
from word2word import Word2word
en2fr = Word2word("en", "fr")
print(en2fr("apple"))
# out: ['pomme', 'pommes', 'pommier', 'tartes', 'fleurs']
```

![gif](./word2word.gif)

## Supported Languages

We provide top-k word-to-word translations across all available pairs 
    from [OpenSubtitles2018](http://opus.nlpl.eu/OpenSubtitles2018.php). 
This amounts to a total of 3,564 language pairs across 62 unique languages. 

The full list is provided [here](word2word/supporting_languages.txt).

## Methodology

Our approach computes the top-k word-to-word translations based on 
the co-occurrence statistics between cross-lingual word pairs in a parallel corpus.
We additionally introduce a correction term that controls for any confounding effect
coming from other source words within the same sentence.
The resulting method is an efficient and scalable approach that allows us to
construct large bilingual dictionaries from any given parallel corpus. 

For more details, see the Methods section of [our paper draft](word2word-draft.pdf).


## Comparisons with Existing Software

A popular publicly available dataset of word-to-word translations is 
[`facebookresearch/MUSE`](https://github.com/facebookresearch/MUSE), which 
includes 110 bilingual dictionaries that are built from Facebook's internal translation tool.
In comparison to MUSE, `word2word` does not rely on a translation software
and contains much larger sets of language pairs (3,564). 
`word2word` also provides the top-k word-to-word translations for up to 100k words 
(compared to 5~10k words in MUSE) and can be applied to any language pairs
for which there is a parallel corpus. 

In terms of quality, while a direct comparison between the two methods is difficult, 
we did notice that MUSE's bilingual dictionaries involving non-European languages may be not as useful. 
For English-Vietnamese, we found that 80% of the 1,500 word pairs in 
the validation set had the same word twice as a pair
(e.g. crimson-crimson, Suzuki-Suzuki, Randall-Randall). 

For more details, see Appendix in [our paper draft](word2word-draft.pdf). 

### added on June, 2019 by kyubyong 
#### key changes
* word2word covers wider langs?
* word2word is case-sensitive.
* evaluation data has some problem as it is pointed out already in our draft.
* esperanto is missing, so it's not possible to compare our results to it.
* I increase the content lines from 1M to 10M.
* I increase the lines for vocab from 100k to 1M.
* If a query in the eval data is not found in our dictionary, we just return the identical result.
* Since we are case-sensitive, we also check a capitalized query if an original one is not found in our dictionary.
* set이 list보다 성능이 낫다. 하지만 갭이 크지 않다. 대신 더 빠르다.
* 많은 데이터를 쓸수록 성능이 낫다
* cutoff는 적어도 상관없다
* rerank width는 클수록 성능이 낫다 100보다 크면 포화
* toktok tokenizer가 훨씬 빠르다.
* lowercase한 것이 대문자한 것보다 성능 비교가 용이하다.
* vocab이 큰 게 낫다.
* vocab line으로 하는 게 빈도순으로 하는 것보다 x2ys의 빈틈이 안 생긴다.


## results

||en-es|es-en|en-fr|fr-en|en-de|de-en|en-ru|ru-en|en-zh|zh-en|en-it|it-en|
|:--:|:--:|:--:|:--:|:--:|--|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|MUSE|81.7|83.3|**82.3**|**82.4**|74.0|72.4|51.7|63.7|42.7|37.5|66.2 > 80.4 > 83.4|58.7 > 76.5 > 80.9|
|word2word(listall)|**84.2**|**85.5**|71.9|70.2|**82.1**|**80.3**|**60.9**|**65.1**|**55.7**|**59.0**|**81.7** > **89.9** > **90.5** | **84.7** > **91.1** > **91.9** | 
|word2word(setall)|**82.5**|**79.3**|83.9|80.9|**82.1**|**80.7**|**66.7**|**68.9**|**56.5**|**59.1**|**80.9** > **89.7** > **91.0** | **82.1** > **90.0** > **91.9** | 


|lang|lines|MUSE|word2word list|word2word set|
| -- | -- | -- | -- | -- |
|**en-es-P@1**|61,434,251|81.7|81.7|**82.5**|
|en-es-P@5|||89.9|**90.3**|
|en-es-P@10|||**91.7**|**91.7**|
|**es-en-P@1**||**83.3**|78.8|79.3|
|es-en-P@5|||**88.3**|**88.3**|
|es-en-P@10|||**90.1**|89.9|
|**en-fr-P@1**|41,763,488|82.3|83.5|**83.9**|
|en-fr-P@5|||**91.5**|**91.5**|
|en-fr-P@10|||**92.7**|92.5|
|**fr-en-P@1**||**82.4**|80.3|80.9|
|fr-en-P@5|||89.1|**89.3**|
|fr-en-P@10|||90.3|**90.4**|
|**en-de-P@1**|22,512,639|74.0|81.9|**82.1**|
|en-de-P@5|||90.4|**90.6**|
|en-de-P@10|||**91.6**|**91.6**|
|**de-en-P@1**||72.4|**80.7**|**80.7**|
|de-en-P@5|||87.5|**87.7**|
|de-en-P@10|||88.2|**88.3**|
|**en-ru-P@1**|25,910,105|51.7|66.2|**66.7**|
|en-ru-P@5|||79.7|**79.9**|
|en-ru-P@10|||**82.4**|**82.4**|
|**ru-en-P@1**||63.7|68.5|**68.9**|
|ru-en-P@5|||**79.9**|79.8|
|ru-en-P@10|||**81.0**|**81.0**|
|**en-zh-P@1**|4,772,273|42.7|55.7|**56.5**|
|en-zh-P@5|||**73.6**|73.5|
|en-zh-P@10|||75.5|**75.8**|
|**zh-en-P@1**||37.5|59.0|**59.1**|
|zh-en-P@5|||72.4|**72.8**|
|zh-en-P@10|||74.1|**74.3**|
|**en-it-P@1**|35,216,229|66.2|80.7|**80.9**|
|en-it-P@5||80.4|89.5|**89.7**|
|en-it-P@10||83.4|90.9|**91.0**|
|**it-en-P@1**||58.7|81.0|**82.1**|
|it-en-P@5||76.5|89.5|**90.0**|
|it-en-P@10||80.9|91.7|**91.9**|

set-all
en-es-P@1: 1238:82.5
en-es-P@5: 1354:90.3
en-es-P@10: 1376:91.7
es-en-P@1: 1189:79.3
es-en-P@5: 1324:88.3
es-en-P@10: 1349:89.9
en-fr-P@1: 1259:83.9
en-fr-P@5: 1372:91.5
en-fr-P@10: 1388:92.5
fr-en-P@1: 1213:80.9
fr-en-P@5: 1340:89.3
fr-en-P@10: 1356:90.4
en-de-P@1: 1231:82.1
en-de-P@5: 1359:90.6
en-de-P@10: 1374:91.6
de-en-P@1: 1210:80.7
de-en-P@5: 1316:87.7
de-en-P@10: 1325:88.3
en-ru-P@1: 1001:66.7
en-ru-P@5: 1198:79.9
en-ru-P@10: 1236:82.4
ru-en-P@1: 1034:68.9
ru-en-P@5: 1197:79.8
ru-en-P@10: 1215:81.0
en-zh_tw-P@1: 847:56.5
en-zh_tw-P@5: 1103:73.5
en-zh_tw-P@10: 1137:75.8
zh_tw-en-P@1: 886:59.1
zh_tw-en-P@5: 1092:72.8
zh_tw-en-P@10: 1115:74.3
en-it-P@1: 1214:80.9
en-it-P@5: 1345:89.7
en-it-P@10: 1365:91.0
it-en-P@1: 1231:82.1
it-en-P@5: 1350:90.0
it-en-P@10: 1378:91.9

en fr
1
2
en-fr-P@1: 1159:0.7726666666666666
en-fr-P@5: 1213:0.8086666666666666
fr en
1
2
fr-en-P@1: 1143:0.762
fr-en-P@5: 1193:0.7953333333333333

set
en fr
1
2
en-fr-P@1: 1103:0.7353333333333333
en-fr-P@5: 1211:0.8073333333333333
fr en
1
2
fr-en-P@1: 1069:0.7126666666666667
fr-en-P@5: 1184:0.7893333333333333

top
en-es-P@1: 1263:84.2
en-es-P@5: 1365:91.0
en-es-P@10: 1370:91.3
es-en-P@1: 1282:85.5
es-en-P@5: 1348:89.9
es-en-P@10: 1354:90.3
en-fr-P@1: 1079:71.9
en-fr-P@5: 1199:79.9
en-fr-P@10: 1222:81.5
fr-en-P@1: 1053:70.2
fr-en-P@5: 1181:78.7
fr-en-P@10: 1198:79.9
en-de-P@1: 1232:82.1
en-de-P@5: 1353:90.2
en-de-P@10: 1364:90.9
de-en-P@1: 1204:80.3
de-en-P@5: 1310:87.3
de-en-P@10: 1320:88.0
en-ru-P@1: 914:60.9
en-ru-P@5: 1116:74.4
en-ru-P@10: 1142:76.1
ru-en-P@1: 977:65.1
ru-en-P@5: 1113:74.2
ru-en-P@10: 1131:75.4
en-zh_tw-P@1: 836:55.7
en-zh_tw-P@5: 1104:73.6
en-zh_tw-P@10: 1133:75.5
zh_tw-en-P@1: 885:59.0
zh_tw-en-P@5: 1086:72.4
zh_tw-en-P@10: 1111:74.1
en-it-P@1: 1226:81.7
en-it-P@5: 1348:89.9
en-it-P@10: 1357:90.5
it-en-P@1: 1270:84.7
it-en-P@5: 1367:91.1
it-en-P@10: 1379:91.9

fr-30-1000000-5000
en fr
en-fr-P@1: 657:0.438
en-fr-P@5: 665:0.44333333333333336
fr en
fr-en-P@1: 772:0.5146666666666667
fr-en-P@5: 804:0.536

fr-30-1000000-50000
en fr
en-fr-P@1: 650:0.43333333333333335
en-fr-P@5: 664:0.44266666666666665
fr en
fr-en-P@1: 771:0.514
fr-en-P@5: 804:0.536

fr-20-1000000-50000
en fr
en-fr-P@1: 459:0.306
en-fr-P@5: 465:0.31
fr en
fr-en-P@1: 577:0.38466666666666666
fr-en-P@5: 593:0.3953333333333333

fr-40-1000000-50000
en fr
en-fr-P@1: 793:0.5286666666666666
en-fr-P@5: 820:0.5466666666666666
fr en
fr-en-P@1: 873:0.582
fr-en-P@5: 921:0.614

fr-50-1000000-5000
en fr
en-fr-P@1: 923:0.6153333333333333
en-fr-P@5: 960:0.64
fr en
fr-en-P@1: 962:0.6413333333333333
fr-en-P@5: 1022:0.6813333333333333

fr-60-1000000-5000
en fr
en-fr-P@1: 1003:0.6686666666666666
en-fr-P@5: 1053:0.702
fr en
fr-en-P@1: 1000:0.6666666666666666
fr-en-P@5: 1072:0.7146666666666667

fr-70-1000000-5000
en fr
en-fr-P@1: 1045:0.6966666666666667
en-fr-P@5: 1114:0.7426666666666667
fr en
fr-en-P@1: 1034:0.6893333333333334
fr-en-P@5: 1119:0.746

fr-80-1000000-5000
en fr
en-fr-P@1: 1071:0.714
en-fr-P@5: 1163:0.7753333333333333
fr en
fr-en-P@1: 1044:0.696
fr-en-P@5: 1151:0.7673333333333333

fr-90-1000000-5000
en fr
en-fr-P@1: 1075:0.7166666666666667
en-fr-P@5: 1185:0.79
fr en
fr-en-P@1: 1055:0.7033333333333334
fr-en-P@5: 1168:0.7786666666666666

fr-100-1000000-5000
en fr
en-fr-P@1: 1079:0.7193333333333334
en-fr-P@5: 1199:0.7993333333333333
fr en
fr-en-P@1: 1053:0.702
fr-en-P@5: 1181:0.7873333333333333
## References

If you use our software for research, please cite:
```bibtex
@misc{word2word2019,
  author = {Park, Kyubyong and Kim, Dongwoo and Choe, Yo Joong},
  title = {word2word},
  year = {2019},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/Kyubyong/word2word}}
}
```
(We may later update this bibtex with a reference to [our paper report](word2word-draft.pdf).)

All of our word-to-word translations were constructed from the publicly available
    [OpenSubtitles2018](http://opus.nlpl.eu/OpenSubtitles2018.php) dataset:
```bibtex
@article{opensubtitles2016,
  title={Opensubtitles2016: Extracting large parallel corpora from movie and tv subtitles},
  author={Lison, Pierre and Tiedemann, J{\"o}rg},
  year={2016},
  publisher={European Language Resources Association}
}
```

## Authors

[Kyubyong Park](https://github.com/Kyubyong), 
[Dongwoo Kim](https://github.com/kimdwkimdw), and 
[YJ Choe](https://github.com/yjchoe)

