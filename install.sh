#/bin/sh
# do NOT use this script from Kodi addons directory, it is intented for development only
DESTDIR=~/kodi/${addons}

rm -rf ${DESTDIR}
mkdir -p ${DESTDIR}
cp -a * ${DESTDIR}
