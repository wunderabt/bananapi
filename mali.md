# Mali Graphics on Banana-Pi M1 with All-Winner A20 chip

Basic instructions taken from https://bootlin.com/blog/mali-opengl-support-on-allwinner-platforms-with-mainline-linux/

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
