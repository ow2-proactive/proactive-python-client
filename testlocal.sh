#!/bin/bash
echo --- RUNNING TEST LOCAL ---
command -v source >/dev/null 2>&1 || {
  echo "I require source but it's not installed.  Aborting." >&2; exit 1;
}

if [ -z "$1" ]
  then
    echo "No Tests will run"
  else
    pytest --metadata proactive_url $1 --metadata username $2 --metadata password $3 --junit-xml=build/reports/TEST-report.xml  
fi

echo --- TEST LOCAL DONE ---
