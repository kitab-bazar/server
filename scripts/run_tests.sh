#!/bin/bash -x

export PYTHONUNBUFFERED=1
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR=$(dirname "$BASE_DIR")


if [ "$CI" == "true" ]; then
    pip3 install coverage

    set -e
    # Wait until database is ready
    wait-for-it ${DATABASE_HOST:-db}:${DATABASE_PORT-5432}

    # To show migration logs
    ./manage.py test -v 2 config.tests.test_fake

    # Finally run test
    COVERAGE_PROCESS_START=`pwd`/.coveragerc COVERAGE_FILE=`pwd`/.coverage PYTHONPATH=`pwd` coverage run -m py.test --reuse-db --durations=10

    # Collect/Generate reports
    coverage report -i
    coverage html -i
    coverage xml

    mkdir -p $ROOT_DIR/coverage/
    mv htmlcov $ROOT_DIR/coverage/
    mv coverage.xml $ROOT_DIR/coverage/

    set +e
else
    py.test
fi
