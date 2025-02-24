#!/bin/bash
# URL of the FastAPI endpoint
URL="http://localhost:8000/v1/emails"

# Use curl to invoke the endpoint
response=$(curl --write-out "%{http_code}\n" --silent --output /dev/null "$URL")

if [ "$response" -eq 200 ]; then
    echo "Successfully invoked endpoint: $URL, Status Code: $response"
else
    echo "Failed to invoke endpoint: $URL, Status Code: $response"
fi
