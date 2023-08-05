#!/bin/bash

src_dir=`pwd`

export arm=arm-linux-gnueabihf-
export arm64=aarch64-linux-gnu-

export arch=$1
export CC=${!arch}gcc
export CXX=${!arch}g++
export LD=${!arch}ld
export STRIP=${!arch}strip

if [ "$arch" == "arm" ]; then
    export arch_name=armv7l
fi
if [ "$arch" == "arm64" ]; then
    export arch_name=aarch64
    # rename package name to *_aarch64
    #export plat_name=any
    #sed -i -E "s/name='(.*)'/name='\1_aarch64'/" setup.py
fi
curl -s https://api.github.com/repos/panda-official/TimeSwipe/releases/latest | grep "browser_download_url.*timeswipe.*$arch_name.deb" | cut -d : -f 2,3 | tr -d \"  | wget -qi -
dpkg -i *.deb && rm *.deb || exit -1
if [ "$arch" == "src" ]; then
python3.8 setup.py sdist --dist-dir /tmp/dist && python3.8 setup.py clean --all && find /tmp/dist -iname "*.tar.gz" -exec cp {} ${src_dir} \;
else
OVERRIDE_INCLUDES=/usr/include/aarch64-linux-gnu/python3.8\ /usr/include/python3.8 OVERRIDE_LIBS=/usr/lib/libtimeswipe.a\ /usr/lib/libboost_python38.a python3.8 setup.py bdist_wheel --plat-name linux_$arch_name --dist-dir /tmp/dist && python3.8 setup.py clean --all || exit -1
OVERRIDE_INCLUDES=/usr/include/aarch64-linux-gnu/python3.7\ /usr/include/python3.7 OVERRIDE_LIBS=/usr/lib/libtimeswipe.a\ /usr/lib/libboost_python37.a python3.7 setup.py bdist_wheel --plat-name linux_$arch_name --dist-dir /tmp/dist && python3.7 setup.py clean --all || exit -1
find /tmp/dist -iname "*.whl" -exec cp {} ${src_dir} \;
fi
dpkg -r timeswipe

