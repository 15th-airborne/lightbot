todo

版本 >= python3.8

后台运行
```
nohup python bot.py >/dev/null &
```

- plugins 文件夹放各种插件
- bot.py 是主文件

> 代码还在疯狂施工中...

### 功能

- 确实：当群友发言中带有“**确实**”这两个字时，小月也会回复一个确实避免冷场。
- 骂鱼哥：发送**骂鱼哥**时，会骂鱼哥
- 揍傻6：发送揍+@傻6时，会揍傻6
- 教小月：作为一名高质量人工智能，自然是要会学习的。发送`教小月 问题 答案`可以教小月
- sur色图：会发sur的色图。


### 更新
2022-01-24
- 修复了不能买活的BUG
- 修复了显示要120秒复活，实际上只要60秒复活的BUG
- 现在不能夯自己了
- 现在每天生命值都会回满了
- 买活价格增加至50g
- 复活时间由60增秒加至7200秒

2022-01-21
- 更新了使用枪的功能
- 更新了双击功能，双击可以获得随机黄金以及固定了生命上限和攻击力提升
- 揍死人可以获得G了

2022-01-13
- 修复了叠buff
- 重构了代码，删掉了会导致叠buff的功能


#### 不关键的记录

插件触发的类型搞成这几种

最基本的
- 匹配开头：以空格分隔多个参数
- 关键词匹配：关键词出现在句子中就算
- 特殊匹配