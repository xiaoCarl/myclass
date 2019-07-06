# mcts_alphzero和mcts_pure代码走读

## _playout()函数对比

* 在mcts_alphzero中，直接根据训练的策略价值网络，获得对应的走棋概率，以及局面的价值

    action_probs, leaf_value = self._policy(state)

* 在mtcs_pure中，扩展叶子节点，并通过随机模拟对局获取该局面的价值

        action_probs, _ = self._policy(state)
        node.expand(action_probs)
        leaf_value = self._evaluate_rollout(state) 

### mcts_alphzero中的实现
    def _playout(self, state):
        """Run a single playout from the root to the leaf, getting a value at
        the leaf and propagating it back through its parents.
        State is modified in-place, so a copy must be provided.
        """
        node = self._root
        while(1):
            if node.is_leaf():
                break
            # Greedily select next move.
            action, node = node.select(self._c_puct)
            state.do_move(action)

        # Evaluate the leaf using a network which outputs a list of
        # (action, probability) tuples p and also a score v in [-1, 1]
        # for the current player.
        action_probs, leaf_value = self._policy(state)
        # Check for end of game.
        end, winner = state.game_end()
        if not end:
            node.expand(action_probs)
        else:
            # for end state，return the "true" leaf_value
            if winner == -1:  # tie
                leaf_value = 0.0
            else:
                leaf_value = (
                    1.0 if winner == state.get_current_player() else -1.0
                )

        # Update value and visit count of nodes in this traversal.
        node.update_recursive(-leaf_value)


### MCTS_pure中的实现
    def _playout(self, state):
        """Run a single playout from the root to the leaf, getting a value at
        the leaf and propagating it back through its parents.
        State is modified in-place, so a copy must be provided.

        node = self._root
        while(1):
            if node.is_leaf():
                break
            # Greedily select next move.
            action, node = node.select(self._c_puct)
            state.do_move(action)
        action_probs, _ = self._policy(state)
        end, winner = state.game_end() 
        if not end: 
            node.expand(action_probs)
            leaf_value = self._evaluate_rollout(state)
        else：
            if winner == -1:  # tie
                leaf_value = 0.0
            else:
                leaf_value = (
                    1.0 if winner == state.get_current_player() else -1.0
                )
        # Update value and visit count of nodes in this traversal.
        node.update_recursive(-leaf_value)

## mcts_pure中的get_move 与 mcts_alphazero中的get_move_probs

* mcts_pure 的get_move只需要获取下一步action

* 在mcts_alphazero,为了收集中self_play的数据s -> pi(pi 就是当前局面s下的所有action的概率),将所有move和probs一起返回。self_player时候，(s ,pi)就是训练数据；如需要走棋，就选最高prob的move


### mcts_alphazero中的get_move_probs函数

    def get_move_probs(self, state, temp=1e-3):
        """Run all playouts sequentially and return the available actions and
        their corresponding probabilities.
        state: the current game state
        temp: temperature parameter in (0, 1] controls the level of exploration
        """
        for n in range(self._n_playout):
            state_copy = copy.deepcopy(state)
            self._playout(state_copy)

        # calc the move probabilities based on visit counts at the root node
        act_visits = [(act, node._n_visits)
                      for act, node in self._root._children.items()]
        acts, visits = zip(*act_visits)
        act_probs = softmax(1.0/temp * np.log(np.array(visits) + 1e-10))

        return acts, act_probs

### mcts_pure中的get_move函数

    def get_move(self, state):
        """Runs all playouts sequentially and returns the most visited action.
        state: the current game state

        Return: the selected action
        """
        for n in range(self._n_playout):
            state_copy = copy.deepcopy(state)
            self._playout(state_copy)
        return max(self._root._children.items(),
                   key=lambda act_node: act_node[1]._n_visits)[0]


## MCSTplayer实现

* 在alphazero 中，需要考虑selfplayer 的场景，在该场景下move的选择增加了一些exploration。

    if self._is_selfplay:
    # add Dirichlet Noise for exploration (needed for
    # self-play training)
        move = np.random.choice(
            acts,
            p=0.75*probs + 0.25*np.random.dirichlet(0.3*np.ones(len(probs)))
        )
   

### mcts_alphazero的MCTSPlayer源代码

    class MCTSPlayer(object):
        """AI player based on MCTS"""

        def __init__(self, policy_value_function,
                    c_puct=5, n_playout=2000, is_selfplay=0):
            self.mcts = MCTS(policy_value_function, c_puct, n_playout)
            self._is_selfplay = is_selfplay

        def set_player_ind(self, p):
            self.player = p

        def reset_player(self):
            self.mcts.update_with_move(-1)

        def get_action(self, board, temp=1e-3, return_prob=0):
            sensible_moves = board.availables
            # the pi vector returned by MCTS as in the alphaGo Zero paper
            move_probs = np.zeros(board.width*board.height)
            if len(sensible_moves) > 0:
                acts, probs = self.mcts.get_move_probs(board, temp)
                move_probs[list(acts)] = probs
                if self._is_selfplay:
                    # add Dirichlet Noise for exploration (needed for
                    # self-play training)
                    move = np.random.choice(
                        acts,
                        p=0.75*probs + 0.25*np.random.dirichlet(0.3*np.ones(len(probs)))
                    )
                    # update the root node and reuse the search tree
                    self.mcts.update_with_move(move)
                else:
                    # with the default temp=1e-3, it is almost equivalent
                    # to choosing the move with the highest prob
                    move = np.random.choice(acts, p=probs)
                    # reset the root node
                    self.mcts.update_with_move(-1)

                if return_prob:
                    return move, move_probs
                else:
                    return move
            else:
                print("WARNING: the board is full")

        def __str__(self):
            return "MCTS {}".format(self.player)
