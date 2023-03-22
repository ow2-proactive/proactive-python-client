#!/bin/bash
command -v source >/dev/null 2>&1 || {
  echo "I require source but it's not installed.  Aborting." >&2; exit 1;
}

echo "HOME: $HOME"
echo "PWD: $PWD"

which python3
which pip3
python3 -V

curl https://bootstrap.pypa.io/pip/3.5/get-pip.py -o get-pip.py
python3 get-pip.py
hash -r
pip3 -V

# pip3 list
# pip3 install -U pip==20.3.4
pip3 install virtualenv
pip3 list

virtualenv -p python3 env
#virtualenv -p python2 env
source env/bin/activate

pip3 list
pip3 install -r requirements.txt

python setup.py sdist --formats=zip
pip3 install dist/proactive*.zip
pip3 list

cd docs
make html
cd ..

if [ -z "$1" ]
  then
    echo "No Tests will run"
  else
    pytest --metadata proactive_url "$1" --metadata username "$2" --metadata password "$3" --junit-xml=build/reports/TEST-report.xml
fi
