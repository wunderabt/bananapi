#!/bin/bash

# archives all files from a given SOURCE_DIR, encrypted with password, in chunks of 200MiB
# via 7z and syncs it with a webdav directory. Splitting it up in chunks should help to
# retry a sync after a network error.

set -e
set -x
SOURCE_DIR=/home/john
TARGET_DIR=/var/backup
## create a new backup-up directory
backup_dir=$(date +"%Y%m%d")
mkdir -p ${TARGET_DIR}/${backup_dir}
## remove old back-up dirs that are older than 10 days
find ${TARGET_DIR} -depth -maxdepth 1 -ctime +10 -exec rm -fr {} \;
## run the back-up
cd ${SOURCE_DIR}
7z a -t7z -mhe=on -pyourpassword -xr\!\*@eaDir\* -xr\!\*Drive/pics\* -v200m ${TARGET_DIR}/${backup_dir}/bkup.7z .
## copy to the cloud in the off hours
rclone sync ${TARGET_DIR} yourcloud:/backup --bwlimit "08:00,512 12:00,10M 13:00,512 18:00,30M 23:00,off"
