"""
SAPCLI gCTS tasks module: scheduling, polling, and status/error handling for gCTS tasks.
"""

import json
import time
from sap.rest.errors import HTTPRequestError
from sap.cli.core import get_console

class GCTSTaskError(Exception):
    pass

class GCTSTaskEngine:
    def __init__(self, connection):
        self.connection = connection

        def schedule_clone_task(self, repo_or_id, use_repoid=False):
            """
            Schedule a clone task for the given repository or repository id. Returns a RepositoryTask object or None.
            """
            if use_repoid:
                from sap.rest.gcts.remote_repo import Repository
                repo = Repository(self.connection, repo_or_id)
            else:
                repo = repo_or_id
            return repo.schedule_clone()

    def wait_for_task(self, repo, task_id, wait_for_ready, pull_period):
        """
        Polls the gCTS task until it finishes or aborts, or times out.
        Returns the final RepositoryTask object or raises GCTSTaskError.
        """
        console = get_console()
        start_time = time.time()
        while time.time() - start_time < wait_for_ready:
            try:
                task = repo.get_task_by_id(task_id)
                filtered_task_info = {
                    'tid': task.tid,
                    'rid': task.rid,
                    'type': task.type,
                    'status': task.status
                }
                console.printout('\n', 'Task monitoring:', json.dumps(filtered_task_info, indent=4))
                if task.status == task.TaskStatus.FINISHED.value:
                    return task
                if task.status == task.TaskStatus.ABORTED.value:
                    raise GCTSTaskError(f'Task execution aborted: task {task_id} for repository {repo.rid}')
            except HTTPRequestError:
                pass
            time.sleep(pull_period)
        raise GCTSTaskError(f'Waiting for the task execution timed out: task {task_id} for repository {repo.rid}.')
