#!/bin/bash

cd $(dirname $0)

source /usr/local/bin/virtualenvwrapper.sh
workon dragonball
./scrape.py Dragon_Ball_Super

