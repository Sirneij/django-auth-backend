#!/usr/bin/env bash

# checks whether or not the source files conform with black and isort formatting
black --skip-string-normalization --check tests
black --skip-string-normalization --check src
isort --atomic --profile black -c src
isort --atomic --profile black -c tests

cd src

# Exits with non-zero code if there is any model without a corresponding migration file
python manage.py makemigrations --check --dry-run

# Uses propector to ensure that the source code conforms with Python best practices
prospector  --profile=../.prospector.yml --path=. --ignore-patterns=static

# Analysis and checks whether or not we have common security issues in our Python code. 
bandit -r . -ll

# Checks for correct annotations
mypy .