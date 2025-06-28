"""Stateful runner that explicitly manages model lifecycle for inference calls"""

from app.types import ModelConfig
from app.models.model_instance import ModelInstance
from app.exceptions import ModelLoadError, to_http_exception


class ModelRunner:
    def __init__(self, config: ModelConfig):
        self.config = config
        self.model_instance = None

    def start_model(self):
        if not self.model_instance:
            self.model_instance = ModelInstance(self.config)
            self.model_instance.run_warm_up()

    def get_response(self, prompt: str) -> str:
        if not self.model_instance:
            raise to_http_exception(ModelLoadError())
        return self.model_instance.get_response(prompt)

    def stop_model(self):
        if self.model_instance:
            self.model_instance.shutdown()
            self.model_instance = None
