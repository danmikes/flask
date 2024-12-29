#!/bin/bash

set -e

sudo systemctl status flask.socket --no-pager
sudo systemctl status flask.service --no-pager
sudo systemctl status nginx --no-pager
sudo nginx -t
