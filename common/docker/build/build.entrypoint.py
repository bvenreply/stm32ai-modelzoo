#!/bin/env python
import yaml
import sys
from os import path
import logging
import shutil
import subprocess as sp

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)

# In place dict merge (a is the receiver)
def merge(a: dict, b: dict, path=[]):
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            # elif a[key] != b[key]:
            #     raise Exception('Conflict at ' + '.'.join(path + [str(key)]))
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]  
    return a

CUBEAI_CODEGEN_ZIP_PATH = "/tmp/inputs/cubeai-output.zip"

def run():
    log.info("Starting up build job...")

    config = {}

    with open("/tmp/inputs/job.json", "rt") as file:
        job_config = yaml.safe_load(file)

        logging.debug("Job config: %r", job_config)

        assert "root" in job_config

        root = job_config["root"]

        assert isinstance(root, str)

        root = path.abspath(root)

        assert path.isdir(root), "Configured script root does not exist"

    user_config_path = path.join(root, "user_config.yaml")

    with open(user_config_path, "rt") as file:
        base_config = yaml.safe_load(file)
    
    _ = merge(config, base_config)

    with open("/tmp/inputs/config.json", "rt") as file:
        override_config = yaml.safe_load(file)
    
    _ = merge(config, override_config)

    config["hydra"] = { "run": { "dir": "outputs" } }

    logging.debug("Final config: %r", config)

    with open(user_config_path, "wt") as file:
        yaml.safe_dump(config, file)

    _spawned = sp.run(
        "python ./deploy.py",
        stdout=sys.stdout,
        stderr=sys.stderr,
        shell=True,
        cwd=root,
        check=True
    )

    outputs_path = path.join(root, "outputs")

    assert path.isdir(outputs_path), "Missing outputs folder"

    shutil.make_archive("/tmp/outputs/outputs", "zip", root_dir=outputs_path)

if __name__ == "__main__":
    run()
