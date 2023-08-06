#!/usr/bin/env python3
"""jello - query JSON at the command line with python syntax"""

import os
import sys
import platform
import textwrap
import json
import signal
from contextlib import redirect_stdout
import io
import ast

__version__ = '0.5.0'


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
                -i    initialize environment with .jelloconf.py in ~ (linux) or %appdata% (Windows)
                -l    output as lines suitable for assignment to a bash array
                -n    print selected null values
                -r    raw string output (no quotes)
                -v    version info
                -h    help

        Use '_' as the input data and assign the result to 'r'. Use python dict syntax.

        Example:
                <JSON Data> | jello 'r = _["foo"]'
                variable=($(cat data.json | jello -l 'r = _["foo"]'))
    '''))


def print_error(message):
    """print error messages to STDERR and quit with error code"""
    print(message, file=sys.stderr)
    sys.exit(1)


def lines(data):
    """This function is deprecated. Instead, use the -l option"""
    return data


def create_json(data, compact=False, nulls=None, lines=None, raw=None):
    if isinstance(data, dict):
        if compact or lines:
            return json.dumps(data)
        else:
            return json.dumps(data, indent=2)

    if isinstance(data, list):
        # check if this list includes lists
        list_includes_list = False
        for item in data:
            if isinstance(item, list):
                list_includes_list = True
                break

        if not lines and not list_includes_list:
            new_list = []

            for entry in data:
                if isinstance(entry, str):
                    new_list.append(entry.replace('\u2063', '\n'))
                else:
                    new_list.append(entry)

            if compact:
                return json.dumps(new_list)

            else:
                return json.dumps(new_list, indent=2)

        if not lines:
            if compact:
                return json.dumps(data)
            else:
                return json.dumps(data, indent=2)

        elif lines and list_includes_list:
            print_error('jello:  Cannot print list of lists as lines. Try normal JSON output.\n')

        # print lines for a flat list
        else:
            flat_list = ''
            for entry in data:
                if entry is None:
                    if nulls:
                        flat_list += 'null\n'
                    else:
                        flat_list += '\n'

                elif entry is True:
                    flat_list += 'true\n'

                elif entry is False:
                    flat_list += 'false\n'

                elif isinstance(entry, str):
                    string_data = entry.replace('\u2063', r'\n')
                    if raw:
                        flat_list += f'{string_data}\n'
                    else:
                        flat_list += f'"{string_data}"\n'

                else:
                    # don't pretty print JSON Lines
                    flat_list += json.dumps(entry) + '\n'

            return flat_list.rstrip()

    # naked single item return case
    elif data is None:
        if nulls:
            return 'null'
        else:
            return ''

    elif data is True:
        return 'true'

    elif data is False:
        return 'false'

    elif isinstance(data, (int, float)):
        return data

    elif isinstance(data, str):
        string_data = data.replace('\u2063', r'\n')
        if raw:
            return string_data
        else:
            return f'"{string_data}"'


def normalize(data, nulls=None, raw=None):
    result_list = []

    # first check if it's a dict
    try:
        if isinstance(ast.literal_eval(data), dict):
            return ast.literal_eval(data.replace(r'\u2063', r'\n'))
    except Exception:
        # was not a dict
        pass

    try:
        for entry in data.splitlines():
            # check if the result is a single list with no dicts or other lists inside
            try:
                list_includes_obj = False
                check_list = ast.literal_eval(entry)
                if isinstance(check_list, list):
                    for item in check_list:
                        if isinstance(item, (list, dict)):
                            list_includes_obj = True
                            break

                if list_includes_obj:
                    # this is a higher-level list of dicts or lists. We can safely replace
                    # \u2063 with newlines here.
                    result_list.append(ast.literal_eval(entry.replace(r'\u2063', r'\n')))
                else:
                    # this is the last node. Don't replace \u2063 with newline yet...
                    # do this in print_json()
                    result_list.append(check_list)

            except (ValueError, SyntaxError):
                # if ValueError or SyntaxError exception then it was not a
                # list, dict, bool, None, int, or float - must be a string
                # we will replace \u2063 with newlines in print_json()
                result_list.append(str(entry))

    except Exception as e:
        print_error(textwrap.dedent(f'''\
            jello:  Normalize Exception: {e}
                    data: {data}
                    result_list: {result_list}
            '''))

    try:
        return result_list[0]

    except IndexError as e:
        print_error(textwrap.dedent(f'''\
            jello:  Normalize Exception: {e}
                    Cannot parse input (Not JSON or JSON Lines)
        '''))


def pyquery(data, query, initialize=None):
    _ = data
    jelloconf = ''

    if initialize:
        if platform.system() == 'Windows':
            conf_file = os.path.join(os.environ['APPDATA'], '.jelloconf.py')
        else:
            conf_file = os.path.join(os.environ["HOME"], '.jelloconf.py')

        try:
            with open(conf_file, 'r') as f: 
                jelloconf = f.read()
        except FileNotFoundError:
            print_error(textwrap.dedent(f'''\
                jello:  Initialization file not found: {conf_file}
            '''))

    query = jelloconf + 'r = None\n' + query + '\nprint(r)'
    output = None

    f = io.StringIO()
    try:
        with redirect_stdout(f):
            print(exec(compile(query, '<string>', 'exec')))
            output = f.getvalue()[0:-6]

    except KeyError as e:
        print_error(textwrap.dedent(f'''\
            jello:  Key does not exist: {e}
        '''))

    except IndexError as e:
        print_error(textwrap.dedent(f'''\
            jello:  {e}
        '''))

    except SyntaxError as e:
        print_error(textwrap.dedent(f'''\
            jello:  {e}
                    {e.text}
        '''))

    except TypeError as e:
        if output is None:
            output = ''
        else:
            print_error(textwrap.dedent(f'''\
                jello:  TypeError: {e}
            '''))

    except Exception as e:
        print_error(textwrap.dedent(f'''\
            jello:  Query Exception: {e}
                    _: {_}
                    query: {query}
                    output: {output}
        '''))

    return output


def load_json(data):
    # replace newline characters in the input text with unicode separator \u2063
    data = data.strip().replace(r'\n', '\u2063')

    # load the JSON or JSON Lines data
    try:
        json_dict = json.loads(data)

    except Exception:
        # if json.loads fails, assume the data is json lines and parse
        data = data.splitlines()
        data_list = []
        for i, jsonline in enumerate(data):
            try:
                entry = json.loads(jsonline)
                data_list.append(entry)
            except Exception as e:
                # can't parse the data. Throw a nice message and quit
                print_error(textwrap.dedent(f'''\
                    jello:  JSON Load Exception: {e}
                            Cannot parse line {i + 1} (Not JSON or JSON Lines data):
                            {str(jsonline)[:70]}
                    '''))

        json_dict = data_list

    return json_dict


def main(data=None, query='r = _', compact=None, lines=None, nulls=None, raw=None, version_info=None, helpme=None, initialize=None):
    # break on ctrl-c keyboard interrupt
    signal.signal(signal.SIGINT, ctrlc)

    commandline = False
    if data is None:
        commandline = True
        data = get_stdin()
    # for debugging
    # data = r'''["word", null, false, 1, 3.14, true, "multiple words", false, "words\nwith\nnewlines", 42]'''

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
            if commandline:
                query = arg

    compact = compact if not commandline else'c' in options
    initialize = initialize if not commandline else 'i' in options
    lines = lines if not commandline else 'l' in options
    nulls = nulls if not commandline else 'n' in options
    raw = raw if not commandline else 'r' in options
    version_info = version_info if not commandline else 'v' in options
    helpme = helpme if not commandline else 'h' in options

    if helpme:
        helptext()

    if version_info:
        print_error(f'jello:   version {__version__}\n')

    if data is None:
        print_error('jello:  missing piped JSON or JSON Lines data\n')

    # lines() function is deprecated. If lines() is found, then call the -l lines option instead.
    lines_warning = False
    if query.find('lines(') != -1:
        lines = True
        lines_warning = True

    list_dict_data = load_json(data)
    raw_response = pyquery(list_dict_data, query, initialize=initialize)
    normalized_response = normalize(raw_response, raw=raw, nulls=nulls)
    output = create_json(normalized_response, compact=compact, nulls=nulls, raw=raw, lines=lines)

    try:
        if commandline:
            print(output)
        else:
            return output

    except Exception as e:
        print_error(textwrap.dedent(f'''\
            jello:  Output Exception:  {e}
                    list_dict_data: {list_dict_data}
                    raw_response: {raw_response}
                    normalized_response: {normalized_response}
                    output: {output}
        '''))

    if lines_warning:
        print('\njello:  Warning: lines() function is deprecated. Please use the -l option instead.\n', file=sys.stderr)


if __name__ == '__main__':
    main()
