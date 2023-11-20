#!/usr/bin/env bash

set -o errexit
set -o nounset

uvicorn --host 0.0.0.0 --reload app.main:app
