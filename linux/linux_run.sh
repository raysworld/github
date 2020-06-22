#!/bin/bash

# the absolute path of this script
BASE_PATH=$(dirname $(readlink -f $0))
# the path of the python executable
PATHON_EXEC='/usr/bin/python3'

${PATHON_EXEC} ${BASE_PATH}/../github_hosts.py
if [ $? -ne 0 ]; then
    echo "get host name error"
    exit 1
fi

sed -i "/GitHub Start/d" /etc/hosts
sed -i "/GitHub End/d" /etc/hosts

# Clear /etc/hosts first
for i in `cat ${BASE_PATH}/../github_domain.txt`; do
    sed -i "/$i/d" /etc/hosts
done

# Add dns record at /etc/hosts
IFS_OLD=$IFS
IFS=$'\n'
ALINES=$(cat ${BASE_PATH}/../github_hosts.txt)
for ALINE in $ALINES;do
    echo $ALINE >> /etc/hosts
done
IFS=$IFS_OLD
