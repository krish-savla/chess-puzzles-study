#!/bin/bash

sync_data() {
    rsync -rtuv --partial --inplace --append --progress $1@homework.cs.tufts.edu:/r/emotiondata/chesspuzzles/data/* ./data/chess/uploaded/
}

sync_data "mrussell"