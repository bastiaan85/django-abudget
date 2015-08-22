#!/bin/bash
set -e
ROOT=`dirname "${BASH_SOURCE[0]}"`
export PYTHONDONTWRITEBYTECODE='dontwrite'
export DJANGO_SETTINGS_MODULE=abudget.settings.test
${ROOT}/venv.sh ./src/manage.py check
