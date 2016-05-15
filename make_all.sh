#!/bin/bash

set -ex

python ./passasjerer_lufttransport.py
python ./flytrafikk.py
python ./koyrelengde.py

cp -fv *.png output/.
