import importlib.util
import os
import unittest
from pathlib import Path
from unittest import mock


def load_invoke_command_module():
    repo_root = Path(__file__).resolve().parents[2]
    module_path = repo_root / ".github" / "PRPs" / "scripts" / "invoke_command.py"
    spec = importlib.util.spec_from_file_location("invoke_command", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


ic = load_invoke_command_module()


class TestInvokeCommandAdapter(unittest.TestCase):
    def setUp(self):
        self.orig_env = dict(os.environ)

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.orig_env)

    def test_get_adapter_default(self):
        os.environ.pop("PRP_TOOL_ADAPTER", None)
        self.assertEqual(ic.get_adapter(), "claude")

    def test_get_adapter_invalid_fallback(self):
        os.environ["PRP_TOOL_ADAPTER"] = "unknown"
        self.assertEqual(ic.get_adapter(), "claude")

    @mock.patch.object(ic.subprocess, "run")
    def test_invoke_command_copilot_mode(self, mock_run):
        os.environ["PRP_TOOL_ADAPTER"] = "copilot"

        tmp_file = Path("temp_test_command.md")
        tmp_file.write_text("Test $ARGUMENTS")

        try:
            ic.invoke_command(command_path=tmp_file, arguments="hello", interactive=False)
            self.assertTrue(mock_run.called)
            called = mock_run.call_args[0][0]
            # should invoke the Copilot adapter script path
            self.assertIn("invoke_copilot.py", " ".join(str(x) for x in called))
        finally:
            tmp_file.unlink()


if __name__ == "__main__":
    unittest.main()
