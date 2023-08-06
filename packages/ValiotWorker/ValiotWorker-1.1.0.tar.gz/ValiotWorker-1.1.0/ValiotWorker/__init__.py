from .worker import ValiotWorker
from .worker import QueueType, JobStatus, PollingMode
from .uploaders import update_job
from . import worker

# * Package name:
name = 'ValiotWorker'
# * required here for pypi upload exceptions:
__version__ = "1.1.0"
