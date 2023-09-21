#Runs the experiments used to create the data for the geoseach workshop
source ../../gestalt_env/bin/activate

# Batch of experiments with 4 Query Terms
python exp_compass.py --experimentName obj10_que4
python exp_compass.py --experimentName obj100_que4
python exp_compass.py --experimentName obj1000_que4
python exp_compass.py --experimentName obj10000_que4
#python exp_compass.py --experimentName obj100000_que4
#python exp_compass.py --experimentName obj1000000_que4

# Batch of experiments with 10 Query Terms
python exp_compass.py --experimentName obj10_que10
python exp_compass.py --experimentName obj100_que10
python exp_compass.py --experimentName obj1000_que10
python exp_compass.py --experimentName obj10000_que10
#python exp_compass.py --experimentName obj100000_que10
#python exp_compass.py --experimentName obj1000000_que10

# Batch of experiments with 100 Query Terms
python exp_compass.py --experimentName obj10_que100
python exp_compass.py --experimentName obj100_que100
python exp_compass.py --experimentName obj1000_que100
python exp_compass.py --experimentName obj10000_que100
#python exp_compass.py --experimentName obj100000_que100
#python exp_compass.py --experimentName obj1000000_que100

# Batch of experiments with 1000 Query Terms
python exp_compass.py --experimentName obj10_que1000
python exp_compass.py --experimentName obj100_que1000
python exp_compass.py --experimentName obj1000_que1000
python exp_compass.py --experimentName obj10000_que1000
#python exp_compass.py --experimentName obj100000_que1000
#python exp_compass.py --experimentName obj1000000_que1000

# Batch of experiments with 10000 Query Terms
python exp_compass.py --experimentName obj10_que10000
python exp_compass.py --experimentName obj100_que10000
python exp_compass.py --experimentName obj1000_que10000
python exp_compass.py --experimentName obj10000_que10000
#python exp_compass.py --experimentName obj100000_que10000
#python exp_compass.py --experimentName obj1000000_que10000

#
# CARDINALITY INVARIANT QUERIES
#

# Batch of experiments with 10 Query Terms
python exp_compass.py --experimentName obj10_que10 --cardinalityInvariant
python exp_compass.py --experimentName obj100_que10 --cardinalityInvariant
python exp_compass.py --experimentName obj1000_que10 --cardinalityInvariant
python exp_compass.py --experimentName obj10000_que10 --cardinalityInvariant
#python exp_compass.py --experimentName obj100000_que10 --cardinalityInvariant
#python exp_compass.py --experimentName obj1000000_que10 --cardinalityInvariant

# Batch of experiments with 100 Query Terms
python exp_compass.py --experimentName obj10_que100 --cardinalityInvariant
python exp_compass.py --experimentName obj100_que100 --cardinalityInvariant
python exp_compass.py --experimentName obj1000_que100 --cardinalityInvariant
python exp_compass.py --experimentName obj10000_que100 --cardinalityInvariant
#python exp_compass.py --experimentName obj100000_que100 --cardinalityInvariant
#python exp_compass.py --experimentName obj1000000_que100 --cardinalityInvariant

# Batch of experiments with 1000 Query Terms
python exp_compass.py --experimentName obj10_que1000 --cardinalityInvariant
python exp_compass.py --experimentName obj100_que1000 --cardinalityInvariant
python exp_compass.py --experimentName obj1000_que1000 --cardinalityInvariant
python exp_compass.py --experimentName obj10000_que1000 --cardinalityInvariant
#python exp_compass.py --experimentName obj100000_que1000 --cardinalityInvariant
#python exp_compass.py --experimentName obj1000000_que1000 --cardinalityInvariant

# Batch of experiments with 10000 Query Terms
python exp_compass.py --experimentName obj10_que10000 --cardinalityInvariant
python exp_compass.py --experimentName obj100_que10000 --cardinalityInvariant
python exp_compass.py --experimentName obj1000_que10000 --cardinalityInvariant
python exp_compass.py --experimentName obj10000_que10000 --cardinalityInvariant
#python exp_compass.py --experimentName obj100000_que10000 --cardinalityInvariant
#python exp_compass.py --experimentName obj1000000_que10000 --cardinalityInvariant


#### WITH distorted locations ###

# Batch of experiments with 4 Query Terms
python exp_compass.py --experimentName dist_obj10_que4
python exp_compass.py --experimentName dist_obj100_que4
python exp_compass.py --experimentName dist_obj1000_que4
python exp_compass.py --experimentName dist_obj10000_que4
#python exp_compass.py --experimentName dist_obj100000_que4
#python exp_compass.py --experimentName dist_obj1000000_que4

# Batch of experiments with 10 Query Terms
python exp_compass.py --experimentName dist_obj10_que10
python exp_compass.py --experimentName dist_obj100_que10
python exp_compass.py --experimentName dist_obj1000_que10
python exp_compass.py --experimentName dist_obj10000_que10
#python exp_compass.py --experimentName dist_obj100000_que10
#python exp_compass.py --experimentName dist_obj1000000_que10

# Batch of experiments with 100 Query Terms
python exp_compass.py --experimentName dist_obj10_que100
python exp_compass.py --experimentName dist_obj100_que100
python exp_compass.py --experimentName dist_obj1000_que100
python exp_compass.py --experimentName dist_obj10000_que100
#python exp_compass.py --experimentName dist_obj100000_que100
#python exp_compass.py --experimentName dist_obj1000000_que100

