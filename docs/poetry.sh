#!/bin/bash

START=$PWD

poetry show -n --no-dev --no-ansi

for dir in other/*; do
    if [ -d "$dir" ]; then
        cd $dir
        # We don't know if the other dir is locked or not
        poetry lock > /dev/null
        poetry show -n --no-dev --no-ansi
        cd $START
    fi
done

