#!/bin/bash

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


API_URL="https://api.n2yo.com/rest/v1/satellite/above/48.782536/9.176995/0/90/0/&apiKey=3HYWGU-QTAEST-5JUAFV-55O6"
OUTPUT_FILE="satellite_above_tue_90_5sek.txt"  # Accept output file as second argument

# Call make_request function with API URL and output file arguments
make_request 

API_URL="https://api.n2yo.com/rest/v1/satellite/above/41.52/12.29/0/90/0/&apiKey=3HYWGU-QTAEST-5JUAFV-55O6"
OUTPUT_FILE="satellite_above_rome_45.txt"  # Accept output file as second argument

