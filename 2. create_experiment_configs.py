#!/usr/bin/python

import os
import sys
import glob2

def create_dir_if_not_exists(dir):
    if not os.path.exists(dir): os.mkdir(dir)

def is_non_empty(x):
    return len(x) != 0

def starts_with(x, c):
    return x[0] == c

def read_lines_from_file(file):
    with open(file, 'r') as f:
        return f.readlines()

def write_lines_to_file(file, lines):
    with open(file, 'w') as f:
        f.writelines(lines)

def main(host_url, candidates_dir, config_dir, base_config, treatments):
    assert(os.path.exists(candidates_dir))
    create_dir_if_not_exists(config_dir)

    subjects = list(
        filter(lambda x: is_non_empty(x) and not starts_with(x, '.'), os.listdir(candidates_dir))
    )

    config_base_lines = read_lines_from_file(base_config)

    for subject in subjects:
        for treatment in treatments:
            index_location = locate_index(
                os.path.join(candidates_dir, subject),
                treatment
            )

            # remove Subjects from the index location since web servers root will be subjects_dir
            # reformat the path to support windows
            url = host_url + "/" + "/".join(os.path.split(index_location[len(candidates_dir)+1:]))
            config_name = "config_" + subject + "_" + treatment + ".json"

            print("writing... " + config_name + " -> " + url)
            write_lines_to_file(
                os.path.join(config_dir, config_name),
                map(lambda x: x.replace("{subject}", url), config_base_lines)
            )
            
def locate_index(subject_dir, treatment):
    result = glob2.glob(os.path.join(subject_dir, "**", treatment, "index.html"))

    if len(result) == 1: 
        return result[0]

    result = glob2.glob(os.path.join(subject_dir, "**", treatment, "*.html"))
    assert(len(result) == 1)

    return result[0]

if __name__ == '__main__':
    if len(sys.argv) == 2:
        host_url = sys.argv[1]
        candidates_dir = 'Candidates' 
        config_dir = 'Experiments'
        base_config = 'base_config.json'
        treatments = ['0', '1', '2', '3']
    elif len(sys.argv) == 6:
        host_url = sys.argv[1]
        candidates_dir = sys.argv[2]
        config_dir = sys.argv[3]
        base_config = sys.argv[4]
        treatments = sys.argv[5].split(',')
    else:
        print("Invalid arguments")
        exit(1)

    if host_url[-1] == "/":
        host_url = host_url[:-1]

    main(host_url, candidates_dir, config_dir, base_config, treatments)
