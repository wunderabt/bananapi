# Mali Graphics on Banana-Pi M1 with All-Winner A20 chip

Basic instructions taken from https://bootlin.com/blog/mali-opengl-support-on-allwinner-platforms-with-mainline-linux/

The steps below were done with `ARMBIAN 5.70 stable Debian GNU/Linux 9 (stretch) 4.19.13-sunxi`

On a x86-64 PC running ubuntu install

    sudo apt install gcc-arm-linux-gnueabihf quilt
    
On the bananapi get the kernel sources (you can probably get them on the PC too but I didn't have a URL for sunxi kernels):

    sudo apt install linux-source-4.19.13-next-sunxi
    
which places a .tar.xz into /usr/src. Copy that over to the PC.

Extract the kernel sources into a directory of your choice (on the PC) - I'll refer to it as $BUILD_DIR

    cd $BUILD_DIR && mkdir linux-src && tar -xJvf ~/Download/linux-source-4.19.13-sunxi.tar.xz
    cd $BUILD_DIR
    git clone https://github.com/mripard/sunxi-mali.git
    cd sunxi-mali
    export CROSS_COMPILE=arm-linux-gnueabihf-
    export KDIR=$BUILD_DIR/linux-src
    ./build.sh -r r6p2 -b
    
That should create `./r6p2/src/devicedrv/mali/mali.ko` for you. Copy `mali.ko` over to the Banana-Pi.

On the Banana-Pi I placed the mali-module `mali.ko` into `/lib/modules/4.19.13-sunxi/kernel/drivers/gpu/drm/mali/` and added a line to `/etc/modules` after which it looked like:

    $ cat /etc/modules
    brcmfmac
    bonding
    mali

In case you have a `lima` driver you should disable it, it conflicts with the mali driver.
Run

    depmod
    
and reboot.

Check that it loaded the mali driver:

    $ lsmod | grep mali
    mali                  188416  0
    
or

    $ dmesg
    [..]
    [    6.655758] mali: loading out-of-tree module taints kernel.
    [    6.672175] Allwinner sunXi mali glue initialized
    [    6.672992] Mali: 
    [    6.673005] Found Mali GPU Mali-400 MP r1p1
    [    6.676886] Mali: 
    [    6.676899] 2+0 PP cores initialized
    [    6.678085] Mali: 
    [    6.678095] Mali device driver loaded
    
Copy the binary drivers:

    git clone https://github.com/bootlin/mali-blobs.git
    cd mali-blobs
    cp -d r6p2/arm/x11_dma_buf/* /usr/lib/arm-linux-gnueabihf
