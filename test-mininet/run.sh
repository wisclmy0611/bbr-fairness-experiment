#!/bin/bash
set -e

rm -rf outputs/*
./fairness.py
chown -R mininet:mininet outputs
