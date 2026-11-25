import asyncio
import importlib
import json
from pathlib import Path
import sys
import types
from unittest import TestCase
from unittest.mock import patch


class HostTest(TestCase):
    def test_native_tool_registration_and_query(self):
        package = types.ModuleType("ace_music_plugin")
        package.__path__ = [str(Path(__file__).resolve().parents[1])]
        sys.modules[package.__name__] = package
        module = importlib.import_module("ace_music_plugin.main")
        tools = [
            name for name in vars(module.AceMusicPlugin) if name.startswith("acemusic_")
        ]
        self.assertEqual(len(tools), 9)
        plugin = module.AceMusicPlugin(None, {"api_key": "fixture"})
        with patch.object(
            module, "invoke", return_value={"id": "saved", "state": "pending"}
        ) as invoke:
            output = asyncio.run(plugin.acemusic_retrieve(None, "saved"))
        self.assertEqual(json.loads(output)["id"], "saved")
        invoke.assert_called_once_with("fixture", "retrieve", {"task_id": "saved"})
