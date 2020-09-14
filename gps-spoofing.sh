while getopts c:t:l: flag
do
    case "${flag}" in
        c) clksrc=${OPTARG};;
        t) time=${OPTARG};;
        l) loc=${OPTARG};;
    esac
done

echo clksrc = $clksrc
echo time = $time
echo loc = $loc

# Download and uncompress BRDC file
wget -4 ftp://cddis.gsfc.nasa.gov/gnss/data/daily/$(date -u +%Y)/brdc/brdc$(date -u +%j0.%g)n.Z
uncompress brdc$(date -u +%j0.%g)n.Z

# Generate GPS bitstream
if [ -z $loc]; then
    loc="21.28,-157.81,100"
    echo Default location = $loc
fi
if [ -z $time ]; then
    time="$(date -u +%Y/%m/%d,+%X)"
    echo Default time = $time
fi

./gps-sdr-sim -e brdc$(date -u +%j0.%g)n -l $loc -d 60 -b 16 -o gpssim.bin -t $time
#./gps-sdr-sim -e brdc$(date -u +%j0.%g)n -l 21.28,-157.81,100 -d 60 -b 16 -o gpssim.bin -t $(date -u +%Y/%m/%d,+%X)

# Send GPS bitstream
if [ -z $clksrc ]; then 
  bladeRF-cli -s bladerf2.0.script
else
  if [ $clksrc = "ext" ]; then
    echo Use external clock reference
    bladeRF-cli -s bladerf-extclk-2.0.script
  else
    bladeRF-cli -s bladerf2.0.script
  fi
fi

