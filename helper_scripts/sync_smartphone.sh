#!/bin/bash
set -e

# prep
mkdir -p /mnt/smartphone
mkdir -p /tmp/rsync

jmtpfs /mnt/smartphone

# sync
rsync --recursive --size-only --human-readable --delete --verbose \
      --exclude=".*" --exclude="*.jpg" --exclude="*.png" --exclude="*.jpeg" --exclude="*.JPG" \
      --temp-dir=/tmp/rsync /home/multimedia/mp3s /mnt/smartphone/disk/Music/ |& tee sync_mp3.log
rsync --recursive --size-only --human-readable --delete --verbose \
      --temp-dir=/tmp/rsync /home/uwe/tonline_bkup/lowrespics /mnt/smartphone/disk/Pictures/ |& tee sync_pic.log

# teardown/cleanup
fusermount -u /mnt/smartphone

rmdir /mnt/smartphone
rm -fr /tmp/rsync
