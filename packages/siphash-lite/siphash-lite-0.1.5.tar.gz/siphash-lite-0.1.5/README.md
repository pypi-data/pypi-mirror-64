# SipHash Lite

[SipHash](https://en.wikipedia.org/wiki/SipHash) implementation ported from [redis](https://github.com/antirez/redis/blob/e8afadd52c32c656d56ea9d5b235881f04c9bd8a/src/siphash.c).

![Python package](https://github.com/cordalace/siphash-lite/workflows/Python%20package/badge.svg)
[![pypi](https://img.shields.io/pypi/v/siphash-lite)](https://pypi.python.org/pypi/siphash-lite)

## Installation

Install using [pip](https://pypi.org/project/siphash-lite/) with:
```
pip install siphash-lite
```

## Usage

```python
>>> import siphash

>>> siphash.siphash(b'hello world', b'1234567812345678')
9929133401751744512
```
