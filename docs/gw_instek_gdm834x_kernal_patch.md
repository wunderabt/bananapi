# Patch kernal to access GW Instek GDM-8341 and GDM-8342 (GDM-834x)

Tested on 5.11.0-34-generic, Ubuntu 21.04

`lsusb` showed

```
Bus 001 Device 002: ID 2184:0030 GW Instek GDM834X VCP PORT
```

Install kernel sources `apt install kernel-source`

Unpack, go to `driver/usb/serial`, edit cp210x.c and add the ID

```
{ USB_DEVICE(0x2184, 0x0030) }, /* GwINSTEK GDM-834x */
```

compile module in that directory

```
make -C /lib/modules/$(uname -r)/build M=$PWD
```

copy it to the kernel

```
cp <compile-path>/cp210x.ko /usr/lib/modules/$(uname -r)/kernel/drivers/usb/serial
```

unload old module and load new driver

```
modprobe -r cp210x
modprobe cp210x
```

check dmesg

```
[ 1102.647125] usbcore: registered new interface driver usbserial_generic
[ 1102.647133] usbserial: USB Serial support registered for generic
[ 1102.647416] cp210x: loading out-of-tree module taints kernel.
[ 1102.647484] cp210x: module verification failed: signature and/or required key missing - tainting kernel
[ 1102.647885] usbcore: registered new interface driver cp210x
[ 1102.647893] usbserial: USB Serial support registered for cp210x
[ 1102.647908] cp210x 1-2:1.0: cp210x converter detected
[ 1102.650572] usb 1-2: cp210x converter now attached to ttyUSB0
```

done
