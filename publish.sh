#!/bin/bash
command -v source >/dev/null 2>&1 || {
  echo "I require source but it's not installed.  Aborting." >&2; exit 1;
}

virtualenv -p python3 env
source env/bin/activate

pip list
pip install twine

if [[ $JENKINS_JNLP_URL ]]
then
   twine upload -r pypi dist/* --config-file /home/activeeon/.pypirc
else
   twine upload -r pypi dist/*
fi