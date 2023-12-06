#!/bin/bash
source ../auth-token.sh
mkdir -p day${1}
cd day${1}
cp -n ../.day_template.py day${1}.py
python ../fetch.py

