# Generic train workload meant to be run from jobcontrol-api

## Runtime interface

### Input

The job expects the following files as input:

- A json-formatted file at `/tmp/inputs/config.json` representing overrides for the options provided in `user_config.yaml`. The options in this file are merged together with the defaults in the training script folder
- A json-formatted file at `/tmp/inputs/job.json` containing job-specific input values. Most importantly, we expect a property under the key `root` whose value must be a string representing the path to the directory containing the target script. This is meant to be the mechanism enabling generality over all modelzoo examples. We'll henceforth refer to this path as `<script-root>`
- The training dataset as a zip archive located at `/tmp/inputs/train.zip`
- The (optional) validation dataset as a zip archive located at `/tmp/inputs/valid.zip`
- The (optional) test dataset as a zip archive located at `/tmp/inputs/test.zip` 

The dataset archives must contain the dataset folder at the top level. These archives will each be extracted in a target folder, the path to which will be respectively set as value to the options of `dataset.training_path`, `dataset.validation_path` and `dataset.test_path`.

### Output

After completing the training, we expect the folder `outputs` to be created in `<script-root>`. This folder is archived at `/tmp/outputs/outputs.zip`. 

## Build

The build context must be set at the root of the repository. from the folder where this file is located, the correct relative path to the build context is `../../..`. 

Assuming the repo root is the current directory, build with

```sh
docker build --file common/docker/train/train.Dockerfile .
```

## jobcontrol-api
