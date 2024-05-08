
from calcgasindex import *

# Some Testing
params =  GasIndexAlgorithmParams()
#GasIndexAlgorithm_reset(params)
GasIndexAlgorithm_init_with_sampling_interval(params, 0, 300)
#GasIndexAlgorithm_init(params, 0)

print(params.__dict__)


