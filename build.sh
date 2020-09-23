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
pip3 install -U pip
pip3 install virtualenv
pip3 list

virtualenv -p python3 env
#virtualenv -p python2 env
source env/bin/activate

pip3 list
pip3 install jprops
pip3 install py4j==0.10.8.1
pip3 install pytest-html requests cloudpickle
python setup.py sdist --formats=zip
pip3 install dist/proactive*.zip
pip3 list

pip3 install sphinx
pip3 install sphinx-rtd-theme

cd docs
make html
cd ..

if [ -z "$1" ]
  then
    echo "No Tests will run"
  else
    pytest --metadata proactive_url "$1" --metadata username "$2" --metadata password "$3" --junit-xml=build/reports/TEST-report.xml
fi
