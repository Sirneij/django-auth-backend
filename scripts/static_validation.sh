#!/usr/bin/env bash
black --skip-string-normalization --line-length 120 --check tests
black --skip-string-normalization --line-length 120 --check src

isort --atomic --profile black -c src
isort --atomic --profile black -c tests

cd src || exit 1

python manage.py makemigrations --check --dry-run

prospector  --profile=../.prospector.yml --path=. --ignore-patterns=static

bandit -r .

mypy .