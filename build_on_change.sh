#!/bin/bash

fswatch -e ".*" -i ".*/[^.]*\\.py$" -0 . | xargs -0 -n 1 -I {} python {}

