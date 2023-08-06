#!/usr/bin/env python
"""
Python client to interface with Ublox receivers

Usage:
    pyublox -h | --help
    pyublox --version
    pyublox config  [ --rate <rate> ] [ --obs-data ] [ --nav-data ] [ --llh-data ]
    pyublox record --file <file>


Options:
    -h --help        shows the help
    -v --version     shows the version
    --rate           Data rate at which the observable will be recorded
    --obs-data       Switch to turn on recording of observables (GNSS measurements)
    --nav-data       Switch to turn on recording of navigation data
    --llh-data       Switch to turn on recording of position estimates
    --file           Record the ublox stream to a file


Commands:
    config         Submit configuration options to ublox
    record         Record the ublox stream to a file
"""
import docopt
import pkg_resources
import sys

from . import commands



def main():
    """
    """

    version = pkg_resources.require("pyublox")[0].version

    args = docopt.docopt(__doc__, version=version, options_first=False)

    #sys.stderr.write("Start main, parsed arg\n {}\n".format(args))

    command, command_args = __get_command__(args)

    try:
        command(**command_args)
    except ValueError as e:
        sys.stderr.write("FATAL: " + str(e))

    return 0



def __get_command__(args):

    command = None
    command_args = {}

    if args['config']:
        command = commands.config
        command_args = __get_args__(args)
    
    elif args['record']:
        command = commands.record
        command_args = __get_args__(args)

    return command, command_args


def __get_args__(args):

    command_args = {}

    return command_args


if __name__ == "__main__":

    return_code = main()
    sys.exit(return_code)
