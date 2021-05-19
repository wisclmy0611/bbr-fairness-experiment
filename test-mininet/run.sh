#!/bin/bash
set -e


rm -rf outputs/*

./run_1c.sh

chown -R mininet:mininet outputs
