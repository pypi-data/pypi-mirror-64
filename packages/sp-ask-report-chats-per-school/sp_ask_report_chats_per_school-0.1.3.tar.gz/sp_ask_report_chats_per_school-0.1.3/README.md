# Ask Schools

[
![PyPI](https://img.shields.io/pypi/v/sp_ask_report_chats_per_school.svg)
![PyPI](https://img.shields.io/pypi/pyversions/sp_ask_report_chats_per_school.svg)
![PyPI](https://img.shields.io/github/license/guinslym/sp_ask_report_chats_per_school.svg)
](https://pypi.org/project/sp_ask_report_chats_per_school/)
[![TravisCI](https://travis-ci.org/guinslym/sp_ask_report_chats_per_school.svg?branch=master)](https://travis-ci.org/guinslym/sp_ask_report_chats_per_school)


This package helps to filter Chats


## Installation

**Ask Schools** can be installed from PyPI using `pip` or your package manager of choice:

```
pip install sp_ask_report_chats_per_school
```

## Usage


Example:

```python

from sp_ask_report_chats_per_school import get_nbr_of_chats_per_school_for_this_day

chats_DataFrame = get_nbr_of_chats_per_school_for_this_day(year=2020, month=3, day=11)
chats_DataFrame.to_excel("chats_per_school.xlsx", index=True)

```

## Code of Conduct

Everyone interacting in the project's codebases, issue trackers, chat rooms, and mailing lists is expected to follow the [PyPA Code of Conduct](https://www.pypa.io/en/latest/code-of-conduct/).
