"""Run multiple trials of multiple simulations"""

import argparse
import csv
from collections import namedtuple
import os
import subprocess

from mihifepe import constants, utils

TRIAL = "trial"
SUMMARY_FILENAME = "all_trials_summary"

Trial = namedtuple("Trial", ["cmd", "output_dir"])


def main():
    """Main"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-num_trials", type=int, default=3)
    parser.add_argument("-start_seed", type=int, default=100000)
    parser.add_argument("-type", choices=[constants.INSTANCE_COUNTS, constants.FEATURE_COUNTS,
                                          constants.NOISE_LEVELS, constants.SHUFFLING_COUNTS],
                        default=constants.INSTANCE_COUNTS)
    parser.add_argument("-summarize_only", help="enable to assume that the results are already generated,"
                        " and just summarize them", action="store_true")
    parser.add_argument("-output_dir", required=True)

    args, pass_arglist = parser.parse_known_args()
    args.pass_arglist = " ".join(pass_arglist)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    args.logger = utils.get_logger(__name__, "%s/run_trials.log" % args.output_dir)

    trials = gen_trials(args)
    run_trials(args, trials)
    summarize_trials(args, trials)


def gen_trials(args):
    """Generate multiple trials, each with multiple simulations"""
    trials = []
    for seed in range(args.start_seed, args.start_seed + args.num_trials):
        output_dir = "%s/trial_%s_%d" % (args.output_dir, args.type, seed)
        cmd = ("python -m mihifepe.simulation.run_simulations -seed %d -type %s -output_dir %s %s" %
               (seed, args.type, output_dir, args.pass_arglist))
        trials.append(Trial(cmd, output_dir))
    return trials


def run_trials(args, trials):
    """Run multiple trials, each with multiple simulations"""
    if not args.summarize_only:
        for trial in trials:
            args.logger.info("Running trial: %s" % trial.cmd)
            subprocess.check_call(trial.cmd, shell=True)


def summarize_trials(args, trials):
    """Summarize outputs from trials"""
    # pylint: disable = too-many-locals
    # Read data
    items = []
    for trial in trials:
        trial_results_filename = "%s/%s_%s.csv" % (trial.output_dir, constants.ALL_SIMULATION_RESULTS, args.type)
        with open(trial_results_filename, "r") as trial_results_file:
            reader = csv.reader(trial_results_file, delimiter=",")
            reader.__next__()
            for row_idx, row in enumerate(reader):
                values = [float(elem) for elem in row]
                if row_idx == len(items):
                    items.append(values)
                else:
                    items[row_idx] = map(sum, zip(items[row_idx], values))
    items = [[elem / args.num_trials for elem in item] for item in items]
    # Number formatting
    for item in items:
        if args.type != constants.NOISE_LEVELS:
            item[0] = int(item[0])
        item[1:] = [round(elem, 4) for elem in item[1:]]
    # Write to file
    summary_filename = "%s/%s.csv" % (args.output_dir, SUMMARY_FILENAME)
    header = ([args.type, constants.FDR, constants.POWER, constants.OUTER_NODES_FDR, constants.OUTER_NODES_POWER,
               constants.BASE_FEATURES_FDR, constants.BASE_FEATURES_POWER, constants.INTERACTIONS_FDR, constants.INTERACTIONS_POWER])
    with open(summary_filename, "w", newline="") as summary_file:
        writer = csv.writer(summary_file, delimiter=",")
        writer.writerow(header)
        for item in items:
            writer.writerow([str(elem) for elem in item])
    # Format nicely
    formatted_summary_filename = "%s/%s_formatted.csv" % (args.output_dir, SUMMARY_FILENAME)
    subprocess.call("column -t -s ',' %s > %s" % (summary_filename, formatted_summary_filename), shell=True)


if __name__ == "__main__":
    main()
