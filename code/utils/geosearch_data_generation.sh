source ../../gestalt_env/bin/activate

### UNMODIFIED QUERIES - EXPECT 100% RECALL ###

# Batch of experiments with 4 Query Terms
python dataGenerator.py --experimentName obj10_que4 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 8 --scaleFactor 2 --edgeFactor 2 --numQueryDistortions 0 --numQueryTerms 4
python dataGenerator.py --experimentName obj100_que4 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 8 --scaleFactor 5 --edgeFactor 2 --numQueryDistortions 0 --numQueryTerms 4
python dataGenerator.py --experimentName obj1000_que4 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 8 --scaleFactor 7 --edgeFactor 4 --numQueryDistortions 0 --numQueryTerms 4
python dataGenerator.py --experimentName obj10000_que4 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 8 --scaleFactor 10 --edgeFactor 5 --numQueryDistortions 0 --numQueryTerms 4
python dataGenerator.py --experimentName obj100000_que4 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 8 --scaleFactor 13 --edgeFactor 7 --numQueryDistortions 0 --numQueryTerms 4
python dataGenerator.py --experimentName obj1000000_que4 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 8 --scaleFactor 16 --edgeFactor 8 --numQueryDistortions 0 --numQueryTerms 4

#With 10 Query Terms
python dataGenerator.py --experimentName obj10_que10 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 8 --scaleFactor 2 --edgeFactor 2 --numQueryDistortions 0 --numQueryTerms 10
python dataGenerator.py --experimentName obj100_que10 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 8 --scaleFactor 5 --edgeFactor 2 --numQueryDistortions 0 --numQueryTerms 10
python dataGenerator.py --experimentName obj1000_que10 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 8 --scaleFactor 7 --edgeFactor 4 --numQueryDistortions 0 --numQueryTerms 10
python dataGenerator.py --experimentName obj10000_que10 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 8 --scaleFactor 10 --edgeFactor 5 --numQueryDistortions 0 --numQueryTerms 10
python dataGenerator.py --experimentName obj100000_que10 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 8 --scaleFactor 13 --edgeFactor 7 --numQueryDistortions 0 --numQueryTerms 10
python dataGenerator.py --experimentName obj1000000_que10 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 8 --scaleFactor 16 --edgeFactor 8 --numQueryDistortions 0 --numQueryTerms 10

#With 100 Query Terms
python dataGenerator.py --experimentName obj10_que100 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 2 --edgeFactor 2 --numQueryDistortions 0 --numQueryTerms 100
python dataGenerator.py --experimentName obj100_que100 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 5 --edgeFactor 2 --numQueryDistortions 0 --numQueryTerms 100
python dataGenerator.py --experimentName obj1000_que100 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 7 --edgeFactor 4 --numQueryDistortions 0 --numQueryTerms 100
python dataGenerator.py --experimentName obj10000_que100 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 10 --edgeFactor 5 --numQueryDistortions 0 --numQueryTerms 100
python dataGenerator.py --experimentName obj100000_que100 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 13 --edgeFactor 7 --numQueryDistortions 0 --numQueryTerms 100
python dataGenerator.py --experimentName obj1000000_que100 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 16 --edgeFactor 8 --numQueryDistortions 0 --numQueryTerms 100

#With 1,000 Query Terms
python dataGenerator.py --experimentName obj10_que1000 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 2 --edgeFactor 2 --numQueryDistortions 0 --numQueryTerms 1000
python dataGenerator.py --experimentName obj100_que1000 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 5 --edgeFactor 2 --numQueryDistortions 0 --numQueryTerms 1000
python dataGenerator.py --experimentName obj1000_que1000 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 7 --edgeFactor 4 --numQueryDistortions 0 --numQueryTerms 1000
python dataGenerator.py --experimentName obj10000_que1000 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 10 --edgeFactor 5 --numQueryDistortions 0 --numQueryTerms 1000
python dataGenerator.py --experimentName obj100000_que1000 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 13 --edgeFactor 7 --numQueryDistortions 0 --numQueryTerms 1000
python dataGenerator.py --experimentName obj1000000_que1000 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 16 --edgeFactor 8 --numQueryDistortions 0 --numQueryTerms 1000

#With 10,000 Query Terms
python dataGenerator.py --experimentName obj10_que10000 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 2 --edgeFactor 2 --numQueryDistortions 0 --numQueryTerms 10000
python dataGenerator.py --experimentName obj100_que10000 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 5 --edgeFactor 2 --numQueryDistortions 0 --numQueryTerms 10000
python dataGenerator.py --experimentName obj1000_que10000 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 7 --edgeFactor 4 --numQueryDistortions 0 --numQueryTerms 10000
python dataGenerator.py --experimentName obj10000_que10000 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 10 --edgeFactor 5 --numQueryDistortions 0 --numQueryTerms 10000
python dataGenerator.py --experimentName obj100000_que10000 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 13 --edgeFactor 7 --numQueryDistortions 0 --numQueryTerms 10000
python dataGenerator.py --experimentName obj1000000_que10000 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 16 --edgeFactor 8 --numQueryDistortions 0 --numQueryTerms 10000

### DISTORTED LOCATIONS - EXPECT < 100% RECALL ###

