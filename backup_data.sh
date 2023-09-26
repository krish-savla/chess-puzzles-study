#!/bin/bash

# sync_data is the old way, but keep it around just in case. 
# sync_data() {
#     rsync -rtuv --partial --inplace --append --progress ./data/* $1@homework.cs.tufts.edu:/r/emotiondata/chesspuzzles/data/
# }
# sync_data "mrussell"


cd data/chess

python3 backup_and_rename_files.py