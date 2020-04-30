mkdir -p mahimahi_0.98-1/DEBIAN
./autogen.sh && ./configure --prefix=$(pwd)/mahimahi_0.98-1/usr/local && make -j4 && sudo make install
cp control mahimahi_0.98-1/DEBIAN/
dpkg-deb --build mahimahi_0.98-1

# Install the deb packet with following two commands
# sudo apt --fix-broken install libc6 libcairo2 libgcc1 libglib2.0-0 libpango-1.0-0 libpangocairo-1.0-0 \
#   libprotobuf10 libssl1.1 libstdc++6 libxcb-present0 libxcb1 iptables dnsmasq-base apache2-bin gnuplot \
#   iproute2 apache2-api-20120211
# sudo dpkg -i 