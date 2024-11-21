'''
A simple console app for calculation of cross sensitivity
'''

import sys
from cross_sensitivity import *


def parse_arguments(args: list[str]) -> dict[str, object]:
    arg_dict = {}
    n = len(args)
    for i in range(n):
        print(args[i])
        #TODO
    return arg_dict


arguments = parse_arguments(sys.argv)
