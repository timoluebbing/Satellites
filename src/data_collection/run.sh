#!/bin/bash

# Path to the script above_45.sh
script_path="./api_call.sh"  # Replace this with the actual path if located elsewhere

# Loop indefinitely
while true
do
    echo "Running $script_path"
    bash "$script_path"  # Execute the above_45.sh script using Bash
    sleep 5  # Sleep for 5 sek
done

