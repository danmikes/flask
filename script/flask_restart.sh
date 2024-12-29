#!/bin/bash

set -e

sudo systemctl daemon-reload

sudo systemctl restart flask.socket || { echo "flask.socket not restarted"; exit 1; }
sudo systemctl restart flask.service || { echo "flask.service not restarted"; exit 1; }
sudo systemctl restart nginx || { echo "nginx not restarted"; exit 1; }

echo "All services restarted"
