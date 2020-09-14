wget -4 ftp://cddis.gsfc.nasa.gov/gnss/data/daily/$(date -u +%Y)/brdc/brdc$(date -u +%j0.%g)n.Z
uncompress brdc$(date -u +%j0.%g)n.Z
./gps-sdr-sim -e brdc$(date -u +%j0.%g)n -l 21.28,-157.81,100 -d 60 -b 16 -o gpssim.bin -t $(date -u +%Y/%m/%d,+%X)
bladeRF-cli -s bladerf2.0.script
