#!/usr/bin/env bash
py.test -n 4 --nomigrations --reuse-db -W error::RuntimeWarning --cov=src --cov-report=html tests/