#!/bin/bash

set -ex

docker build --tag=ivarref/koyrelengde-per-person .
docker run -v $(pwd)/output:/usr/src/app/output ivarref/koyrelengde-per-person
cp -fv output/*.png .

