#!/bin/bash

while true; do
    ./s.sh
    minecraft_pid=$!
    sleep 1800
    kill $minecraft_pid
    wait $minecraft_pid 2>/dev/null
done
