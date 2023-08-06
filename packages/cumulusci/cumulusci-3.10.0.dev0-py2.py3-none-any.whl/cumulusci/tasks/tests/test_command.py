""" Tests for the Command tasks """

from unittest import mock
import unittest
from io import BytesIO

from testfixtures.popen import MockPopen
from testfixtures import Replacer

from cumulusci.core.config import BaseGlobalConfig
from cumulusci.core.config import BaseProjectConfig
from cumulusci.core.config import OrgConfig
from cumulusci.core.config import TaskConfig
from cumulusci.core.tests.utils import MockLoggerMixin

from cumulusci.tasks.command import Command
from cumulusci.tasks.command import SalesforceCommand
from cumulusci.tasks.command import CommandException


class TestCommandTask(MockLoggerMixin, unittest.TestCase):
    """ Tests for the basic command task """

    def setUp(self):
        self.global_config = BaseGlobalConfig()
        self.project_config = BaseProjectConfig(
            self.global_config, config={"noyaml": True}
        )
        self.task_config = TaskConfig()
        self._task_log_handler.reset()
        self.task_log = self._task_log_handler.messages

    def test_functional_run_ls(self):
        """ Functional test that actually subprocesses and runs command.

        Checks that command either ran successfully or failed as expected
        so that it can be run on any platform. Other tests will mock
        the subprocess interaction.
        """

        self.task_config.config["options"] = {"command": "ls -la"}

        task = Command(self.project_config, self.task_config)

        # try to run the command and handle the command Exception
        # if no exception, confirm that we logged
        # if exception, confirm exception matches expectations
        try:
            task()
        except CommandException:
            self.assertTrue(any("Return code" in s for s in self.task_log["error"]))

        self.assertTrue(any("total" in s for s in self.task_log["info"]))

    def test_init__json_env(self):
        task_config = TaskConfig({"options": {"env": "{}", "command": "ls"}})
        task = Command(self.project_config, task_config)
        self.assertEqual({}, task.options["env"])

    def test_init__dict_env(self):
        task_config = TaskConfig({"options": {"env": {}, "command": "ls"}})
        task = Command(self.project_config, task_config)
        self.assertEqual({}, task.options["env"])

    def test_get_env__pass_env_false(self):
        task_config = TaskConfig({"options": {"pass_env": "False", "command": "ls"}})
        task = Command(self.project_config, task_config)
        self.assertEqual({}, task._get_env())

    def test_handle_returncode(self):
        task_config = TaskConfig({"options": {"command": "ls"}})
        task = Command(self.project_config, task_config)
        with self.assertRaises(CommandException):
            task._handle_returncode(1, BytesIO(b"err"))


class TestCommandTaskWithMockPopen(MockLoggerMixin, unittest.TestCase):
    """ Run command tasks with a mocked popen """

    def setUp(self):
        self.global_config = BaseGlobalConfig()
        self.project_config = BaseProjectConfig(
            self.global_config, config={"noyaml": True}
        )
        self.task_config = TaskConfig()

        self._task_log_handler.reset()
        self.task_log = self._task_log_handler.messages

        self.Popen = MockPopen()
        self.r = Replacer()
        self.r.replace("cumulusci.tasks.command.subprocess.Popen", self.Popen)
        self.addCleanup(self.r.restore)

    def test_functional_mock_command(self):
        """ Functional test that runs a command with mocked
        popen results and checks the log.
        """

        self.task_config.config["options"] = {"command": "ls -la"}

        self.Popen.set_command("ls -la", stdout=b"testing testing 123", stderr=b"e")

        task = Command(self.project_config, self.task_config)
        task()

        self.assertTrue(any("testing testing" in s for s in self.task_log["info"]))


class TestSalesforceCommand(unittest.TestCase):
    def setUp(self):
        self.global_config = BaseGlobalConfig()
        self.project_config = BaseProjectConfig(
            self.global_config, config={"noyaml": True}
        )
        self.task_config = TaskConfig({"options": {"command": "ls"}})
        self.org_config = OrgConfig(
            {"access_token": "TOKEN", "instance_url": "https://na01.salesforce.com"},
            "test",
        )
        self.org_config.refresh_oauth_token = mock.Mock()

    def test_update_credentials(self):
        task = SalesforceCommand(self.project_config, self.task_config, self.org_config)
        task()
        self.org_config.refresh_oauth_token.assert_called_once()

    def test_get_env(self):
        task = SalesforceCommand(self.project_config, self.task_config, self.org_config)
        env = task._get_env()
        self.assertIn("SF_ACCESS_TOKEN", env)
        self.assertIn("SF_INSTANCE_URL", env)
