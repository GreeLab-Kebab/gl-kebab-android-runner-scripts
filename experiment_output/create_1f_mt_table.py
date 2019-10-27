import os
import sys
from zipfile import ZipFile
import shutil
import re
import pandas as pd

RUN_EXPERIMENT_PATH = 'kebab/dciw/5. run_experiment.sh'
SUBJECTS = pd.DataFrame([
    (1, "m.youtube.com"),
    (2, "www.amazon.com"),
    (3, "www.wikipedia.org"),
    (4, "aws.amazon.com"),
    (5, "www.office.com"),
    (6, "www.buzzfeed.com"),
    (7, "nl.godaddy.com"),
    (8, "www.mozilla.org"),
    (9, "stackoverflow.com"),
    (10, "apache.org"),
    (11, "www.theguardian.com"),
    (12, "stackexchange.com"),
    (13, "www.paypal.com"),
    (14, "www.booking.com"),
    (15, "www.bbc.com"),
    (16, "www.amazon.in")
], columns=['ID', 'Subject'])

def read_file(file_path):
    with open(file_path,'r') as f:
        return list(map(lambda x: x.strip(), f.readlines()))

def main(excluded_path, zips):
    # All zips must exist for this to work
    if not (all(map(os.path.exists, zips))):
        print("ERROR: not all files passed as an argument exist! (%s)"%str(zips))
        exit(1)

    excluded_subjects = read_file(excluded_path)
    zips = filter(os.path.isfile, zips)
    zips = filter(lambda x: x.endswith(".zip"), zips)
    
    all_valid_experiments = []
    all_runs = []
    all_run_ids = []
    for zip_name in zips:
        with ZipFile(zip_name, 'r') as zip:
            raw_name = zip_name[:-4]
            output_dir = "%s_tmp"%zip_name
            zip.extract(RUN_EXPERIMENT_PATH, output_dir)
            
            lines = read_file(os.path.join(output_dir, RUN_EXPERIMENT_PATH))
            lines = filter(lambda x: x != "sleep 120" and x != "cd Experiments", lines)
            experiments = list(map(
                lambda x: x.replace(
                    "python ../../../android-runner config_", 
                    ""
                ).replace(
                    ".json", 
                    ""
                ), lines
            ))
            
            failed_experiments_path = "%s_failed_experiments.txt"%raw_name
            failed_experiments = read_file(failed_experiments_path) if os.path.exists(failed_experiments_path) else []

            experiments = list(filter(
                lambda x: not any(map(lambda y : x.endswith(y), excluded_subjects)),
                experiments
            ))
            failed_experiments = list(filter(
                lambda x: not any(map(lambda y : x.endswith(y), excluded_subjects)),
                failed_experiments
            ))

            valid_experiments = list(filter(
                lambda x: not any(map(lambda y: x.endswith(y), failed_experiments)),
                experiments
            ))

            assert(len(experiments) - len(failed_experiments) == len(valid_experiments))
            
            all_valid_experiments += valid_experiments
            all_runs += [raw_name] * len(valid_experiments)

            shutil.rmtree(output_dir)

    df = pd.DataFrame({
        'Subject': map(lambda x: x.split('_')[0], all_valid_experiments),
        'Optimization Level': map(lambda x: x.split('_')[1], all_valid_experiments),
        'Execution Index': range(1, len(all_valid_experiments)+1)
    })

    df = SUBJECTS.merge(df, on='Subject', how='right')
    df = df.sort_values(['ID', 'Optimization Level'])
    df.insert(3, 'Run ID', df.groupby(['ID', 'Optimization Level']).cumcount()+1)

    df.to_csv('1f_mt_table.csv', index=False)
    df.to_latex('1f_mt_table.tex', index=False)


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print("usage:")
        print("python3 create_1f_mt_table.py [excluded_subjects] [zip] [zip2] ... [zipN]")
        exit(1)

    main(sys.argv[1], sys.argv[2:])


