import subprocess
from dataclasses import dataclass
from pathlib import Path

from lightning import BuildConfig, CloudCompute, LightningWork


@dataclass
class CustomBuildConfig(BuildConfig):
    def build_commands(self):
        return [
            "sudo apt-get update",
            "sudo apt-get install python3-opencv",
        ]


class Trainer(LightningWork):
    def __init__(self):
        super().__init__(
            cloud_compute=CloudCompute("gpu"),
            cloud_build_config=CustomBuildConfig(
                requirements=["git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch"]
            ),
        )

    def download_data(self):
        data_path = Path("data")
        if data_path.exists():
            return

        subprocess.call("ns-download-data --dataset=nerfstudio --capture=poster", shell=True)

    def train(self):
        subprocess.call("ns-train nerfacto --vis=viewer ", shell=True)

    def run(self):
        self.download_data()
        self.train()
