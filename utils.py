from io import BytesIO
from typing import Any, Tuple
from functools import cache
import config
from collections.abc import Sequence, Mapping
import httpx
import json

@cache
def token() -> str:
    with open("token.txt", "rt") as file:
        return file.read()

headers = {"Authorization": f"Bearer {token()}"}

class NamedBuffer(BytesIO):
    name: str

    def __init__(self, name: str, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.name = name


class JobException(Exception):
    ...
    
async def block_until_done(job_id: str) -> Mapping[str, Any]:
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "GET",
            f"{config.JOBCONTROL_API_JOBS_ENDPOINT}/{job_id}",
            headers=headers,
            params={
                "watch": "true"
            },
            timeout=300
        ) as res:
            async for line in res.aiter_lines():
                job = json.loads(line)
                match job["status"]:
                    case "Succeeded":
                        return job
                    case "Pending" | "Running":
                        continue
                    case _:
                        raise JobException(f"Job has unexpected status: {job['status']}")

        raise JobException("Job watch terminated unexpectedly")

def _artifacts(job: Mapping[str, Any]) -> Sequence[Tuple[str, str]]:
    artifacts = job["outputs"]["artifacts"]

    return tuple(
        (item["name"], item["authorizedGetUrl"]) for item in artifacts
    )

def download_artifacts(job: Mapping[str, Any]) -> Mapping[str, Any]:

    pairs = _artifacts(job)

    with httpx.Client() as client:
        return {
            pair[0]: client.get(pair[1]).raise_for_status().read() for pair in pairs
        }
