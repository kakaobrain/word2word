[![image](https://img.shields.io/pypi/v/word2word.svg)](https://pypi.org/project/word2word/)
[![image](https://img.shields.io/pypi/l/word2word.svg)](https://pypi.org/project/word2word/)
[![image](https://img.shields.io/pypi/pyversions/word2word.svg)](https://pypi.org/project/word2word/)
[![image](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/kimdwkimdw)

# word2word

Easy-to-use word-to-word translations for 3,564 language pairs.

[https://arxiv.org/abs/1911.12019](https://arxiv.org/abs/1911.12019)

## Key Features

* A large collection of freely & publicly available word-to-word translations 
    **for 3,564 language pairs across 62 unique languages.** 
* Easy-to-use Python interface.
* Constructed using an efficient approach that is quantitatively examined by 
    proficient bilingual human labelers.

## Usage

First, install the package using `pip`:
```shell script
pip install word2word
```

OR

```shell script
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

For more details, see the Methodology section of [our arXiv paper](https://arxiv.org/abs/1911.12019).


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

The dictionary can alternatively be built from the command line as follows:
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

If you use word2word for research, please cite [our arXiv paper](https://arxiv.org/abs/1911.12019):
```bibtex
@misc{choe2019word2word,
    title={word2word: A Collection of Bilingual Lexicons for 3,564 Language Pairs},
    author={Yo Joong Choe and Kyubyong Park and Dongwoo Kim},
    year={2019},
    eprint={1911.12019},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
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

