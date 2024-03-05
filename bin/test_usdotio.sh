#!/usr/bin/env bash

test_usdotio()
{
    otio=$1
    usd=$2

    usd_out=/tmp/test.usda
    otio_out=/tmp/test.otio

    otio_cat=/tmp/orig_cat.otio
    otio_out_cat=/tmp/new_cat.otio

    usdotio add -o "${usd_out}" "${otio}" "${usd}"

    usdview ${usd_out}
    exit 0
    
    usdotio save "${otio_out}" "${usd_out}"

    otiocat "${otio}" > "${otio_cat}"
    otiocat "${otio_out}" > "${otio_out_cat}"

    error=`diff -w ${otio_cat} ${otio_out_cat}`
    if [[ "${error}" != "" ]]; then
	echo "usd file ${usd_out}"
	echo "${otio}" "${otio_out}"
	meld "${otio_cat}" "${otio_out_cat}"
	exit 1
    else
	echo "MATCHING FILES"
    fi
}


export ROOT=$PWD

if [[ $PWD == */bin ]]; then
    export ROOT=$ROOT/..
fi

. $ROOT/bin/env.sh

cd ~/Movies

file=nested_stack.otio
test_usdotio $file ~/assets/sphere.usda

# for i in *.otio; do
#     test_usdotio $i ~/assets/sphere.usda
# done

# cd ~/code/applications/mrv2/tlRender/etc/SampleData
# for i in *.otio; do
#     test_usdotio $i ~/assets/sphere.usda
# done
