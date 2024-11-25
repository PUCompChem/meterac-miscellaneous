'''
A simple console app for calculation of cross sensitivity
'''

import sys
from cross_sensitivity import *

class CLIOption:
    def __init__(self, shortName: str, longName: str, booleanOpt : bool):
        self.shortName = shortName
        self.longName = longName
        self.booleanOpt = booleanOpt

    def checkOption(self, arg: str) -> bool:
       #Checking whether the argument is an CLI option:
       # -o  or --option (returns true)
       if arg.startswith("--"):
           #checking long names
           opt = arg[2:]
           if (opt == self.longName):
               return True
       elif arg.startswith("-"):
           #checking short names
           opt = arg[1:]
           if (opt == self.shortName):
               return True
       return False


def extract_arguments(args: list[str], options: list[CLIOption]) -> dict[str, object]:
    arg_dict = {}
    n = len(args)
    arg_dict["app_name"] = args[0]
    main_arguments = []
    boolean_options = []
    standard_options = {}
    #Iterated all arguments and find options
    if n > 1:
        i = 1
        while i < n:
            print(args[i])
            opt_flag = False
            if options:
                for opt in options:
                    if opt.checkOption(args[i]):
                        opt_flag = True
                        if opt.booleanOpt:
                            boolean_options.append(opt.longName)
                        else:
                            i+=1 #iterated to next argument to get option value
                            if i < n:
                                standard_options[opt.longName] = args[i]
                            else:
                                standard_options[opt.longName] = None
            if not opt_flag:
                main_arguments.append(args[i])
            i+=1

    arg_dict["main_arguments"] = main_arguments
    arg_dict["boolean_options"] = boolean_options
    arg_dict["standard_options"] = standard_options
    return arg_dict

options = [CLIOption("f","file", False)]

arguments = extract_arguments(sys.argv, options)
print(arguments)
