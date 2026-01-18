#!/bin/sh
echo "Starting CPU stress test for 30 seconds..."
dd if=/dev/urandom | head -c 100M | bzip2 > /dev/null
echo "Test finished."
