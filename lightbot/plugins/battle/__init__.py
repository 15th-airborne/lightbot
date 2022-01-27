
from .battle import (
    CheckStatusPlugin, 
    AttackSomeonePlugin, 
    ShowMarketPlugin,
    SignPlugin,
    BuyPlugin,
    LuckDrawPlugins,
    EatPlugins,
)

from plugin_manager import all_plugins

all_plugins.append(CheckStatusPlugin)
all_plugins.append(AttackSomeonePlugin)
all_plugins.append(ShowMarketPlugin)
all_plugins.append(SignPlugin)
all_plugins.append(BuyPlugin)
all_plugins.append(LuckDrawPlugins)
all_plugins.append(EatPlugins)
