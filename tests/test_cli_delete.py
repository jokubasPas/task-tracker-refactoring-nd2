import os
import tempfile
import unittest
from argparse import Namespace
from unittest.mock import patch

from tasktracker import task_tracker
from tasktracker.tasks import Manager


class TestDeleteCommand(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        path = os.path.join(self.temp_dir.name, "tasks.json")
        self.manager = Manager(path)
        self.task = self.manager.add_task("Test task")

        self.patcher = patch.object(
            task_tracker, "manager", self.manager
        )
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.temp_dir.cleanup()

    def test_delete_confirmed(self):
        with patch.object(
            task_tracker, "_confirm_delete", return_value=True
        ), patch.object(
            task_tracker.pretty_print, "print_by_tasks_command"
        ) as output:
            task_tracker._handle_delete_command(
                Namespace(task_index=self.task.index)
            )

        self.assertEqual(len(self.manager.tasks), 0)
        output.assert_called_once_with("delete", task=self.task)

    def test_delete_cancelled(self):
        with patch.object(
            task_tracker, "_confirm_delete", return_value=False
        ):
            task_tracker._handle_delete_command(
                Namespace(task_index=self.task.index)
            )

        self.assertEqual(len(self.manager.tasks), 1)

    def test_delete_nonexistent(self):
        with patch.object(
            task_tracker, "_confirm_delete"
        ) as confirm:
            task_tracker._handle_delete_command(
                Namespace(task_index=999)
            )

        confirm.assert_not_called()
        self.assertEqual(len(self.manager.tasks), 1)