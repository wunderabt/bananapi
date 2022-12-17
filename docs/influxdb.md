# Influx DB on banana pi

## Hint 1
/usr/lib/influxdb/scripts/influxd-systemd-start.sh

look for "sleep 1" and change to "sleep 5" or so. The Banana-pi is too slow :-)

## Hint 2

Turn off self monitoring to save power. Default causes CPU load every 10s.

in `/etc/influxdb/influxdb.conf` set

```
[monitor]
  # Whether to record statistics internally.
  store-enabled = false
```
