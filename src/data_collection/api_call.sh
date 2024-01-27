#!/bin/bash

# api_call.sh
# create GET request to n2yo api to retrieve satellite positions above location x with degree alpha and
# and write to output file.
# Sebastian Volz, Januar 2024

# Function to make the GET request and append response with timestamp to the file
make_request() {
      # Accept API URL as first argument

    # Make the GET request and retrieve JSON response
    RESPONSE=$(curl -s "$API_URL")

    # Parse JSON response and add current timestamp field to it
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    UPDATED_RESPONSE=$(echo "$RESPONSE" | jq --arg timestamp "$TIMESTAMP" '. + {date: $timestamp}')

    # Save updated JSON response with added date field to the output file
    echo "$UPDATED_RESPONSE" >> "$OUTPUT_FILE"
    echo ";" >> "$OUTPUT_FILE"
    echo "Request at $TIMESTAMP to $API_URL completed and appended to $OUTPUT_FILE"
}

# Coordinates
latitude=48.5269
longitude=9.0632
alpha=90

# API Key
api_key="3HYWGU-QTAEST-5JUAFV-55O6"

# Construct API URL with variables
API_URL="https://api.n2yo.com/rest/v1/satellite/above/$latitude/$longitude/0/$alpha/0/&apiKey=$api_key"
OUTPUT_FILE="satellite_above_tue_90_5sek.txt"  # Accept output file as second argument

make_request

