# Release notes

<!-- do not remove -->

## 0.0.3

### New Features

- Add support for path arguments via `__` parameter ([#2](https://github.com/AnswerDotAI/fastgit/pull/2)), thanks to [@ncoop57](https://github.com/ncoop57)

**Usage:**
```python
g.log('--oneline', __=['file1.py', 'file2.py'])
# → git log --oneline -- file1.py file2.py
```


## 0.0.2

### New Features

- Fix boolean kwargs: --flag instead of --flag=True ([#1](https://github.com/AnswerDotAI/fastgit/pull/1)), thanks to [@jph00](https://github.com/jph00)


## 0.0.1

- Initial release

