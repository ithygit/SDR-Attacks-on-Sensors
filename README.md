# SDR-Attacks-on-Sensors

For more information, see the [SDR Attacks on Sensors wiki](https://github.com/jianqiucao/SDR-Attacks-on-Sensors/wiki)


The following file included in the repo are needed for the GPS Spoofing experiment (See the Wiki).

* gps-spoofing.sh: A one-click script for downloading BRDC file, generating bitstream and sending it through bladeRF.  

* gps-sdr-sim.exe: Windows 64-bit executable for generating GPS bitstream (from [GPS-SDR-SIM releases](https://github.com/osqzss/gps-sdr-sim/releases))
  * For Linux executables, complile from the source code [gps-sdr-sim](https://github.com/osqzss/gps-sdr-sim).
* bladerf.script: transmission script for bladeRF-cli with BladeRF v1.0
* bladerf2.0.script: transmission script for bladeRF-cli with BladeRF v2.0
* brdc2830.19n: GPS broadcast ephemeris file (BRDC) on Oct. 10, 2019 (from ftp://cddis.gsfc.nasa.gov/gnss/data/daily/)  

* SatGenNMEA.exe: SatGen Trajectory generation executable for generating NMEA file (from [SatGen Trajectory generation](https://www.labsat.co.uk/index.php/en/free-gps-nmea-simulator-software))
* holmes_hall.kml: route around Holmes Hall created by Google maps
* holmes20.txt: NMEA file of maximum speed at 20km/s
* holmes100.txt: NMEA file of maximum speed at 100km/s
* SatGen_commands2.txt: SatGenNMEA user command for making spoofing trajectory.
