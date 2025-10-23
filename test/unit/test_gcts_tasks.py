import pytest
from unittest.mock import MagicMock, patch
from sap.cli.gcts_tasks import GCTSTaskEngine, GCTSTaskError

class DummyTask:
    class TaskStatus:
        FINISHED = type('Enum', (), {'value': 'FINISHED'})
        ABORTED = type('Enum', (), {'value': 'ABORTED'})
    def __init__(self, tid, status):
        self.tid = tid
        self.rid = 'RID'
        self.type = 'CLONE'
        self.status = status
        self.TaskStatus = DummyTask.TaskStatus

class DummyRepo:
    def __init__(self, task):
        self._task = task
        self.rid = 'RID'
    def schedule_clone(self):
        return self._task
    def get_task_by_id(self, tid):
        return self._task

@patch('sap.cli.gcts_tasks.get_console')
def test_schedule_clone_task(mock_console):
    engine = GCTSTaskEngine(connection=MagicMock())
    repo = DummyRepo(DummyTask('TID1', 'FINISHED'))
    task = engine.schedule_clone_task(repo)
    assert task.tid == 'TID1'
    assert task.status == 'FINISHED'

@patch('sap.cli.gcts_tasks.get_console')
def test_wait_for_task_finished(mock_console):
    engine = GCTSTaskEngine(connection=MagicMock())
    repo = DummyRepo(DummyTask('TID2', 'FINISHED'))
    task = engine.wait_for_task(repo, 'TID2', wait_for_ready=1, pull_period=0)
    assert task.status == 'FINISHED'

@patch('sap.cli.gcts_tasks.get_console')
def test_wait_for_task_aborted(mock_console):
    engine = GCTSTaskEngine(connection=MagicMock())
    repo = DummyRepo(DummyTask('TID3', 'ABORTED'))
    with pytest.raises(GCTSTaskError):
        engine.wait_for_task(repo, 'TID3', wait_for_ready=1, pull_period=0)

@patch('sap.cli.gcts_tasks.get_console')
def test_wait_for_task_timeout(mock_console):
    class SlowRepo(DummyRepo):
        def __init__(self, task):
            super().__init__(task)
            self.rid = 'RID4'
        def get_task_by_id(self, tid):
            # Always return a non-terminal status
            t = DummyTask(tid, 'RUNNING')
            t.TaskStatus = DummyTask.TaskStatus
            return t
    engine = GCTSTaskEngine(connection=MagicMock())
    repo = SlowRepo(DummyTask('TID4', 'RUNNING'))
    with pytest.raises(GCTSTaskError):
        engine.wait_for_task(repo, 'TID4', wait_for_ready=0.1, pull_period=0)
