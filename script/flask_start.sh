#!/bin/bash

set -e

sudo systemctl daemon-reload

sudo systemctl start flask.socket || { echo "flask.socket not started"; exit 1; }
sudo systemctl start flask.service || { echo "flask.service not started"; exit 1; }
sudo systemctl start nginx || { echo "nginx not started"; exit 1; }

echo "All services started"
