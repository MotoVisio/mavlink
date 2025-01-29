#!/bin/bash

#TODO fix this so that we have our own c_library_v2.0 that we update with the update_c_library.sh
if [[ $# -eq 1 &&  $(basename $1) -eq "qgroundcontrol" ]]; then
  QGC_DIR=$( readlink -f $1 )
  QGC_CLIBRARY_DIR=${QGC_DIR}/libs/mavlink/include/mavlink/v2.0
  else
    echo "[ERROR] ./scripts/update_qgc.sh <path-to-qgroundcontrol>"
    exit 1
fi


OUTPUT_DIR="tmp"
if [[ -e ${OUTPUT_DIR} ]]; then
  rm -r ${OUTPUT_DIR}
fi


function generate_headers() {
python pymavlink/tools/mavgen.py \
    --output ${OUTPUT_DIR} \
    --lang C \
    --wire-protocol 2.0 \
    message_definitions/v1.0/$1.xml
}

echo -e "\0033[34mStarting to generate c headers\0033[0m\n"
generate_headers development
generate_headers ardupilotmega
generate_headers matrixpilot
generate_headers test
generate_headers ASLUAV
generate_headers standard

echo -e "\0033[34mupdateing${QGC_CLIBRARY_DIR}\0033[0m\n"
mkdir -p ${OUTPUT_DIR}/message_definitions
cp message_definitions/v1.0/* $OUTPUT_DIR/message_definitions/.
cp -R ${OUTPUT_DIR}/* ${QGC_CLIBRARY_DIR}/
rm -r ${OUTPUT_DIR}

echo -e "\0033[34mFinished generating c headers\0033[0m\n"