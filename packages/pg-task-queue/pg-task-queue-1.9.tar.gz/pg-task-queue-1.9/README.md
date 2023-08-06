#### Add task example
```python
from pg_tasks_queue.TaskManager import TaskManager
task_manager = TaskManager()
database_dict = {'host': '127.0.0.1',
                 'port': '5432',
                 'dbname': 'task_queue',
                 'schema': 'public',
                 'user': '<user_login>',
                 'password': '<user_password>'}
if task_manager.init(database_dict):
    task_dict = {'module': '<module_name>',
                 'func': '<function_name>',
                 'priority': 1, 
                 'params': {'counter': 3}, 
                 'max_retry_count': 3}
    task_id = task_manager.add_task(task_dict)
```
#### Init task with external connection
In this case external connection not closed
```python
task_manager.init(database_dict, connection=external_connection)
```
#### Start worker example
```python
from pg_tasks_queue.Worker import Worker
worker = Worker()
config_dict = {
    'database': {'host': '127.0.0.1',
                 'port': '5432',
                 'dbname': 'task_queue',
                 'schema': 'public',
                 'user': '<user_login>',
                 'password': '<user_password>'},
    'worker': {'timeout_sec': 30., 'sleep_sec': .5}
}
if worker.init(config_dict):
    worker.start()
```
#### Init worker with keeping connection alive (default=False)
```python
worker.init(config_dict, keep_connection=True)
```
#### Init worker with external connection
In this case external connection not closed
```python
worker.init(config_dict, connection=external_connection)
```
#### Init worker with different process types
By the definition process_type=None
- process_type=None: 
    - worker starting in the same thread as main process;
    - separate thread for worker not created; 
    - after timeout main process exit with signal.SIGINT.
- process_type='fork': 
    - worker starting in fork;
    - after timeout worker termenate and main process not stopped.
- process_type='thread': 
    - worker starting in the same thread as main process;
    - separate thread for worker is created; 
    - after timeout main process exit with sys.exit(1).
- process_type='kthread': 
    - worker starting in the same thread as main process;
    - separate thread for worker is created; 
    - after timeout worker termenate and main process not stopped.
```python
worker.init(config_dict, process_type='fork')
```
