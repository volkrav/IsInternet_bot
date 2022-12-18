#!/bin/bash
for i in {1..5}
do
 curl http://127.0.0.1:8000/ &>/dev/null
 sleep 3
done

