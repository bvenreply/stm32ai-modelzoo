from io import BytesIO
from typing import Any
import config
import time
import httpx


def token() -> str:
    with open("token.txt", "rt") as file:
        return file.read()


def headers():
    return {"Authorization": f"Bearer {token()}"}


class NamedBuffer(BytesIO):
    name: str

    def __init__(self, name: str, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.name = name


class JobException(Exception):
    ...


async def block_until_done(job_id: str):
    with httpx.Client() as client:
        while True:
            res = client.get(
                f"{config.JOBCONTROL_API_JOBS_ENDPOINT}/{job_id}", headers=headers()
            )
            job = res.json()
            status = job["status"]

            if status == "Succeeded":
                return job
            elif status == "Pending" or status == "Running":
                time.sleep(config.JOB_POLLING_INTERVAL_SECS)
                # Continue polling...
            else:
                raise JobException(f"job {job_id} has unexpected status: {status}")


def _artifacts(job):
    artifacts = job["outputs"]["artifacts"]

    return tuple((item["name"], item["authorizedGetUrl"]) for item in artifacts)


def download_artifacts(job):
    pairs = _artifacts(job)

    with httpx.Client() as client:
        return {
            pair[0]: client.get(pair[1]).raise_for_status().read() for pair in pairs
        }
