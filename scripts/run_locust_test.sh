#!/bin/bash

# Configuration
HOST="http://localhost:8000"  # Target host to test
USERS=50                      # Number of simulated users
SPAWN_RATE=5                  # How many users to spawn per second (reduced for more gradual ramp-up)
RUN_TIME="2m"                 # Increased run time to allow for gradual ramp-up
DB_TYPE="sqlite"              # Database type (sqlite, postgres, etc.)
SERVER_TYPE="wsgi_gunicorn"   # Server type (asgi_gunicorn, wsgi_gunicorn, asgi_daphne)
WORKER_COUNT=4                # Number of workers
CSV_PREFIX="locust_${DB_TYPE}_${SERVER_TYPE}_${WORKER_COUNT}"  # Prefix for CSV files
TEST_FILE="tests/load/locustfile.py"  # Path to locustfile

# Create a results directory if it doesn't exist
RESULTS_DIR="locust_results"
mkdir -p $RESULTS_DIR

# Get current date/time for unique filenames
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Run locust in headless mode with CSV output
echo "Starting Locust test with $USERS users at a rate of $SPAWN_RATE users/second for $RUN_TIME..."

# Use a more reliable approach for gradual user spawning
locust -f $TEST_FILE \
  --host=$HOST \
  --users=$USERS \
  --spawn-rate=$SPAWN_RATE \
  --run-time=$RUN_TIME \
  --headless \
  --csv="$RESULTS_DIR/${CSV_PREFIX}_${TIMESTAMP}" \
  --html="$RESULTS_DIR/${CSV_PREFIX}_${TIMESTAMP}.html" \
  --only-summary

echo "Test completed. Results saved to $RESULTS_DIR/${CSV_PREFIX}_${TIMESTAMP}"
echo "CSV files:"
echo "  - $RESULTS_DIR/${CSV_PREFIX}_${TIMESTAMP}_stats.csv (Request statistics)"
echo "  - $RESULTS_DIR/${CSV_PREFIX}_${TIMESTAMP}_stats_history.csv (Time series statistics)"
echo "  - $RESULTS_DIR/${CSV_PREFIX}_${TIMESTAMP}_failures.csv (Failed requests)"
echo "  - $RESULTS_DIR/${CSV_PREFIX}_${TIMESTAMP}_exceptions.csv (Python exceptions)"
echo "HTML report: $RESULTS_DIR/${CSV_PREFIX}_${TIMESTAMP}.html" 