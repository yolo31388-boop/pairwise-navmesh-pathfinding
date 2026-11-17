# pairwise-navmesh-pathfinding

NPC 追玩家时贴着墙角走，遇到 U 形障碍就原地打转，绕过墙之后还要在拐点停顿一下，一群人追同一个目标时挤成一团互相穿插。查下来是 ai/navmesh.py 的寻路有严重问题：heuristic() 用曼哈顿距离，八方向移动的代价估得偏高，A* 扩展大量无用节点；astar() 根本不搜，直接把起点终点连成直线，墙和边界全都不管；line_of_sight() 恒返回真，隔着墙也认为能直达；smooth_path() 每隔一个点丢一个，拐角全被抹掉；path_cost() 按点数算长度，对角线代价完全不对；tile_index() 用截断取整，负坐标全落到 0 号格；tile_neighbors() 固定返回八邻域，边界格返回越界坐标；avoidance_velocity() 恒返回零向量，单位重叠也不分离。你要修的是：启发式用八方向 octile 距离；A* 做八方向搜索、检查边界和墙、禁止贴角穿越；视线检测按格子采样；平滑只删共线点、保留拐角；路径代价按欧氏长度累加；瓦片索引向下取整；邻域只返回格内四邻；避障按距离加权产生分离速度。ai/navmesh.py 是核心，tests/test_navmesh.py 15个红。

## 运行

```
python -m pytest tests -q
```

初始状态：15 个用例失败。修复实现使全部用例通过，不要修改 `tests/` 下的测试。