# Batch of experiments with 1000 Query Terms
python exp_compass.py --experimentName dist_obj10_que1000
python exp_compass.py --experimentName dist_obj100_que1000
python exp_compass.py --experimentName dist_obj1000_que1000
python exp_compass.py --experimentName dist_obj10000_que1000
#python exp_compass.py --experimentName dist_obj100000_que1000
#python exp_compass.py --experimentName dist_obj1000000_que1000

# Batch of experiments with 10000 Query Terms
python exp_compass.py --experimentName obj10_que10000
python exp_compass.py --experimentName obj100_que10000
python exp_compass.py --experimentName obj1000_que10000
python exp_compass.py --experimentName obj10000_que10000
#python exp_compass.py --experimentName obj100000_que10000
#python exp_compass.py --experimentName obj1000000_que10000

#
# CARDINALITY INVARIANT QUERIES
#

# Batch of experiments with 10 Query Terms
python exp_compass.py --experimentName dist_obj10_que10 --cardinalityInvariant
python exp_compass.py --experimentName dist_obj100_que10 --cardinalityInvariant
python exp_compass.py --experimentName dist_obj1000_que10 --cardinalityInvariant
python exp_compass.py --experimentName dist_obj10000_que10 --cardinalityInvariant
#python exp_compass.py --experimentName dist_obj100000_que10 --cardinalityInvariant
#python exp_compass.py --experimentName dist_obj1000000_que10 --cardinalityInvariant

# Batch of experiments with 100 Query Terms
python exp_compass.py --experimentName dist_obj10_que100 --cardinalityInvariant
python exp_compass.py --experimentName dist_obj100_que100 --cardinalityInvariant
python exp_compass.py --experimentName dist_obj1000_que100 --cardinalityInvariant
python exp_compass.py --experimentName dist_obj10000_que100 --cardinalityInvariant
#python exp_compass.py --experimentName dist_obj100000_que100 --cardinalityInvariant
#python exp_compass.py --experimentName dist_obj1000000_que100 --cardinalityInvariant

# Batch of experiments with 1000 Query Terms
python exp_compass.py --experimentName dist_obj10_que1000 --cardinalityInvariant
python exp_compass.py --experimentName dist_obj100_que1000 --cardinalityInvariant
python exp_compass.py --experimentName dist_obj1000_que1000 --cardinalityInvariant
python exp_compass.py --experimentName dist_obj10000_que1000 --cardinalityInvariant
#python exp_compass.py --experimentName dist_obj100000_que1000 --cardinalityInvariant
#python exp_compass.py --experimentName dist_obj1000000_que1000 --cardinalityInvariant

# Batch of experiments with 10000 Query Terms
python exp_compass.py --experimentName dist_obj10_que10000 --cardinalityInvariant
python exp_compass.py --experimentName dist_obj100_que10000 --cardinalityInvariant
python exp_compass.py --experimentName dist_obj1000_que10000 --cardinalityInvariant
python exp_compass.py --experimentName dist_obj10000_que10000 --cardinalityInvariant
#python exp_compass.py --experimentName dist_obj100000_que10000 --cardinalityInvariant
#python exp_compass.py --experimentName dist_obj1000000_que10000 --cardinalityInvariant


### 100 k size experiments 
python exp_compass.py --experimentName obj100000_que4
python exp_compass.py --experimentName obj100000_que10
python exp_compass.py --experimentName obj100000_que100
python exp_compass.py --experimentName obj100000_que1000
python exp_compass.py --experimentName obj100000_que10000
python exp_compass.py --experimentName obj100000_que10 --cardinalityInvariant
python exp_compass.py --experimentName obj100000_que100 --cardinalityInvariant
python exp_compass.py --experimentName obj100000_que1000 --cardinalityInvariant
python exp_compass.py --experimentName obj100000_que10000 --cardinalityInvariant
python exp_compass.py --experimentName dist_obj100000_que4
python exp_compass.py --experimentName dist_obj100000_que10
python exp_compass.py --experimentName dist_obj100000_que100
python exp_compass.py --experimentName dist_obj100000_que1000
python exp_compass.py --experimentName dist_obj100000_que10 --cardinalityInvariant
python exp_compass.py --experimentName dist_obj100000_que100 --cardinalityInvariant
python exp_compass.py --experimentName dist_obj100000_que1000 --cardinalityInvariant
python exp_compass.py --experimentName dist_obj100000_que10000 --cardinalityInvariant


### 1M size experiments
python exp_compass.py --experimentName obj1000000_que4
python exp_compass.py --experimentName obj1000000_que10
python exp_compass.py --experimentName obj1000000_que100
python exp_compass.py --experimentName obj1000000_que1000
python exp_compass.py --experimentName obj1000000_que10000
python exp_compass.py --experimentName obj1000000_que10 --cardinalityInvariant
python exp_compass.py --experimentName obj1000000_que100 --cardinalityInvariant
python exp_compass.py --experimentName obj1000000_que1000 --cardinalityInvariant
python exp_compass.py --experimentName obj1000000_que10000 --cardinalityInvariant
python exp_compass.py --experimentName dist_obj1000000_que4
python exp_compass.py --experimentName dist_obj1000000_que10
python exp_compass.py --experimentName dist_obj1000000_que100
python exp_compass.py --experimentName dist_obj1000000_que1000
python exp_compass.py --experimentName dist_obj1000000_que10 --cardinalityInvariant
python exp_compass.py --experimentName dist_obj1000000_que100 --cardinalityInvariant
python exp_compass.py --experimentName dist_obj1000000_que1000 --cardinalityInvariant
python exp_compass.py --experimentName dist_obj1000000_que10000 --cardinalityInvariant
