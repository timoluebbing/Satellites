#!/bin/bash

# run.sh
# call api_call for duration_minutes of time in interval of x seconds
# Sebastian Volz, Januar 2024


# Path to the script above_45.sh
script_path="./api_call.sh"  # Replace this with the actual path if located elsewhere


# Set the duration in minutes
duration_minutes=10  # Change this to the desired duration

# Set sleep interval in seconds
sleep_interval=5

# Calculate the end time
end_time=$((SECONDS + duration_minutes * 60))


# Loop until the current time is less than the end time
while [ $SECONDS -lt $end_time ]
do
    echo "Running $script_path"
    bash "$script_path"  # Execute the above_45.sh script using Bash
    sleep "$sleep_interval"  # Sleep for 5 sek
done

echo "Script execution completed for $duration_minutes minutes."

