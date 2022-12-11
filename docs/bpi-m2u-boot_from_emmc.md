(only needed for some images)

$ bpi-copy 2022-10-18-ubuntu-18.04-mate-desktop-k4.19-bpi-m2b-sd-emmc.img.zip /dev/mmcblk1

$ mount /dev/mmcblk1 /mnt
$ cd /mnt
$ find . -type f -exec grep -H mmcblk0 {} \; > /tmp/matches
$ grep Binary /tmp/matches | cut -d " " -f3 | xargs sudo sed -i 's/mmcblk0/mmcblk1/g'
$ grep -v Binary /tmp/matches | cut -d : -f 1 | xargs sudo sed -i 's/mmcblk0/mmcblk1/g'

