
_default_base_url = "https://dev.stm-vespucci.com"

try:
    from getpass import getuser
    VESPUCCI_BASE_URL = (
        "http://jobcontrol-api:5002"
        if getuser() == "vespucciuser"
        else _default_base_url
    )
except Exception as _:
    VESPUCCI_BASE_URL = _default_base_url


JOBCONTROL_API_BASE_URL = f"{VESPUCCI_BASE_URL}/svc/jobcontrol/v1alpha1"
JOBCONTROL_API_JOBS_ENDPOINT = f"{JOBCONTROL_API_BASE_URL}/jobs"
TRAINING_JOB_TEMPLATE_ID = "01HM2EE60T3HJ4G5MPYK3GVT5D"
CUBEAI_JOB_TEMPLATE_ID = "01HKWQDAW8CQA0AVQP5NSG4R76"
BENCHMARKING_JOB_TEMPLATE_ID = "01HKWQDAW8CQA0AVQP5NSG4R76"
COMPILATION_JOB_TEMPLATE_ID = "01HMBW4VR0P1YQXJZEDW04YHJY"

JOB_POLLING_INTERVAL_SECS = 1
