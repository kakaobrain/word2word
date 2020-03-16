[![image](https://img.shields.io/pypi/v/word2word.svg)](https://pypi.org/project/word2word/)
[![image](https://img.shields.io/pypi/l/word2word.svg)](https://pypi.org/project/word2word/)
[![image](https://img.shields.io/pypi/pyversions/word2word.svg)](https://pypi.org/project/word2word/)
[![image](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/kimdwkimdw)

# word2word

Easy-to-use word translations for 3,564 language pairs.

This is the official code accompanying [our LREC 2020 paper](https://arxiv.org/abs/1911.12019).

## Summary

* A large collection of freely & publicly available bilingual lexicons
    **for 3,564 language pairs across 62 unique languages.** 
* Easy-to-use Python interface for accessing top-k word translations and 
    for building a new bilingual lexicon from a custom parallel corpus.
* Constructed using a simple approach that yields bilingual lexicons with 
    high coverage and competitive translation quality.

## Usage

First, install the package using `pip`:
```shell script
pip install word2word
```

OR

```shell script
git clone https://github.com/kakaobrain/word2word
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

Our approach computes top-k word translations based on 
the co-occurrence statistics between cross-lingual word pairs in a parallel corpus.
We additionally introduce a correction term that controls for any confounding effect
coming from other source words within the same sentence.
The resulting method is an efficient and scalable approach that allows us to
construct large bilingual dictionaries from any given parallel corpus. 

For more details, see the Methodology section of [our paper](https://arxiv.org/abs/1911.12019).


## Building a Bilingual Lexicon on a Custom Parallel Corpus

The `word2word` package also provides interface for 
building a custom bilingual lexicon using a different parallel corpus.
Here, we show an example of building one from 
the [Medline English-French dataset](https://drive.google.com/drive/folders/0B3UxRWA52hBjQjZmYlRZWHQ4SUE): 
```python
from word2word import Word2word

# custom parallel data: data/pubmed.en-fr.en, data/pubmed.en-fr.fr
my_en2fr = Word2word.make("en", "fr", "data/pubmed.en-fr")
# ...building...
print(my_en2fr("mitochondrial"))
# out: ['mitochondriale', 'mitochondriales', 'mitochondrial', 
#       'cytopathies', 'mitochondriaux']
```

When built from source, the bilingual lexicon can also be constructed from the command line as follows:
```shell script
python make.py --lang1 en --lang2 fr --datapref data/pubmed.en-fr
```

In both cases, the custom lexicon (saved to `datapref/` by default) can be re-loaded in Python:
```python
from word2word import Word2word
my_en2fr = Word2word.load("en", "fr", "data/pubmed.en-fr")
# Loaded word2word custom bilingual lexicon from data/pubmed.en-fr/en-fr.pkl
```

### Multiprocessing

In both the Python interface and the command line interface, 
`make` uses multiprocessing with 16 CPUs by default.
The number of CPU workers can be adjusted by setting 
`num_workers=N` (Python) or `--num_workers N` (command line).

## References

If you use word2word for research, please cite [our paper](https://arxiv.org/abs/1911.12019):
```bibtex
@inproceedings{choe2020word2word,
 author = {Yo Joong Choe and Kyubyong Park and Dongwoo Kim},
 title = {word2word: A Collection of Bilingual Lexicons for 3,564 Language Pairs},
 booktitle = {Proceedings of the 12th International Conference on Language Resources and Evaluation (LREC 2020)},
 year = {2020}
}
```

All of our pre-computed bilingual lexicons were constructed from the publicly available
    [OpenSubtitles2018](http://opus.nlpl.eu/OpenSubtitles2018.php) dataset:
```bibtex
@inproceedings{lison-etal-2018-opensubtitles2018,
    title = "{O}pen{S}ubtitles2018: Statistical Rescoring of Sentence Alignments in Large, Noisy Parallel Corpora",
    author = {Lison, Pierre  and
      Tiedemann, J{\"o}rg  and
      Kouylekov, Milen},
    booktitle = "Proceedings of the Eleventh International Conference on Language Resources and Evaluation ({LREC} 2018)",
    month = may,
    year = "2018",
    address = "Miyazaki, Japan",
    publisher = "European Language Resources Association (ELRA)",
    url = "https://www.aclweb.org/anthology/L18-1275",
}
```

## Authors

[Kyubyong Park](https://github.com/Kyubyong), 
[Dongwoo Kim](https://github.com/kimdwkimdw), and 
[YJ Choe](https://github.com/yjchoe)