# Batch of experiments with 4 Query Terms
python dataGenerator.py --experimentName dist_obj10_que4 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 8 --scaleFactor 2 --edgeFactor 2 --numQueryDistortions 2 --numQueryTerms 4
python dataGenerator.py --experimentName dist_obj100_que4 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 8 --scaleFactor 5 --edgeFactor 2 --numQueryDistortions 2 --numQueryTerms 4
python dataGenerator.py --experimentName dist_obj1000_que4 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 8 --scaleFactor 7 --edgeFactor 4 --numQueryDistortions 2 --numQueryTerms 4
python dataGenerator.py --experimentName dist_obj10000_que4 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 8 --scaleFactor 10 --edgeFactor 5 --numQueryDistortions 2 --numQueryTerms 4
python dataGenerator.py --experimentName dist_obj100000_que4 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 8 --scaleFactor 13 --edgeFactor 7 --numQueryDistortions 2 --numQueryTerms 4
python dataGenerator.py --experimentName dist_obj1000000_que4 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 8 --scaleFactor 16 --edgeFactor 8 --numQueryDistortions 2 --numQueryTerms 4

#With 10 Query Terms
python dataGenerator.py --experimentName dist_obj10_que10 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 8 --scaleFactor 2 --edgeFactor 2 --numQueryDistortions 2 --numQueryTerms 10
python dataGenerator.py --experimentName dist_obj100_que10 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 8 --scaleFactor 5 --edgeFactor 2 --numQueryDistortions 2 --numQueryTerms 10
python dataGenerator.py --experimentName dist_obj1000_que10 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 8 --scaleFactor 7 --edgeFactor 4 --numQueryDistortions 2 --numQueryTerms 10
python dataGenerator.py --experimentName dist_obj10000_que10 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 8 --scaleFactor 10 --edgeFactor 5 --numQueryDistortions 2 --numQueryTerms 10
python dataGenerator.py --experimentName dist_obj100000_que10 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 8 --scaleFactor 13 --edgeFactor 7 --numQueryDistortions 2 --numQueryTerms 10
python dataGenerator.py --experimentName dist_obj1000000_que10 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 8 --scaleFactor 16 --edgeFactor 8 --numQueryDistortions 2 --numQueryTerms 10

#With 100 Query Terms
python dataGenerator.py --experimentName dist_obj10_que100 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 2 --edgeFactor 2 --numQueryDistortions 2 --numQueryTerms 100
python dataGenerator.py --experimentName dist_obj100_que100 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 5 --edgeFactor 2 --numQueryDistortions 2 --numQueryTerms 100
python dataGenerator.py --experimentName dist_obj1000_que100 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 7 --edgeFactor 4 --numQueryDistortions 2 --numQueryTerms 100
python dataGenerator.py --experimentName dist_obj10000_que100 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 10 --edgeFactor 5 --numQueryDistortions 2 --numQueryTerms 100
python dataGenerator.py --experimentName dist_obj100000_que100 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 13 --edgeFactor 7 --numQueryDistortions 2 --numQueryTerms 100
python dataGenerator.py --experimentName dist_obj1000000_que100 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 16 --edgeFactor 8 --numQueryDistortions 2 --numQueryTerms 100

#With 1,000 Query Terms
python dataGenerator.py --experimentName dist_obj10_que1000 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 2 --edgeFactor 2 --numQueryDistortions 2 --numQueryTerms 1000
python dataGenerator.py --experimentName dist_obj100_que1000 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 5 --edgeFactor 2 --numQueryDistortions 2 --numQueryTerms 1000
python dataGenerator.py --experimentName dist_obj1000_que1000 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 7 --edgeFactor 4 --numQueryDistortions 2 --numQueryTerms 1000
python dataGenerator.py --experimentName dist_obj10000_que1000 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 10 --edgeFactor 5 --numQueryDistortions 2 --numQueryTerms 1000
python dataGenerator.py --experimentName dist_obj100000_que1000 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 13 --edgeFactor 7 --numQueryDistortions 2 --numQueryTerms 1000
python dataGenerator.py --experimentName dist_obj1000000_que1000 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 16 --edgeFactor 8 --numQueryDistortions 2 --numQueryTerms 1000

#With 10,000 Query Terms
python dataGenerator.py --experimentName dist_obj10_que10000 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 2 --edgeFactor 2 --numQueryDistortions 2 --numQueryTerms 10000
python dataGenerator.py --experimentName dist_obj100_que10000 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 5 --edgeFactor 2 --numQueryDistortions 2 --numQueryTerms 10000
python dataGenerator.py --experimentName dist_obj1000_que10000 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 7 --edgeFactor 4 --numQueryDistortions 2 --numQueryTerms 10000
python dataGenerator.py --experimentName dist_obj10000_que10000 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 10 --edgeFactor 5 --numQueryDistortions 2 --numQueryTerms 10000
python dataGenerator.py --experimentName dist_obj100000_que10000 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 13 --edgeFactor 7 --numQueryDistortions 2 --numQueryTerms 10000
python dataGenerator.py --experimentName dist_obj1000000_que10000 --randomSeed 3 --queryRatio 0.5 --numLocations 10 --numClasses 52 --scaleFactor 16 --edgeFactor 8 --numQueryDistortions 2 --numQueryTerms 10000

