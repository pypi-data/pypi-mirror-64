import pydash as __
import time
import json
from json.decoder import JSONDecodeError
import multiprocessing as mp
from multiprocessing import SimpleQueue
from datetime import datetime, timedelta
from enum import Enum
from pygqlc import GraphQLClient
from singleton_decorator import singleton
from .Notifications import NotificationBehaviour
from .Logging import log, LogLevel, LogStyle
from . import uploaders
from . import queries
from . import mutations
from . import subscriptions
from .dateHelpers import getUtcDate
from .croniterHelpers import get_croniter

class QueueType(Enum):
  EVENT= 'EVENT'
  FREQUENCY = 'FREQUENCY'
  ON_DEMAND = 'ON_DEMAND'
  SCHEDULE = 'SCHEDULE'

class JobStatus(Enum):
  ABORTED = 'ABORTED'
  ERROR = 'ERROR'
  FINISHED = 'FINISHED'
  PAUSED = 'PAUSED'
  RUNNING = 'RUNNING'
  WAITING = 'WAITING'

class PollingMode(Enum):
  QUERY = 'QUERY'
  SUBSCRIPTION = 'SUBSCRIPTION'

DEFAULT_EVENT_CONFIG = {
  "timeout": 5.0, # seconds to wait, None to run ASAP
  "min_batch": 10,
  "max_batch": 100
}

def safe_pop(data, index=0, default=None):
  if len(data) > 0:
    return data.pop(index)
  else:
    return default

