#!/bin/bash

# Define the path to the script that will invoke the endpoint
INVOKE_SCRIPT="./invoke_emails.sh"  # Update this path
LOGFILE="./logfile.log"  # Update this path

# Create the invoke script if it doesn't exist
cat << 'EOF' > "$INVOKE_SCRIPT"
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
EOF

# Make the invoke script executable
chmod +x "$INVOKE_SCRIPT"

# Set up the cron job
CRON_JOB="*/1 * * * * $INVOKE_SCRIPT >> $LOGFILE 2>&1"

# Check if the cron job already exists
(crontab -l | grep -v -F "$INVOKE_SCRIPT"; echo "$CRON_JOB") | crontab -
echo "Cron job set up to run every 10 minutes."