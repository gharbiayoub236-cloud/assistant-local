import unittest
from types import SimpleNamespace
from unittest.mock import patch
import main


class Message:
    def __init__(self, content="", calls=None):
        self.content = content
        self.tool_calls = calls
    def model_dump(self, **kwargs):
        return {"role": "assistant", "content": self.content, "tool_calls": self.tool_calls}


class AssistantTests(unittest.TestCase):
    def test_path_escape_rejected(self):
        with self.assertRaises(ValueError):
            main.chemin("../secret.txt")

    def test_tool_results_are_returned_to_model(self):
        call = SimpleNamespace(function=SimpleNamespace(name="test", arguments={"value": "ok"}))
        responses = iter([
            SimpleNamespace(message=Message(calls=[call])),
            SimpleNamespace(message=Message(content="terminé")),
        ])
        received = []
        def chat(**kwargs):
            received.append(list(kwargs["messages"]))
            return next(responses)
        messages = [{"role": "user", "content": "test"}]
        with patch.dict(main.TOOLS, {"test": lambda value: value}):
            result = main.repondre(messages, SimpleNamespace(chat=chat), "fake")
        self.assertEqual(result, "terminé")
        self.assertEqual(received[1][-1], {"role": "tool", "tool_name": "test", "content": "ok"})

    def test_tool_loop_is_bounded(self):
        call = SimpleNamespace(function=SimpleNamespace(name="inconnu", arguments={}))
        client = SimpleNamespace(chat=lambda **kwargs: SimpleNamespace(message=Message(calls=[call])))
        messages = []
        self.assertIn("Limite", main.repondre(messages, client, "fake"))
        self.assertEqual(len(messages), 16)


if __name__ == "__main__":
    unittest.main()
