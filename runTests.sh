#! /bin/bash
command -v source >/dev/null 2>&1 || {
  echo "I require source but it's not installed.  Aborting." >&2; exit 1;
}
source activate
pip install pytest-html
pytest --junit-xml=build/reports/TEST-report.xml



