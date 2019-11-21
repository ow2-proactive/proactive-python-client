#!/bin/bash
echo --- RUNNING INSTALL LOCAL ---
command -v source >/dev/null 2>&1 || {
  echo "I require source but it's not installed.  Aborting." >&2; exit 1;
}

pip install dist/proactive*.zip

echo --- INSTALL LOCAL DONE ---
