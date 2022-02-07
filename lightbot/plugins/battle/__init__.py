
from .battle import (
    CheckStatusPlugin,
    GoodsStatusPlugin,
    AttackSomeonePlugin, 
    ShowMarketPlugin,
    SignPlugin,
    BuyPlugin,
    EatPlugins,
)

from .lottery import LotteryPlugin

from plugin_manager import all_plugins

all_plugins.append(CheckStatusPlugin)
all_plugins.append(GoodsStatusPlugin)
all_plugins.append(AttackSomeonePlugin)
all_plugins.append(ShowMarketPlugin)
all_plugins.append(SignPlugin)
all_plugins.append(BuyPlugin)
all_plugins.append(EatPlugins)

all_plugins.append(LotteryPlugin)


