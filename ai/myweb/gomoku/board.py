from __future__ import print_function
from collections import defaultdict


class Board(object):
    '''
    Define general rules of a game.
    State: State is an object which is only be used inside the board class.
        Normally, a state include game board information (e.g. chessmen positions, action index, current action, current player, etc.)
    Action: an object to describe a move. 
    '''
    def __init__(self):

        '''
        width,height: The board's width & height.        
        num_players: The player numbers of the board.
        n_in_low:  How many pieces in a row to win.
        states: The board's states is stored as a dict, key is the move (as a location) on the board,value is the player
        availables: keep available moves in a list
        '''
        self.width = 15
        self.height = 15
        self.n_in_row =5
        self.num_players = 2    
        self.players = [1,2]
       
        self.states = defaultdict(lambda:0)
        self.availables = list(range(self.width * self.height))

        self.last_action = -1

    def location_to_action(self,i,j):
        """location = (i,j),move=i+j*width 
        """
        return i+j*self.width

    def action_to_location(self,move):
        """location = (i,j),dot=i+j*width 
        """
        j = move % self.width
        i = move // self.height
        return [i, j]

    def start(self,player1,player2):
        ''' 
        Start the game
        Return: the initial state
        '''

        self.player1 = player1
        self.player2 = player2
        self.currentplayer = player1

        #self.display()
        while True:
            player_in_turn = self.current_player()
            action = player_in_turn.get_action(self) 
            state = self.next_state(action)
        #    self.display()
            end ,winner = self.winner()
            self.current_player().reply(end,winner,self.states[action],
                 self.action_to_location(action)[1],
                 self.action_to_location(action)[0])

            if end:
                self.player1.reply(end,winner,self.states[action],
                    self.action_to_location(action)[1],
                    self.action_to_location(action)[0])
                self.player2.reply(end,winner,self.states[action],
                    self.action_to_location(action)[1],
                    self.action_to_location(action)[0])

                if winner != -1:
                    print("Game end. Winner is", self.players[winner-1])
                else:
                    print("Game end. Tie")
                return winner

    def display(self):
        '''
        Dispaly the board
        state: current state
        action: current action
        Return: display information
        '''
        width = self.width
        height = self.height

        print("Player1", self.players[0], "with X".rjust(3))
        print("Player2", self.players[1], "with O".rjust(3))
        print("current play loc:",self.action_to_location(self.last_action))
        print()
        for x in range(self.width):
            print("{0:8}".format(x), end='')
        print('\r\n')
        for i in range(self.height - 1, -1, -1):
            print("{0:4d}".format(i), end='')
            for j in range(self.width):
                loc = i * self.width + j
                p = self.states.get(loc, -1)
                if p == self.players[0]:
                    print('X'.center(8), end='')
                elif p == self.players[1]:
                    print('O'.center(8), end='')
                else:
                    print('_'.center(8), end='')
            print('\r\n\r\n') 

    def parse(self, action):
        '''
        Parse player input text into an action.
        If the input action is invalid, return None.
        The method is used by a human player to parse human input.
        action: player input action texxt.
        Return: action if input is a valid action, otherwise None.
        '''
        return None

    def next_state(self, action):
        '''
        Calculate the next state base on current state and action.
        state: the current state
        action: the current action
        Return: the next state
        '''
        if self.currentplayer == self.player1:
            p = self.players[0]
            self.currentplayer =self.player2
        else:
            p = self.players[1]   
            self.currentplayer =self.player1
                
        self.states[action] = p
        self.availables.remove(action)
        self.last_action = action
        return action

    def is_legal(self, history, action):
        '''
        Check if an action is legal.
        The method is used by a human player to validate human input.
        history: an array of history states.
        Return: ture if the action is legal, otherwise return false.
        '''
        return True

    def legal_actions(self, history):
        '''
        Calculate legal action from history states.
        The method is mainly used by AI players.
        history: an array of history states.
        Return: an array of legal actions.
        '''
        return actions

    def current_player(self):
        '''
        Gets the current player.
        state: the current state.
        Return: the current player number.
        '''
        return self.currentplayer

    def winner(self):
        '''
        Gets the win player.
        history: an array of history states.
        Return: win player number. 0: no winner and no end, players numbers + 1: draw
        '''
        width  = self.width
        height = self.height
        states = self.states
        n = self.n_in_row

        moved = list(set(range(width * height)) - set(self.availables))
        if len(moved) < 9:
            return False, -1  

        for m in moved:
            h = m // width
            w = m % width
            player = states[m]

            if (w in range(width - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n))) == 1):
                return True, player

            if (h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * width, width))) == 1):
                return True, player

            if (w in range(width - n + 1) and h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * (width + 1), width + 1))) == 1):
                return True, player

            if (w in range(n - 1, width) and h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * (width - 1), width - 1))) == 1):
                return True, player
        
        if len(self.availables) == 0 :
            return True ,-1  #tie
        else: 
            return False, -1


    def winner_message(self, winner):
        '''
        Gets game result.
        winner: win player number
        Return: winner message, the game result.
        '''
        return "WOW"

