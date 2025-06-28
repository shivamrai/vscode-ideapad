"""
Unit tests for the Model Runner class.
"""

import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from model_runner import ModelRunner
from app.types import ModelConfig
from app.exceptions import InvalidPromptError
import tempfile

# Create a temporary file to mock a model file for testing.
with tempfile.NamedTemporaryFile(delete=False) as tmp:
    DUMMY_MODEL_PATH = Path(tmp.name)


# The test class for ModelRunner in the main code.
class TestModelRunner(unittest.TestCase):
    def setUp(self):
        self.config = ModelConfig(
            model_path=DUMMY_MODEL_PATH,
            n_ctx=2048,
            model_tokens=100,
            temperature=0.7,
            top_p=1.0,
            top_k=40,
            repeat_penalty=1.1,
            repeat_last_n=64,
            num_threads=4,
            num_predict=128,
        )
        self.runner: ModelRunner = ModelRunner(self.config)

    @patch("model_runner.ModelRunner.run_warm_up")
    def test_start_model(self, mock_run_warm_up: MagicMock):
        self.runner.start_model()
        mock_run_warm_up.assert_called_once_with()

    @patch("model_runner.ModelRunner.get_response")
    def test_get_response(self, mock_get_response: MagicMock):
        mock_get_response.return_value = "Test response"
        response = self.runner.get_response("Test prompt")
        self.assertEqual(response, "Test response")

    @patch("Model_runner.ModelRunner.shutdown")
    def test_stop_model(self, mock_shutdown: MagicMock):
        self.runner.stop_model()
        mock_shutdown.assert_called_once()

    def test_invalid_prompt(self):
        with self.assertRaises(InvalidPromptError):
            self.runner.get_response(
                ""
            )  # Assuming empty prompt raises InvalidPromptError
