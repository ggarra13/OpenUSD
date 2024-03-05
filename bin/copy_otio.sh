#!/usr/bin/env bash

set -x

export ROOT=$PWD

if [[ $PWD == */bin ]]; then
    export ROOT=$ROOT/..
fi

. $ROOT/bin/env.sh

cp -r $INSTALL/bin/usdotio $ROOT/pxr/usd/bin/usdotio/usdotio.py

sed -i -e 's%#!/usr/bin/python.?%#!/pxrpythonsubst%' $ROOT/pxr/usd/bin/usdotio/usdotio.py

rm -rf $ROOT/extras/usd/examples/usdOtio
cp -r $INSTALL/share/usd/examples/plugin/usdOtio/ $ROOT/extras/usd/examples


cp -r $INSTALL/lib/python/usdOtio/ $ROOT/extras/usd/examples/usdOtio/python
rm -rf $ROOT/extras/usd/examples/usdOtio/python/__pycache__
