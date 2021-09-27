#!/bin/bash

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

set -e

DIR="$(dirname "$0")"
case $1 in
  "integ-test")
  echo "${@:2}"
  "$DIR/run.sh" "$DIR/src/run_integ_test.py" "${@:2}"
  ;;
  "bwc-test")
  echo "${@:2}"
  "$DIR/run.sh" "$DIR/src/run_bwc_test.py" "${@:2}"
  ;;
  *)
  echo "Invalid Test suite"
  exit 1
  ;;
esac

