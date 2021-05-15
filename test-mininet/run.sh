#!/bin/bash
set -e

pip3 install matplotlib

rm -rf outputs/*

./run_1c.sh

chown -R mininet:mininet outputs
