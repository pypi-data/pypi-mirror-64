"""
cli.py - command line interface for simple-plotter

Copyright (c) 2020 Thies Hecker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from simple_plotter.core.code_generator import DataHandler, Formula, PlotData
from simple_plotter.core.code_parser import CodeChecker
import sys

usage_info = """
usage:
simple-plotter [options] -i <input-file>

Options:
----------
--input, -i:     Input file name (JSON file with simple-plotter project data)
--plotlib, -p:   library used for plotting - either 'matplotlib' (default) or 'kivy-garden/graph'
--output, -o:    export code to python file - followed by file name
--no-check, -n:  Do not run the code checker
--help:          Show this help

For further information visit the documentation at 
https://simple-plotter.readthedocs.io/en/latest/
"""


def setup_code_checker():
    """CodeChecker: Sets up the code checker"""

    # code checker setup
    allowed_imports = ['numpy', 'matplotlib.pyplot', 'csv', 'simple_plotter.core.advanced_graph']
    allowed_calls = ['f', 'str', 'Graph', 'MeshLinePlot', 'range', 'len', 'append', 'min', 'max', 'int', 'check_value',
                     'enumerate', 'float', 'AnnotatedLinePlot']
    allowed_FunctionDefs = ['f', 'check_value']
    allowed_aliases = ['np', 'plt', 'points', 'graph', 'x_values', 'y_values', 'xy_values', 'kv', 'kv_graph']
    allowed_names = ['points', 'xy0']
    cc = CodeChecker(allowed_imports=allowed_imports, allowed_calls=allowed_calls, allowed_names=allowed_names,
                     allowed_aliases=allowed_aliases, allowed_FunctionDefs=allowed_FunctionDefs)

    return cc


def call_generator(inputfile, plotlib=None, outputfile=None, check=True):
    """Calls the plot code generator"""
    formula = Formula()
    plot_data = PlotData()
    if check:
        code_checker = setup_code_checker()
    else:
        code_checker = None

    datahandler = DataHandler(formula=formula, plot_data=plot_data, plot_lib=plotlib, code_checker=code_checker)
    datahandler.load_project(filename=inputfile)

    print('\nGenerating plot code...', end='')
    plotcode = datahandler.combine_code()
    print('done.\n')

    if outputfile:
        with open(outputfile, 'w') as file:
            file.write(plotcode)
        print('Plot code has been written to {}.'.format(outputfile))
    else:
        print(plotcode)

    if check:
        print('\nRunning code checker...')
        errors, error_logs = datahandler.check_code()
        for i, error in enumerate(errors):
            print('Error code: {}'.format(error))
            for error_log in error_logs[i]:
                print(error_log)
        if len(errors) > 0:
            print('{} error(s) were observed in plot code!'.format(len(errors)))
            exit(1)
        else:
            print('No errors observed.')
            exit(0)
    else:
        print('\nWarning: Code checker has been disabled. Code was not checked for errors.')
    exit(0)


def main():
    """Main routine entry point for CLI script"""

    # definition of valid options and aliases
    valid_options = {
        '--plotlib': {
            'args': True,
            'valid_values': ['matplotlib', 'kivy-garden/graph']
        },
        '--output': {
            'args': True,
            'valid_values': None    # file name - no predefined values
        },
        '--input': {
            'args': True,
            'valid_values': None  # file name - no predefined values
        },
        '--no-check': {
            'args': False,
            'valid_values': None
        }
    }

    aliases = {
        '-p': '--plotlib',
        '-o': '--output',
        '-n': '--no-check',
        '-i': '--input'
    }

    # check command line arguments
    if len(sys.argv) == 1:
        print('simple-plotter: Not enough arguments!')
        print(usage_info)
        exit(1)
    elif len(sys.argv) == 2:
        if sys.argv[1] == '--help':
            print('simple-plotter CLI - code generator for python plots')
            print(usage_info)
            exit(0)
        else:  # assumes this is the project filename
            print('simple-plotter: Invalid number of arguments!')
            print(usage_info)
            exit(1)

    else:  # more than one argument

        argument_expected = False
        current_option = None
        options = {}
        for i, arg in enumerate(sys.argv):
            # print('Arg {}: {}'.format(i, arg))
            if i == 0:
                pass    # this is only the command name
            else:
                if argument_expected:
                    if valid_options[current_option]['valid_values'] is None:
                        options[current_option] = arg
                        argument_expected = False
                    else:
                        if arg in valid_options[current_option]['valid_values']:
                            options[current_option] = arg
                            argument_expected = False
                        else:
                            print('simple-plotter: Invalid value \'{}\' for \'{}\''.format(arg, current_option))
                            print(usage_info)
                            exit(1)
                else:
                    if arg in valid_options.keys():
                        current_option = arg
                    elif arg in aliases:
                        current_option = aliases[arg]
                    else:
                        print('simple-plotter: Unknown option \'{}\''.format(arg))
                        print(usage_info)
                        exit(1)

                    if valid_options[current_option]['args']:
                        argument_expected = True
                    else:
                        options[current_option] = None
                        argument_expected = False

        # print(options)

        # check options
        if '--plotlib' in options.keys():
            plotlib = options['--plotlib']
        else:
            plotlib = 'matplotlib'
        if '--output' in options.keys():
            outputfile = options['--output']
        else:
            outputfile = None
        if '--no-check' in options.keys():
            check = False
        else:
            check = True
        if '--input' in options.keys():
            inputfile = options['--input']
        else:
            print('simple-plotter: Input file not specified!')
            print(usage_info)
            exit(0)

        call_generator(inputfile=inputfile, plotlib=plotlib, outputfile=outputfile, check=check)


if __name__ == '__main__':
    main()
