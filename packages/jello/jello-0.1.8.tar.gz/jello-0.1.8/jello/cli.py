#!/usr/bin/env python3
"""jello - query JSON at the command line with python syntax"""

import os
import sys
import textwrap
import json
import signal
from contextlib import redirect_stdout
import io
import ast

__version__ = '0.1.8'


def ctrlc(signum, frame):
    """exit with error on SIGINT"""
    sys.exit(1)


def get_stdin():
    """return STDIN data"""
    if sys.stdin.isatty():
        return None

    return sys.stdin.read()


def helptext():
    print_error(textwrap.dedent('''\
        jello:   query JSON at the command line with python syntax

        Usage:  <JSON Data> | jello [OPTIONS] QUERY

                -c    compact JSON output
                -v    version info
                -h    help

        Use '_' as the input data and assign the result to 'r'. Use python dict syntax.

        Example:
                <JSON Data> | jello 'r = _["foo"]'
    '''))


def print_error(message):
    """print error messages to STDERR and quit with error code"""
    print(message, file=sys.stderr)
    sys.exit(1)


def print_json(data, compact=False):
    if isinstance(data, (list, dict)):
        if compact:
            print(json.dumps(data))
        else:
            print(json.dumps(data, indent=2))
    elif data is None:
        exit()
    else:
        print(data)


def process(data):
    result = None
    result_list = []
    try:
        if len(data.splitlines()) == 1:
            try:
                result = ast.literal_eval(data)
            except Exception:
                # if exception then it was not a list or dict
                result = data.lstrip("'").rstrip("'")
        else:
            for entry in data.splitlines():
                try:
                    result_list.append(ast.literal_eval(entry))
                except Exception:
                    # if exception then it was not a list or dict
                    result_list.append(entry.lstrip("'").rstrip("'"))

    except Exception as e:
        print(e)
        sys.exit(1)

    if result_list:
        if isinstance(result_list[0], (dict, list)):
            list_of_objs = []
            for obj in result_list:
                list_of_objs.append(json.dumps(obj))
            result = '\n'.join(list_of_objs)
        else:
            result = '\n'.join(result_list)

    return result


def pyquery(data, query):
    _ = None
    result = None
    query = 'r = None\n' + query + '\nprint(r)'

    # load the JSON or JSON Lines data
    try:
        json_dict = json.loads(data)

    except Exception:
        # if json.loads fails, assume the data is formatted as json lines and parse
        data = data.splitlines()
        data_list = []
        for i, jsonline in enumerate(data):
            try:
                entry = json.loads(jsonline)
                data_list.append(entry)
            except Exception as e:
                # can't parse the data. Throw a nice message and quit
                print(textwrap.dedent(f'''\
                    jello:  Exception - {e}
                            Cannot parse line {i + 1} (Not JSON or JSON Lines data):
                            {str(jsonline)[:70]}
                    '''))
                sys.exit(1)

        json_dict = data_list

    _ = json_dict

    f = io.StringIO()
    try:
        with redirect_stdout(f):
            print(exec(compile(query, '<string>', 'exec')))
            output = f.getvalue()[0:-6]

    except KeyError as e:
        print(textwrap.dedent(f'''\
            jello:  Key does not exist: {e}
        '''))
        sys.exit(1)

    except IndexError as e:
        print(textwrap.dedent(f'''\
            jello:  {e}
        '''))
        sys.exit(1)

    result = process(output)

    return result


def main():
    # break on ctrl-c keyboard interrupt
    signal.signal(signal.SIGINT, ctrlc)
    stdin = get_stdin()

    query = 'r = _'

    options = []
    long_options = {}
    for arg in sys.argv[1:]:
        if arg.startswith('-') and not arg.startswith('--'):
            options.extend(arg[1:])

        elif arg.startswith('--'):
            try:
                k, v = arg[2:].split('=')
                long_options[k] = int(v)
            except Exception:
                helptext()

        else:
            query = arg

    compact = 'c' in options
    version_info = 'v' in options
    helpme = 'h' in options

    if helpme:
        helptext()

    if version_info:
        print_error(f'jello:   version {__version__}\n')

    if stdin is None:
        print_error('jello:  missing piped JSON or JSON Lines data\n')

    result = pyquery(stdin, query)

    print_json(result, compact=compact)


if __name__ == '__main__':
    main()
