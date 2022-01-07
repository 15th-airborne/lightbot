from plugins.battle.models import Player

p1 = Player.get(user_id=123, group_id=244)
p2 = Player.get(user_id=12323, group_id=244)

