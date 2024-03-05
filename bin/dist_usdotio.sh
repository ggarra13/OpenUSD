#!/usr/bin/env bash


export ROOT=$PWD

if [[ $PWD == */bin ]]; then
    export ROOT=$ROOT/..
fi

. $ROOT/bin/env.sh

cd $ROOT

rm -rf $INSTALL/lib/python/usdOtio/__pycache__

cd $INSTALL
zip -r usdotio.zip bin/usdotio bin/usdotio.cmd lib/python/usdOtio share/usd/examples/plugin/usdOtio scripts/usdotio.bat usdOtio_README.txt
