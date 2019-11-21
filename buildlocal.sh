#!/bin/bash
echo --- RUNNING BUILD LOCAL ---
command -v source >/dev/null 2>&1 || {
  echo "I require source but it's not installed.  Aborting." >&2; exit 1;
}

python setup.py sdist --formats=zip

echo --- BUILD LOCAL DONE ---
