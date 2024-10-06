#!/bin/bash

generate_id() {
    echo $((RANDOM % 100 + 1))
}

generate_info() {
    echo "Information$((RANDOM % 10000))"
}

for i in {1..10}; do
    echo "$(generate_info)"
    echo "P: $(generate_id)"
    echo "C: $(generate_id)"
done