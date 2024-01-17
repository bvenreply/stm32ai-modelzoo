#!/usr/bin/env python
import yaml
import sys
from os import path, makedirs
import logging
import shutil
import subprocess as sp
import zipfile as zf

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

    assert path.isfile(CUBEAI_CODEGEN_ZIP_PATH), "Missing CubeAI codegen archive"

    outputs_path = path.join(root, "outputs")
    stm32ai_files_path = path.join(outputs_path, "stm32ai_files")
    
    makedirs(stm32ai_files_path, exist_ok=True)

    with zf.ZipFile(CUBEAI_CODEGEN_ZIP_PATH, "r") as archive:
        archive.extractall(stm32ai_files_path)

    user_config_path = path.join(root, "user_config.yaml")

    with open(user_config_path, "rt") as file:
        base_config = yaml.safe_load(file)
    
    _ = merge(config, base_config)

    with open("/tmp/inputs/config.json", "rt") as file:
        override_config = yaml.safe_load(file)
    
    _ = merge(config, override_config)

    config["hydra"] = { "run": { "dir": "outputs" } }
    config["model"]["model_path"] = "/tmp/inputs/model.tflite"

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

    project_folder = path.join(path.dirname(path.dirname(root)), "getting_started")
    assert path.isdir(project_folder), "Missing project folder"

    shutil.make_archive("/tmp/outputs/getting_started", "zip", root_dir=project_folder)

if __name__ == "__main__":
    run()
