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
#       'cytopathies', 'myopathies']
```

The dictionary can alternatively be built from the command line as follows:
```bash
python make.py --lang1 en --lang2 fr --datapref data/pubmed.en-fr
```
Then, the custom lexicon can be loaded analogously in Python:
```python
from word2word import Word2word
my_en2fr = Word2word.load("en", "fr", "data/pubmed.en-fr")
# Loaded word2word custom bilingual lexicon from data/pubmed.en-fr.word2word/en-fr.pkl
```


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

