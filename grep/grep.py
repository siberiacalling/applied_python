import re
import argparse
import sys


def output(line):
    print(line)


def context_in_params(params):
    if params.before_context == 0 and params.context == 0 and params.after_context == 0:
        return False
    else:
        return True


def update_lines_before(lines_before, context_before, line, number):
    if context_before != 0:
        if len(lines_before) < context_before:
            lines_before.append((line, number))
        else:
            for i in range(len(lines_before) - 1):
                lines_before[i] = lines_before[i + 1]
            if len(lines_before) != 0:
                del lines_before[len(lines_before) - 1]
            lines_before.append((line, number))
    return lines_before


def processing_print(line, number, params, selected_by_regexp=False):
    if params.line_number is True:
        if selected_by_regexp is True:
            output(str(number) + ':' + line)
        else:
            output(str(number) + '-' + line)
    else:
        output(line)


def processing_context(params, lines, regexp):
    context_before = max(params.before_context, params.context)
    context_after = max(params.after_context, params.context)
    number_lines_after = 0
    number = 0
    lines_before = []
    for line in lines:
        line = line.rstrip()
        number += 1
        if bool(re.search(regexp, line, re.I if params.ignore_case else 0)) is (params.invert is False):
            while len(lines_before) > 0:
                line_for_print = lines_before.pop(0)
                processing_print(line_for_print[0], line_for_print[1], params, False)
            processing_print(line, number, params, True)
            number_lines_after = context_after
        elif number_lines_after != 0:
            processing_print(line, number, params, False)
            number_lines_after -= 1
        else:
            lines_before = update_lines_before(lines_before, context_before, line, number)


def processing_not_context(params, lines, regexp):
    number = 0
    number_of_selected = 0
    for line in lines:
        line = line.rstrip()
        number += 1
        if bool(re.search(regexp, line, re.I if params.ignore_case else 0)) is (params.invert is False):
            number_of_selected += 1
            if params.count is False:
                processing_print(line, number, params, True)
    if params.count is True:
        output(str(number_of_selected))


def grep(lines, params):
    regexp = params.pattern
    regexp = regexp.replace('?', '.')
    regexp = regexp.replace('*', '.*')
    if context_in_params(params):
        processing_context(params, lines, regexp)
    else:
        processing_not_context(params, lines, regexp)


def parse_args(args):
    parser = argparse.ArgumentParser(description='This is a simple grep on python')
    parser.add_argument(
        '-v', action="store_true", dest="invert", default=False, help='Selected lines are those not matching pattern.')
    parser.add_argument(
        '-i', action="store_true", dest="ignore_case", default=False, help='Perform case insensitive matching.')
    parser.add_argument(
        '-c',
        action="store_true",
        dest="count",
        default=False,
        help='Only a count of selected lines is written to standard output.')
    parser.add_argument(
        '-n',
        action="store_true",
        dest="line_number",
        default=False,
        help='Each output line is preceded by its relative line number in the file, starting at line 1.')
    parser.add_argument(
        '-C',
        action="store",
        dest="context",
        type=int,
        default=0,
        help='Print num lines of leading and trailing context surrounding each match.')
    parser.add_argument(
        '-B',
        action="store",
        dest="before_context",
        type=int,
        default=0,
        help='Print num lines of trailing context after each match')
    parser.add_argument(
        '-A',
        action="store",
        dest="after_context",
        type=int,
        default=0,
        help='Print num lines of leading context before each match.')
    parser.add_argument('pattern', action="store", help='Search pattern. Can contain magic symbols: ?*')
    return parser.parse_args(args)


def main():
    params = parse_args(sys.argv[1:])
    grep(sys.stdin.readlines(), params)


if __name__ == '__main__':
    main()
