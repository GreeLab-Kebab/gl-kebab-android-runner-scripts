#!/usr/bin/python

import os
import sys
import random

def is_non_empty(x):
    return len(x) != 0

def main(config_dir, android_runner_path):
    configs = list(
        filter(lambda x: is_non_empty(x) and x.startswith('config_'), os.listdir(config_dir))
    )

    random.shuffle(configs)

    with open('5. run_experiment.sh', 'w') as f:
        f.write("cd %s\n"%config_dir)
        for config in configs:
            f.write("python %s %s\n" % (android_runner_path, config))
            f.write("sleep 120\n")



if __name__ == '__main__':
    if len(sys.argv) == 1:
        config_dir = 'Experiments'
        android_runner_path = '../../../android-runner'
    elif len(sys.argv) == 3:
        config_dir = sys.argv[1]
        android_runner_path = sys.argv[2]
    else:
        print("Invalid arguments")
        exit(1)

    main(config_dir, android_runner_path)