@singleton
class ValiotWorker():
  def __init__(self):
    self.queues = {}
    self.eventQueues = {}
    self.currentQueues = []
    self.lockedJobs = []
    self.gql = GraphQLClient()
    self.worker = None
    self.worker_code = None
    self.pollingMode = PollingMode.QUERY
    self.context = None
    self.unsubJobCreated = None
    # logging attributes
    self.loggingStyle = LogStyle.PREFIX_FIRST_LINE
    self.stopLogging = False
    self.loggingProcess = None
    self.log = None
    self.logQueues = {
        'main': SimpleQueue()  # queue for the main thread (Orchestator)
    }
  
  def setClient(self, client):
    self.gql = client
  
  def setWorker(self, worker):
    self.worker_code = worker
  
  def setPollingMode(self, mode):
    self.pollingMode = mode
  
  def setLoggingStyle(self, style):
    self.loggingStyle = style

  def job(
    self,
    name, 
    alias, 
    description='', 
    schedule='', 
    enabled=None, 
    queueType=QueueType.ON_DEMAND,
    query='',
    lockRequired=False,
    notificationBehaviour=NotificationBehaviour.DEFAULT,
    notificationFrequency = '',
    notificationSchedule = '',
    eventConfig = DEFAULT_EVENT_CONFIG
    ):
    def wrap(f):
      parameters = {
        'name': name,
        'alias': alias,
        'description': description,
        'schedule': schedule,
        'type': queueType.value,
        'query': query,
        'lockRequired': lockRequired,
        'function': f,
        "last_run_at": datetime.now()
      }
      if enabled is not None:
        parameters['enabled'] = enabled
      self.queues[name] = parameters
      self.eventQueues[name] = {
        "name": name,
        "function": f,
        "mailbox": [],
        "config": {**DEFAULT_EVENT_CONFIG, **eventConfig},
        "start_time": None # Time to track, if elapsed and mailbox not empty, trigger event
      }
      return f
    return wrap

  def not_found(self, job_id, update_job, kwargs):
    from .Notifications import nextNotifOld
    self.log(LogLevel.ERROR, 'Function not found :(')
    message= 'Funcion no habilitada, favor de contactar a administrador'
    notificationData = {}
    if(nextNotifOld(kwargs['job'])): 
      data, errors = self.gql.mutate(mutations.create_notification, {
        'context': 'DANGER',
        'title': f'Error en {kwargs["job"]["queue"]["alias"]}',
        'content': message,
        'metadata': json.dumps({"resolved": False}),
      })
      now = getUtcDate(datetime.now())
      nextNotifDate = now + timedelta(minutes=20)
      notificationData = {
        'id': data['result']['id'],
        'Sent': True,
        'SentAt': now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        # 'frequency': '*/2 * * * *', # cron descriptor or empty string
        'sendNextAt': nextNotifDate.strftime("%Y-%m-%dT%H:%M:%SZ"), # cron descriptor or empty string
      }
    update_job({
      'id': job_id,
      'status': 'ERROR',
      'output': json.dumps({
        'notification': notificationData,
        'message': message
      })
    })

  # Run helpers: -------------------------------
  def getJobData(self, job):
    NOT_FOUND = {
      'alias': 'Funcion no encontrada',
      'description': 'Funcion ejecutada cuando se trata de llamar Job sin una función registrada',
      'schedule': None,
      'enabled': True,
      'type': QueueType.ON_DEMAND,
      'function': self.not_found,
      "last_run_at": datetime.now()
    }
    fn_name = __.get(job, 'queue.name', 'NOT_FOUND')
    job_dict = __.get(self.queues, fn_name, NOT_FOUND)
    return fn_name, job_dict

  def abortJob(self, job):
    variables = {
      'id': job['id'],
      'status': 'ABORTED'
    }
    data, errors = self.gql.mutate(mutations.update_job, variables)
  
  def lockQueue(self, queue_name):
    variables = {
      'queue': queue_name,
      'worker': self.worker['code'],
      'active': True,
      'startAt': getUtcDate(datetime.now()).strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    data, errors = self.gql.mutate(mutations.create_lock, variables)
    lock = __.get(data, 'result')
    queue_index = __.arrays.find_index(self.currentQueues, lambda q: q['name'] == queue_name)
    self.currentQueues[queue_index]['locks'].insert(0, lock)
    return lock  # returns lock object
  
  def unlockQueue(self, queue_name, lock):
    variables = {
      'id': lock['id'],
      'active': False,
      'endAt': getUtcDate(datetime.now()).strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    data, errors = self.gql.mutate(mutations.update_lock, variables)
    lock = __.get(data, 'result')
    queue_index = __.arrays.find_index(self.currentQueues, lambda q: q['name'] == queue_name)
    self.currentQueues[queue_index]['locks'].insert(0, lock)
    return __.get(data, 'successful')  # returns unlocking success status

  def runJob(self, job):
    # obtiene lock (if needed):
    lock = None
    if job["queue"]["lockRequired"]:
      lock = self.lockQueue(job["queue"]["name"])
    # Obtiene job
    fn_name, job_dict = self.getJobData(job)
    self.log(LogLevel.INFO, f"running {fn_name}")
    job_fn = job_dict['function']
    # Obtiene inputs
    if job['input']:
      try:
        if type(job['input']) == dict:
          kwargs = job['input']
        else:
          kwargs = json.loads(job['input']) # FALLBACK, attempt to load as a json-encoded string
      except JSONDecodeError as e:
        # falló al leer datos de input, aborta mision
        variables = {
          'id': int(job['id']),
          'status': 'ERROR',
          'output': f'Job input error: {str(e)}'
        }
        uploaders.update_job(variables)
        self.log(LogLevel.ERROR, e)
        return
    else:
      kwargs = job_dict
    # try to run job
    def update_this_job(variables):
      # * funcion de utilidad para actualizar job sin necesidad de conocer su ID
      status = variables.get('status')
      if not status:
        raise Exception('Missing "status" variable')
      # cast to status type to enforce an enumeration value
      status = JobStatus(status)
      # Extract string from enumeration
      safe_vars = {**variables, 'status': status.value}
      # this allows to specify ID inside job for backwards compatibility
      return uploaders.update_job({'id': job['id'], **safe_vars})
    # ! Inyecta a los kwargs el job que se está ejecutando:
    kwargs['job'] = job
    kwargs['job_id'] = job['id']
    kwargs['job']['update'] = update_this_job # couple of aliases for the same fn
    kwargs['update_job'] = update_this_job  # couple of aliases for the same fn
    # acceso directo a atributos del queue al que pertenece el job
    kwargs['queue'] = job['queue']
    kwargs['log'] = self.getProcessLoggerFunction(queue=job['queue'], job=job)
    kwargs['kwargs'] = {**kwargs}
    variables = {
      'id': int(job['id']),
      'queueName': job['queue']['name'],
      'status': 'RUNNING',
      'lastRunAt': getUtcDate(datetime.now()).strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    data, errors = self.gql.mutate(mutation=mutations.run_job, variables=variables)
    job_success = __.get(data, 'updateJob.successful')
    queue_success = __.get(data, 'updateQueue.successful')
    if job_success and queue_success:
      def safe_fn(**kwargs):
        try:
          job_fn(**kwargs)
        except TypeError as e:
          self.log(LogLevel.ERROR,
              f'Error starting job from queue {fn_name}:\n{str(e)}')
          self.log(LogLevel.ERROR,
              f'Did you forget to ignore additional params in the job definition?:')
          self.log(LogLevel.ERROR, f'@vw.job(...)')
          self.log(LogLevel.ERROR, f'def my_job(my_param, my_param2, **_) # <== can be **kwargs or **_')
          self.log(LogLevel.ERROR, f'\t...')
      p = self.context.Process(target=safe_fn, kwargs=(kwargs))
      self.log(LogLevel.INFO, f'started job with ID {job["id"]}')
      p.start()
      if lock:
        self.lockedJobs.append({
          'process': p,
          'job': job,
          'lock': lock
        })
    else:
      self.log(LogLevel.ERROR, f'Error starting job (queue={fn_name})')
  
  def queue_locked(self, queue_name):
    queues_by_name = __.group_by(self.currentQueues, 'name')
    current_queue = __.get(queues_by_name, f'{queue_name}.0')
    if not __.get(current_queue, 'lockRequired'):
      return False # Queue does not require locking
    return __.get(current_queue, 'locks.0.active') # locked if last lock is active

  def processJobs(self):
    jobs, errors = self.gql.query(queries.all_jobs, variables={'worker': self.worker['code']})
    if errors:
      message = errors[0]
      self.log(LogLevel.ERROR, f'Error! msg: {message}')
      return
    if jobs is not None and len(jobs) > 0:
      self.log(LogLevel.WARNING, f"Found {len(jobs)} jobs")
      for job in jobs:
        if self.queue_locked(job['queue']['name']):
          self.log(LogLevel.ERROR, f"{job['queue']['name']} is LOCKED, job aborted")
          self.abortJob(job)
        elif job['queue']['enabled']:
          self.runJob(job)
        else:
          self.log(LogLevel.WARNING, f"{job['queue']['name']} is DISABLED, skipping job")
    else:
      self.log(LogLevel.INFO, "Listening to events...")

  def abortStaleJobs(self):
    jobs, errors = self.gql.query(queries.waiting_jobs, variables={'worker': self.worker['code']})
    if (errors):
      self.log(LogLevel.ERROR, f'errors: {errors}')
    elif (len(jobs) > 0):
      self.log(LogLevel.ERROR, f'Deleting {len(jobs)} stale jobs:')
      for job in jobs:
        result, errors = self.gql.mutate(mutations.delete_job, {'id': job['id']})
        if (not errors):
          self.log(LogLevel.ERROR, f'deleted stale job {job["id"]}:')
        else:
          self.log(LogLevel.ERROR, f'errors deleting stale job: {errors}')

  def updateAvailableQueues(self):
    self.log(LogLevel.SUCCESS, 'Actualizando Jobs disponibles')
    for name, queue in self.queues.items():
      enabled = __.get(queue, 'enabled', None)
      description = __.get(queue, 'description', None)
      schedule = __.get(queue, 'schedule', None)
      query = __.get(queue, 'query', None)
      lockRequired = __.get(queue, 'lockRequired', None)
      variables = {
        'name':queue['name'],
        'alias':queue['alias'],
        'type': queue['type'],
      }
      # ! Add optional variables
      if enabled is not None:
        variables['enabled'] = enabled
      if description:
        variables['description'] = description
      if schedule:
        variables['schedule'] = schedule
      if query:
        variables['query'] = query
      if lockRequired:
        variables['lockRequired'] = lockRequired
      data, errors = self.gql.mutate(
        mutation=mutations.upsert_queue,
        variables=variables
      )
      if (errors):
        self.log(LogLevel.ERROR, f'Error actualizando Queue {name}.')
        self.log(LogLevel.ERROR, errors)
      else:
        self.log(LogLevel.SUCCESS, f'Queue {name} actualizado correctamente')

  def unlockFinishedJobs(self, force=False):
    unlocked = []
    for i, job_lock in enumerate(self.lockedJobs):
      if not job_lock['process'].is_alive() or force:
        if self.unlockQueue(job_lock['job']['queue']['name'], job_lock['lock']):
          self.log(LogLevel.SUCCESS, f'{job_lock["job"]["queue"]["name"]} UNLOCKED')
          unlocked.append(i)
        else:
          self.log(LogLevel.ERROR, f'error unlocking {job_lock["job"]["queue"]["name"]}')
    for u in unlocked:
      self.lockedJobs.pop(u)

  def runTimedOutEvents(self):
    current_time = time.time()
    for queue in self.eventQueues.values():
      if not queue['start_time'] or len(queue['mailbox']) == 0:
        continue  # nothing to run
      elapsed = current_time - queue['start_time']
      if elapsed >= queue['config']['timeout']:
        self.log(LogLevel.WARNING, f'Event {queue["name"]} timed out, running...')
        self.runEvent(queue['name'])
  
  def runFrequencyQueues(self):
    from pytz import timezone
    utc = timezone("UTC")
    queuesByType = __.group_by(self.currentQueues, 'type')
    freqQueues = __.get(queuesByType, 'FREQUENCY', default=[])
    # self.log(LogLevel.WARNING, f'checking {len(freqQueues)} frequency queues')
    for queue in freqQueues:
      # if it has never been ran, set the lastRunAt as a very old date (forces next run)
      lastRunAt = __.get(queue, 'lastRunAt', None)
      if not lastRunAt:
        lastRunDate = datetime(2000, 1, 1)
      else:
        lastRunDate = datetime.strptime(lastRunAt, "%Y-%m-%dT%H:%M:%SZ")
      lastRunDate = utc.localize(lastRunDate)
      now = getUtcDate(datetime.now())
      cron_iter = get_croniter(queue['schedule'], now)
      nextRunAt = [cron_iter.get_next(datetime) for _ in [0, 1]] # next and nexter dates
      #validate if next date is met:
      elapsedFromLastRun = (now - lastRunDate).total_seconds() / 60.0 # in minutes
      freq = (nextRunAt[1] - nextRunAt[0]).total_seconds() / 60.0 # in minutes
      if (elapsedFromLastRun > freq):
        # ! Run the frequency job!
        if (queue["enabled"]):
          self.gql.mutate(
            mutation=mutations.create_job,
            variables={
              'queueName': queue['name'],
              'worker': self.worker['code']
            }
          )
  
  def registerJobCreatedSubscription(self):
    """Registers JobCreated subscription that will call certain job when activated"""
    def runOnDemandJob(data):
      """Callback to run when job is created.
      It checks if the job corresponds to active worker or is a dummy subscription call
      """
      job = __.get(data, 'result')
      if not job:
        return # Possibly a job for another worker
      if self.queue_locked(job['queue']['name']):
        self.log(LogLevel.ERROR, f"{job['queue']['name']} is LOCKED, job aborted")
        self.abortJob(job)
      elif job['queue']['enabled']:
        self.runJob(job)
      else:
        self.log(LogLevel.WARNING, f"{job['queue']['name']} is DISABLED, skipping job")

    self.unsubJobCreated = self.gql.subscribe(
      query=subscriptions.JOB_CREATED,
      variables={'workerCode': self.worker['code']},
      callback=runOnDemandJob)
    if (self.unsubJobCreated):
      self.log(LogLevel.SUCCESS, 'SUBSCRIBED TO JOB CREATIONS')
    else:
      self.log(LogLevel.ERROR, 'ERROR SUBSCRIBING TO JOB CREATIONS')
  
  def runEvent(self, queue_name):
    queuesByName = __.group_by(self.currentQueues, 'name')
    currentQueue = __.get(queuesByName, f'{queue_name}.0')
    if self.queue_locked(currentQueue['name']):
      self.log(LogLevel.WARNING, f"{currentQueue['name']} is LOCKED, event postponed")
      return
    elif not currentQueue['enabled']:
      self.log(LogLevel.WARNING, f'Event triggered for {queue_name} but Queue not enabled, skipping...')
      return
    data = self.eventQueues[queue_name]["mailbox"]
    # ! try to run job
    # obtiene lock (if needed):
    lock = None
    if currentQueue["lockRequired"]:
      lock = self.lockQueue(currentQueue["name"])
    # Crea job asociado a evento
    response, errors = self.gql.mutate(
        mutation=mutations.run_event_job,
        variables={
            'queueName': queue_name,
            'worker': self.worker['code'],
            'lastRunAt': getUtcDate(datetime.now()).strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    )
    if errors:
      self.log(LogLevel.ERROR, f'Error starting event:\n{errors}')
      return
    job = __.get(response, 'job.result')
    def update_this_job(variables):
      # * funcion de utilidad para actualizar job sin necesidad de conocer su ID
      status = variables.get('status')
      if not status:
        raise Exception('Missing "status" variable')
      # cast to status type to enforce an enumeration value
      status = JobStatus(status)
      # Extract string from enumeration
      safe_vars = {**variables, 'status': status.value}
      # this allows to specify ID inside job for backwards compatibility
      return uploaders.update_job({'id': job['id'], **safe_vars})
    # ! Inyecta a los kwargs el job que se está ejecutando:
    kwargs = {
      'job_id': job['id'],
      'job': {**job, 'update': update_this_job},
      'update_job': update_this_job,
      'queue': currentQueue,
      'data': data,
      'log': self.getProcessLoggerFunction(queue=currentQueue, job=job)
    }
    kwargs['kwargs'] = {**kwargs}
    def safe_fn(**kwargs):
      try:
        self.eventQueues[queue_name]['function'](**kwargs)
      except TypeError as e:
        self.log(LogLevel.ERROR, f'Error starting job from queue {queue_name}:\n{str(e)}')
        self.log(LogLevel.ERROR, f'Did you forget to ignore additional params in the job definition?:')
        self.log(LogLevel.ERROR, f'@vw.job(...)')
        self.log(LogLevel.ERROR, f'def my_job(my_param, my_param2, **_) # <== can be **kwargs or **_')
        self.log(LogLevel.ERROR, f'\t...')
    p = self.context.Process( target=safe_fn, kwargs=(kwargs))
    p.start()
    if lock:
      self.lockedJobs.append({
        'process': p,
        'job': {**job, 'queue': {**currentQueue}},
        'lock': lock
      })
    # Move mailbox data and clear it
    self.eventQueues[queue_name]["mailbox"] = []
    self.eventQueues[queue_name]["start_time"] = None # Clear timeout

  def registerEventJobs(self):
    queuesByType = __.group_by(self.queues.values(), 'type')
    eventQueues = __.get(queuesByType, 'EVENT', default=[])
    for queue in eventQueues:
      def onEventTriggered(data):
        """Callback to execute on every event triggered of the same type.
        This callback performs a check to know if enough data (or time)
        has elapsed and thus the Job has to be executed with the current chunk of data
        
        Parameters
        ----------
        data : any
            Data received from the event
        """
        if len(self.eventQueues[queue["name"]]["mailbox"]) == 0:
          self.log(LogLevel.WARNING, f'EVENT { queue["name"] } TRIGGERED, BUILDING BATCH')
          self.eventQueues[queue["name"]]["start_time"] = time.time()
        self.eventQueues[queue["name"]]["mailbox"].append(data)
        if len(self.eventQueues[queue["name"]]["mailbox"]) >= self.eventQueues[queue["name"]]['config']['max_batch']:
          """Run event only if event surpassed the upper data limit"""
          self.runEvent(queue["name"])
      unsub = self.gql.subscribe(query=queue['query'], callback=onEventTriggered)
      if (unsub):
        self.log(LogLevel.SUCCESS, f'REGISTERED LISTENER FOR EVENT QUEUE { queue["name"] }')
      else:
        self.log(LogLevel.ERROR, f'ERROR REGISTERING LISTENER FOR EVENT QUEUE { queue["name"] }')

  def getProcessLoggerFunction(self, queue=None, job=None):
    """Logs to STDOUT formatted to help get helpful information
    
    Parameters
    ----------
    queue : int, optional
      ID for the queue sending this message, by default 0
    job : int, optional
      ID for the job sending this message, by default 0
    """
    job_zero_padding = len(str(__.get(self.worker, 'jobs.0.id')))
    W = str(self.worker["id"]).zfill(2) # no need to pass as argument, will always be the same
    Q = str(__.get(queue, 'id', 0)).zfill(3)
    J = str(__.get(job, 'id', 0)).zfill(job_zero_padding)
    log_queue_key = __.get(queue, 'name', 'main')
    log_queue = self.logQueues[log_queue_key]
    if self.loggingStyle == LogStyle.PREFIX_ALL_LINES:
      def sendLogToQueue(level, message):
        D = getUtcDate(datetime.now()).strftime("%Y-%m-%dT%H:%M:%SZ")
        msgs = message.split('\n')
        for msg in msgs:
          log_queue.put({
            'level': level,
            'content': f'[D={D}/W={W}/Q={Q}/J={J}] - {msg}'
          })
    else:
      def sendLogToQueue(level, message):
        D = getUtcDate(datetime.now()).strftime("%Y-%m-%dT%H:%M:%SZ")
        log_queue.put({
            'level': level,
            'content': f'[D={D}/W={W}/Q={Q}/J={J}] - {message}'
        })
    return sendLogToQueue

  def startLoggingLoop(self):
    self.log = self.getProcessLoggerFunction()
    # FN DEFINITION --------------------------
    def loggingLoop():
      while not self.stopLogging:
        # * check mailbox for every queue
        # * log as many messages from same queue as possible
        # TODO: May set a limit to this, in message count or timeout for other queues)
        # ! Send messages to log-upload queue
        # ! flag as CREATE or UPSERT for retention or real-time visualization only
        for _, log_queue in self.logQueues.items():
          while not log_queue.empty():
            msg = log_queue.get()
            log(msg['level'], msg['content'])
      self.log(LogLevel.WARNING, 'Logging loop stopped')
    # END FN DEFINITION --------------------------
    # Create Queues for each queue:
    for queue_name, _ in self.queues.items():
      self.logQueues[queue_name] = SimpleQueue()
    self.loggingProcess = self.context.Process(target=loggingLoop)
    self.loggingProcess.start()
    self.log(LogLevel.SUCCESS, 'Logging loop started')

  def stopLoggingLoop(self):
    self.stopLogging = True
    self.loggingProcess.join()

  def eventLoop(self, interval=1.0):
    try:
      currentQueues, errors = self.gql.query(queries.all_queues)
      if (errors):
        self.log(LogLevel.ERROR, f'errors: {errors}')
        return
      self.currentQueues = currentQueues
      self.unlockFinishedJobs()
      self.runFrequencyQueues()
      self.runTimedOutEvents()
      # TODO: sendReminders(queues)
      if self.pollingMode == PollingMode.QUERY:
        self.processJobs()
      else:
        self.log(LogLevel.INFO, 'Listening to events...')
    except Exception as e:
      self.log(LogLevel.ERROR, f"Error in worker's event loop!")
      self.log(LogLevel.ERROR, f'e: {e}')
    time.sleep(interval)
  
  def getWorker(self):
    worker, errors = self.gql.query_one(
      queries.get_worker,
      {'code': self.worker_code}
    )
    if errors:
      log(LogLevel.ERROR, errors)
      raise Exception('Worker not found')
    self.worker = worker

  def run(self, interval=1.0):
    self.context = mp.get_context('fork')
    self.getWorker()
    self.startLoggingLoop()
    self.abortStaleJobs()
    self.updateAvailableQueues()
    if (self.pollingMode == PollingMode.SUBSCRIPTION):
      self.registerJobCreatedSubscription()
    self.registerEventJobs()
    while 1:
      try:
        self.eventLoop(interval=interval)
      except KeyboardInterrupt:
        self.log(LogLevel.WARNING, "\nuser's stop signal, exiting...")
        self.stopLoggingLoop()
        self.unlockFinishedJobs(force=True)
        self.gql.close()
        break
