'''
A simple console app for calculation of cross sensitivity
'''

import sys
from cross_sensitivity import *


def extract_arguments(args: list[str]) -> dict[str, object]:
    arg_dict = {}
    n = len(args)
    arg_dict["app_name"] = args[0]
    main_arguments = []
    if n > 1:
        for i in range(1,n):
            print(args[i])
            #TODO
    arg_dict["main_arguments"] = main_arguments
    return arg_dict


arguments = extract_arguments(sys.argv)
print(arguments)
