# Kebab Android Runner Scripts

In order to perform the experiment run the scripts in order.

1. `1. download_candidates.sh`: This script downloads the subjects on which the experiment is to be performed, they are initially called candidates and will become subjects when the JS code is injected (this is done during step 3).
2. `2. create_experiment_configs.py`: This script creates configs for each subject. The config file is used to perform an experiment for one subject with one treatment, the config files are passed to Android Runner in step 5.

3. `3. create_subjects.py`: This script injects JavaScript code into the candidates, turning them into subjects. This JavaScript code is used to measure the load time of the subjects.

4. `4. generate_exerpiement_runner.py`: This script generate the file used in step 5, it basically looks at all the experiments that are to be performed (by looking at the generated configs) and randomizes them.

5. `5. run_experiment.sh`: This script runs the experiment, invoking Android Runner with all the generated configs in a fixed random order.

## Notes:
1. Make sure to pass the host of the subjects to `2. create_experiment_configs.py`
2. Make sure to double check android-runner's location (passed to `4. generate_experiment_runner.py`).
