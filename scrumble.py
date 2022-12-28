#! /bin/env python3

import argparse
import collections.abc
import datetime
import itertools
import json
import logging
import random
import sys

logging.basicConfig(level=logging.INFO)

DEFAULT_LIMIT=1024
KEYWORD_GROUPS="groups"
KEYWORD_ALL_SOLUTIONS="all_solutions"
KEYWORD_SOLUTION="solution"
KEYWORD_EXPORT_DATE="export_date"


# A constraint is a tuple (A, B) mean A cannot make a gift to B (and only in this way)
# So all constraints are stored in a set( (A, B), (B, C) )

def get_subset_of(member, position, possible):
    return (x for x in possible
    if x[position] == member)


def build_gift_path(member, current_solution, all_gift_possible, expected_length):
    logging.debug("Searching path for: %s, %s %s", member, current_solution, all_gift_possible)
    if len(all_gift_possible) == 0:
        if len(current_solution) == expected_length:
            yield current_solution
        else:
            return
    else:
        subset_possible = set(get_subset_of(member, 0, all_gift_possible))
        for x in sorted(subset_possible):
            have_gift = set(get_subset_of(x[1], 1, all_gift_possible)) # now we remove x1 witch already have a gift
            tmp_sol = list(current_solution) # create a copy
            tmp_sol.append(x)
            yield from tuple(build_gift_path(x[1], tmp_sol, all_gift_possible - subset_possible - have_gift, expected_length))


def merge_solution(solution, all_solution):
    m = dict(solution)
    present = False
    for s in all_solution:
        if s == m:
            present = True
    if not present:
        all_solution.append(m)


def search_gifts(all_people, constraints):
    logging.debug("All people are: %s", all_people)
    logging.debug("Constraints are: %s", constraints)
    all_gift_possible = set(itertools.permutations(all_people, 2)) - constraints

    logging.debug("All gift possible are: %s", all_gift_possible)

    all_solution = []
    for p in all_people:
        for solution in build_gift_path(p, [], all_gift_possible, len(all_people)):
            merge_solution(solution, all_solution)

    return all_solution


def print_all_solution(solutions):
    for i, s in enumerate(solutions):
        sol_str = get_gift_solution(s)
        print(f"{i}) {sol_str}")
        


def load_config(conf_file):
    with open(conf_file, "r") as fh:
        return json.load(fh)


def load_constraint(all_constraints, data):
    if KEYWORD_GROUPS in data:
        all_constraints.update(get_groups_constraints(data))
    if KEYWORD_SOLUTION in data:
        all_constraints.update(get_solution_constraints(data))


def load_constraints_from_files(constraints_files):
    all_constraints = set()
    for constraint_file in constraints_files:
        root = load_config(constraint_file)
        if isinstance(root, collections.abc.Sequence):
            for x in root:
                load_constraint(all_constraints, x)
        elif isinstance(root, collections.abc.Mapping):
            load_constraint(all_constraints, root)
    return all_constraints


def get_groups_constraints(configuration):
    logging.debug("Loading groups constraints.")
    group_constraints = set()
    for group in configuration[KEYWORD_GROUPS]:
        group_constraints.update(itertools.permutations(group))
    logging.debug("Groupe constraints are: %s", group_constraints)
    return group_constraints


def get_solution_constraints(configuration):
    logging.debug("Loading solution constraints.")
    solution_constraints = set(configuration[KEYWORD_SOLUTION].items())
    logging.debug("Solution constraints are: %s", solution_constraints)
    return solution_constraints


def get_all_people_from_constraints(constraints):
    return list(sorted(set(sum(constraints, ()))))


def export_object(data, output):
    logging.debug("exporting object to: %s", output)
    export_data = dict(data)
    export_data[KEYWORD_EXPORT_DATE] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='minutes')
    with open(output, "w") as fh:
        json.dump([export_data], fh, sort_keys=True, indent=' ')


def get_gift_solution(solution):
    logging.debug("Trying to print solutions: %s", len(solution))
    key = list(sorted(solution.keys()))[0]
    x = [key]
    while True:
        next_key = solution[key]
        if next_key in x:
            break
        x.append(next_key)
        key = next_key
    return "->".join(x)


def build_parser():
    parser = argparse.ArgumentParser(
                    prog = 'scrumble',
                    description = 'Search for christmas present',
                    epilog = 'Happy Christmas')
    parser.add_argument('constraints_file', nargs='+', help='Load files with constraints')
    parser.add_argument('-v', '--verbose', help="Verbose (default %(default)s)", action='store_true')
    parser.add_argument('-a', '--all-solutions', help="Output all solution to a file (default %(default)s).", action='store')
    parser.add_argument('--print-all', help="Print all solutions (default %(default)s).", action='store_true')
    parser.add_argument('-p', '--print', help="Print selected solution (default %(default)s).", action='store_true', default=False)
    parser.add_argument('-s', '--selector', help="Select element from the list of solutions (default %(default)s) (0 is first) (-1 is last) (r is random)", default="0")
    output = "solution_" + datetime.date.today().strftime("%Y%m%d") + ".json"
    parser.add_argument('-e', '--export', help="Write solution to the path given (default %(default)s).", default=output)
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    logging.debug("Options are: %s", args)

    constraints = load_constraints_from_files(args.constraints_file)
    all_people = get_all_people_from_constraints(constraints)
    all_solutions = search_gifts(all_people, constraints)

    if not all_solutions:
        print("No solution found. Try to remove some constraints.", file=sys.stderr)
        sys.exit(1)

    if args.all_solutions:
        export_object({KEYWORD_ALL_SOLUTIONS: all_solutions}, args.all_solutions)
    
    if args.print_all:
        print_all_solution(all_solutions)

    selector = args.selector
    if selector == 'r':
        selector = random.randint(0, len(all_solutions))
    else:
        selector = int(selector)

    solution = all_solutions[selector%len(all_solutions)]
    if args.print:
        print(get_gift_solution(solution))

    export_object({KEYWORD_SOLUTION: solution, }, args.export)


if __name__ == "__main__":
    main()