#!/usr/bin/env bash

# Get the directory of the script being executed
# If sourced, this will be the directory of the sourced script
# If executed directly, this will be the directory of the script itself
INSTALL="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL="${INSTALL%/bin}"

plugin_dir=$INSTALL/share/usd/examples/plugin
export PYTHONPATH=$INSTALL/lib/python:$plugin_dir/usdOtio:$PYTHONPATH
export PXR_PLUGINPATH_NAME=$plugin_dir/usdOtio:$PXR_PLUGINPATH_NAME
