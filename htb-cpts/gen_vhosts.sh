#!/bin/bash

DSTIP="${1}"
READFR="${2}"

if [[ -z $DSTIP ]] || [[ -z $READFR ]]; then
    echo "${0} <dest ip> <vhosts-lists.txt>"
    exit 1
fi

while read -r line; do
    echo -e "${DSTIP}  $line"
done < "${READFR}"

