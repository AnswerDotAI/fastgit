# Release notes

<!-- do not remove -->

## 0.1.3

### New Features

- Add pluggable runner param to callgit/acallgit/Git/get_top so command execution can be replaced ([#13](https://github.com/AnswerDotAI/fastgit/issues/13))

### Bugs Squashed

- Render 2-3 letter kwargs as short-flag clusters ([#14](https://github.com/AnswerDotAI/fastgit/pull/14)), thanks to [@jph00](https://github.com/jph00)


## 0.1.2

### New Features

- Add async support via sync=False and acallgit; refactor callgit into shared helpers ([#12](https://github.com/AnswerDotAI/fastgit/issues/12))
- Treat git query commands exit 1 as success, returning output as GitRes with returncode ([#11](https://github.com/AnswerDotAI/fastgit/issues/11))


## 0.1.1

### New Features

- Make Git error output terse and git-style (single line with command and stderr) ([#8](https://github.com/AnswerDotAI/fastgit/issues/8))


## 0.1.0

### Breaking Changes

- `split` param removed; stderr added to output

### New Features

- Refactor callgit to return combined stdout/stderr string; add `raise_exc` option and `current_branch` property ([#7](https://github.com/AnswerDotAI/fastgit/issues/7))


## 0.0.6

### New Features

- Add pre param to `call_git` ([#6](https://github.com/AnswerDotAI/fastgit/issues/6))


## 0.0.5

### New Features

- Add `head_sha` property to Git class ([#5](https://github.com/AnswerDotAI/fastgit/issues/5))


## 0.0.4

### New Features

- Add tilde expansion support for paths ([#4](https://github.com/AnswerDotAI/fastgit/pull/4)), thanks to [@ncoop57](https://github.com/ncoop57)


## 0.0.3

### New Features

- Add support for path arguments via `__` parameter ([#2](https://github.com/AnswerDotAI/fastgit/pull/2)), thanks to [@ncoop57](https://github.com/ncoop57)


## 0.0.2

### New Features

- Fix boolean kwargs: --flag instead of --flag=True ([#1](https://github.com/AnswerDotAI/fastgit/pull/1)), thanks to [@jph00](https://github.com/jph00)


## 0.0.1

- Initial release
