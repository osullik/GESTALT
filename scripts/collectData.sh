#collectData.sh

#shell script to automate the collection of data from OSM; assumes it is being run from the GESTALT/scripts directory

#Variables (update these to change the python script that runs)

BB_LL="-31.90009882641578"
BB_LR="115.96168231510637"
BB_TL="-31.77307863942101" 
BB_TR="116.05029961853784"
SEARCHTERM="winery"
OUTPUTFILE="../data/osm.json"


#Activate the venv
source ../gestalt_env/bin/activate

python3 ../code/gestalt.py -q -b $BB_LL $BB_LR $BB_TL $BB_TR -s $SEARCHTERM -o $OUTPUTFILE
#python3 ../code/gestalt.py -q -b -31.90009882641578 115.96168231510637 -31.77307863942101 116.05029961853784 -s winery -o ../data/osm.json