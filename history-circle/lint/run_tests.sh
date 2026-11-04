#!/bin/sh
# 합성 샘플로 모든 검사를 시험한다(크레딧 없음). 사용: sh run_tests.sh
cd "$(dirname "$0")/tests" && PYTHONPATH=..:. python3 -W ignore -m unittest discover -s . -p "test_*.py" "$@"
