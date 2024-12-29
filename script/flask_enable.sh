#!/bin/bash

set -e

sudo systemctl enable flask.socket || { echo "flask.socket not enabled"; exit 1; }
sudo systemctl enable flask.service || { echo "flask.service not enabled"; exit 1; }
sudo systemctl enable nginx || { echo "nginx not enabled"; exit 1; }

echo "All services enabled"
