
from .teacher import TeachPlugin, AskPlugin
from plugin_manager import all_plugins

all_plugins.append(TeachPlugin)
all_plugins.append(AskPlugin)

