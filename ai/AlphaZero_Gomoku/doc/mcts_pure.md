# MCTS基本原理

蒙特卡洛树搜索（MCTS）仅展开根据 UCB 公式所计算过的节点，并且会采用一种自动的方式对性能指标好的节点进行更多的搜索。具体步骤概括如下：

1. 由当前局面建立根节点，生成根节点的全部子节点，分别进行模拟对局；
2. 从根节点开始，进行最佳优先搜索；
3. 利用 UCB 公式计算每个子节点的 UCB 值，选择最大值的子节点；
4. 若此节点不是叶节点，则以此节点作为根节点，重复 2；
5. 直到遇到叶节点，如果叶节点未曾经被模拟对局过，对这个叶节点模拟对局；否则为这个叶节点随机生成子节点，并进行模拟对局；
6. 将模拟对局的收益（一般胜为 1 负为 0）按对应颜色更新该节点及各级祖先节点，同时增加该节点以上所有节点的访问次数；
7. 回到 2，除非此轮搜索时间结束或者达到预设循环次数；
8. 从当前局面的子节点中挑选平均收益最高的给出最佳着法。

由此可见 UCT 算法就是在设定的时间内不断完成从根节点按照 UCB 的指引最终走到某一个叶节点的过程。而算法的基本流程包括了选择好的分支（Selection）、在叶子节点上扩展一层（Expansion）、模拟对局（Simulation）和结果回馈（Backpropagation）这样四个部分。
UCT 树搜索还有一个显著优点就是可以随时结束搜索并返回结果，在每一时刻，对 UCT 树来说都有一个相对最优的结果。
------------------------------------------------------------------------------------------
# Treenode类 蒙特卡洛树的节点
## 属性    
1.  父节点：     self._parent = parent
2.  孩子节点：   self._children = {}  # a map from action to TreeNode

3.  self._n_visits = 0 :总访问次数： 
4.  self._Q = 0 : 总模拟收益,或者类似评分 
每个访问过的节点都需要维护这两个值。换句话说，如果你随机找一个节点，这个节点的统计信息反映了它多大可能是最佳下一步（总模拟收益），以及它被访问的频率（总访问次数）。收益高的节点是接下来探索的优秀候选节点，但那些访问次数低的节点也同样值得关注（因为它没有被探索完全）

5.        self._u = 0
6.        self._P = prior_p

## 方法
1. expand(self, action_priors)    ：expansion:除非该节点游戏结束，新扩展一个节点
2. select(self, c_puct)           : select:选择一个最优的子节点
    2.1 get_value(self, c_puct)
    
3. update_recursive(self, leaf_value) ：Backpropagation:反向传播
    3.1 update(self, leaf_value)            
5. is_leaf(self)
6. is_root(self)  

# MCTS类
## 属性
1. self._root = TreeNode(None, 1.0)：根节点
2. self._c_puct = c_puct
3. self._n_playout = n_playout ：规划局数，每次模拟的局树，也有场合直接使用时间在控制模拟次数。

## 方法
1. _playout(self, state)          :Simulation访真，用随机策略进行模拟对局
   2.1 self._policy = policy_value_fn ：策略价值函数
   2.2 _evaluate_rollout(self, state, limit=1000)

2. get_move(self, state)
3. update_with_move(self, last_move)




---------------------------------------------------------------------------------------
# MCTSPlayer类


# rollout_policy_fn(board)


# policy_value_fn(board)


 