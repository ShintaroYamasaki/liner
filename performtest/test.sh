#!/bin/bash

if [ "$1" = "" -o "$2" = "" -o "$3" = "" ]; then
  echo "Please set number, interval, and number of connectors"
  exit
fi

NUM=$1
INTERVAL_DS=$2
INTERVAL_LC=$2
CONNECTORS=$3

START_TIME=`date +%s`
RESULT_DIR="result_"$1"_"$2"_"$3"_"$START_TIME

mkdir $RESULT_DIR

## Data set
echo "Preparing data set..."
APP_IDS_FILE=$RESULT_DIR"/appids.txt"
#python dataset.py $NUM $MODE > $APP_IDS_FILE
python dataset.py $NUM $CONNECTORS > $APP_IDS_FILE
echo "Done"
echo ""


## Interval set
echo "Setting interval"
python changeinterval.py $INTERVAL_DS $INTERVAL_LC
echo "Done"
echo ""

## Profile
DIRNAME=`pwd`
PROFILE_SCRIPT="profile_perform.sh"
RUN_TIME=60
RUN_TIME_P=70
MAIN_CMD="python main.py"
MONGO_CMD="mongodb.conf"

LOG_USAGE_MAIN=$RESULT_DIR"/usage_main.log"
LOG_USAGE_DB=$RESULT_DIR"/usage_mongo.log"

echo "Running main and profiling..."
# Run profiling for main
timeout $RUN_TIME_P bash $PROFILE_SCRIPT $MAIN_CMD > $LOG_USAGE_MAIN &
# Run profiling for mongodb
timeout $RUN_TIME_P bash $PROFILE_SCRIPT $MONGO_CMD > $LOG_USAGE_DB & 
sleep 5
cd ..
LOG_MAIN=$DIRNAME"/"$RESULT_DIR"/main.log"
echo -n "" > $LOG_MAIN
# Run main script
timeout $RUN_TIME $MAIN_CMD 2>&1 | tee $LOG_MAIN &
cd $DIRNAME


sleep 25


# Change values
#######
echo $CONNECTORD
if [ "$CONNECTORS" != "" -a "$CONNECTORS" != "0" ]; then
  DATA_CHANGE_LOG=$RESULT_DIR"/data_change.log"
  head -n $(($CONNECTORS * 2)) $APP_IDS_FILE | awk 'NR%2==1' | while read appid
  do
    change_time=`date +%s%N`
    echo -n 1 > ../nodes/testapp/io/${appid}.io
    echo ${change_time:0:10}"."${change_time:10}","$appid >> $DATA_CHANGE_LOG
    sleep 0.5
  done &
fi
#######


sleep $(($RUN_TIME - 25))
sleep 5

echo "Done"
echo ""

echo "Collecting and Calculating datastores..."


cat $APP_IDS_FILE | while read appid
do
  DATASTORE_FILE_DB=$RESULT_DIR/datastore_${appid}_db.log
  DATASTORE_FILE_APP=$RESULT_DIR/datastore_${appid}_app.log

  python datacollect.py $appid > $DATASTORE_FILE_DB
  mv ../nodes/testapp/logs/${appid}.log $DATASTORE_FILE_APP

  rm ../nodes/testapp/io/${appid}.io
done

echo ""
echo "Done"

exit
