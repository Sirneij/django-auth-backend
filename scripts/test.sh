#!/usr/bin/env bash
py.test -n auto --nomigrations --reuse-db -W error::RuntimeWarning --cov=src --cov-report=html tests/