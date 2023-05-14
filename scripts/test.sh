#!/usr/bin/env bash
py.test -n 4 --disable-socket --nomigrations --reuse-db -W error::RuntimeWarning --cov=src --cov-report=html tests/