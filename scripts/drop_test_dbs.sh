#!/bin/bash

PREFIX='test' || '_sqlx_test'
export PGPASSWORD=password
export PGUSER=quickcheck
export PGHOST=localhost
export PGPORT=5432

TEST_DB_LIST=$(psql -l | awk '{ print $1 }' | grep '^[a-z]' | grep -v template | grep -v postgres)
for TEST_DB in $TEST_DB_LIST ; do
    if [ $(echo $TEST_DB | sed "s%^$PREFIX%%") != $TEST_DB ]
    then
        echo "Dropping $TEST_DB"
        dropdb --if-exists $TEST_DB
    fi
done
