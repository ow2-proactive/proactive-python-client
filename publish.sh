#!/bin/bash
command -v source >/dev/null 2>&1 || {
  echo "I require source but it's not installed.  Aborting." >&2; exit 1;
}
virtualenv -p python3 env
source env/bin/activate

pip install twine

twine upload -r pypi dist/*