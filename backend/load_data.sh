#!/bin/sh

cd data/
python3 prepare_data.py
cd ..
python3 manage.py loaddata data/fixtures.json