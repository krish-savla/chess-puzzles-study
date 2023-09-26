#!/bin/bash
trap 'kill $BGPID; exit' INT
if [ -z "$1" ]
  then
    cd python_servers
    python3 pyserv.py &
    BGPID=$!
    cd ..
    npm run start
  else # any cmd line arg.
    cd python_servers
    python3 pyserv_ab.py &
    BGPID=$!
    cd ..
    npm run start_ab
fi
