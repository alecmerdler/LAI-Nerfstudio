import os

from lightning import LightningApp, LightningFlow
from lightning.app.frontend import StaticWebFrontend

from theia.components.trainer import Trainer


class WebFrontend(LightningFlow):
    def configure_layout(self):
        return StaticWebFrontend(os.path.join(os.path.dirname(__file__), "theia", "ui", "build"))


class NerfstudioApp(LightningFlow):
    def __init__(self):
        super().__init__()

        self.frontend = WebFrontend()
        self.trainer = Trainer()

    def configure_layout(self):
        return [{"name": "home", "content": self.frontend}]

    def run(self):
        self.trainer.run()


app = LightningApp(NerfstudioApp())
