#!/bin/bash
command -v source >/dev/null 2>&1 || {
  echo "I require source but it's not installed.  Aborting." >&2; exit 1;
}


virtualenv -p python3 env
source env/bin/activate


pip install jprops

python setup.py sdist --formats=zip

pip install pytest-html
pip install requests
pip install py4j

if [ -z "$1" ]
  then
    echo "No Tests will run"
  else
    pytest --metadata proactive_url $1 --metadata username $2 --metadata password $3 --junit-xml=build/reports/TEST-report.xml  
fi



