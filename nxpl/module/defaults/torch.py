from torch import nn

from nxpl.config import Config


class Conv2d(nn.Conv2d):
    def from_config(self, config: Config):
        pass
