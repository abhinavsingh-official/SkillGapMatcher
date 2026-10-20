# Attribution

The `pydparser` package in this directory is vendored from
[Justicea83/pydparser](https://github.com/Justicea83/pydparser), MIT licensed
(see `LICENSE-pydparser.txt`). It is vendored directly rather than pip-installed
so two real bugs found while integrating it could be fixed in place:

- `utils.py`'s `extract_text()` had no code path for `.txt` input (only
  `.pdf`/`.docx`/`.doc`), but this project's UX is paste-as-text. Added a
  `.txt` branch.
- `job_parser.py`'s `__get_basic_details()` read `cust_tags['DOMAIN']` with no
  guard, unlike every other field in the same function — a bare `KeyError` on
  any job description with no recognized domain entity (a common case). Fixed
  to `cust_tags.get('DOMAIN')`.

No other changes were made to the vendored code. `matcher.py` in the project
root imports it and adds the actual differentiating feature: a skills-gap
breakdown, not just a single similarity score.
