#!/bin/bash
echo --- RUNNING BUILD LOCAL ---
command -v source >/dev/null 2>&1 || {
  echo "I require source but it's not installed.  Aborting." >&2; exit 1;
}

python3 -m pip install virtualenv
virtualenv -p python3 env
source env/bin/activate

python3 -m pip install --upgrade pip
python3 -m pip -V

python3 -m pip install jprops
python3 -m pip install py4j
python3 -m pip install pytest-html requests cloudpickle

# generate ./build/proactive-XXX.zip
python3 setup.py sdist --formats=zip
# install
python3 -m pip install dist/proactive*.zip

python3 -m pip list
python3 -m pip -V

echo --- BUILD LOCAL DONE ---
