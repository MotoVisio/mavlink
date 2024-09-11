#!/usr/bin/env bash



# Build C library
GEN_START_PATH=$PWD
mkdir -p include/mavlink/v2.0
cd include/mavlink/v2.0
git clone git@github.com:MotoVisio/c_library_v2.git
cd ../../..
./scripts/update_c_library.sh 2
## v1.0 legacy
#cd "$GEN_START_PATH"
#mkdir -p include/mavlink/v1.0
#cd include/mavlink/v1.0
#git clone https://github.com/mavlink/c_library_v1.git
#cd ../../..
#./scripts/update_c_library.sh 1
