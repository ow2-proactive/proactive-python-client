#!/bin/bash
command -v source >/dev/null 2>&1 || {
  echo "I require source but it's not installed.  Aborting." >&2; exit 1;
}

echo "HOME: $HOME"
echo "PWD: $PWD"

which python3
which pip3
python3 -V
pip3 -V

pip3 list
virtualenv -p python3 env
source env/bin/activate

pip3 list
pip3 install twine
pip3 list

# find / -name .pypirc
PYPIRC_FILE=/home/activeeon/.pypirc
if [ -f "$PYPIRC_FILE" ]; then
  echo "$PYPIRC_FILE exist"
  twine upload -r pypi dist/* --config-file $PYPIRC_FILE
  echo "Done"
else
  echo "$PYPIRC_FILE does not exist"
  echo "The upload to pypi was aborted!"
fi
