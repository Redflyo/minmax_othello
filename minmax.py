import numpy as np
class State:
    def __init__(self,init_tab_funct):
        """Generate the starter with the function init_tab 

        Args:
            init_tab_funct (func): This function must return the First State
        """
        self.tab = init_tab_funct()

    def get_cell(self,x,y):
        """Return the value contain at the x,y cell

        Args:
            x (int): X coordinate
            y (int): Y coordinate

        Returns:
            Optionnal[int]: Value containing
        """
        if (x < len(self.tab) and x >= 0) and (y < len(self.tab) and y >= 0):
            return (self.tab[x])[y]
        else:
            return None
        

    def set_cell(self,x,y,value):
        """Put value in the cell at the coordinate x,y

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            value (int): Value of the cell
        """
        (self.tab[x])[y] = value


    def __str__(self):
        """Define the State in string

        Returns:
            string: String representing the current State
        """
        result = ""
        for t in self.tab:
            result += ("_"*(len(self.tab)*2+1)) + "\n"
            for d in t:
                if d is not None:
                    result += ("|"+str(d))
                else:
                    result += ("| ")
            result += ("|\n")
        return result


class AI:
    def __init__(self):
        self.min_player=1 # noir
        self.max_player=2 # blanc


    def min_value(self,depth_max,state,utility_funct,action_funct,game_end_funct,alpha=-np.inf,beta=np.inf,depth_cpt=0):
        """le joueur min est le joueur noir, il commence toujours la partie.

        Args:
            depth_max (int): Depth max 
            state (State): State tested
            utility_funct (func): Return the Score of the State
            action_funct (func): Yield all the next State possible for a Player
            game_end_funct (func): Check if the game is finnished
            alpha (int): current alpha. Defaults to -np.inf.
            beta (int): current beta. Defaults to np.inf.
            depth_cpt (int, optional): _description_. Defaults to 0.

        Returns:
            _type_: _description_
        """
        new_depth = depth_cpt + 1
        if game_end_funct(state) or new_depth > depth_max:
            return utility_funct(state), state
        else:
            better_move= state
            v = np.inf
            for new_state in action_funct(state,self.min_player):
                new_v,_ = self.max_value(depth_max,new_state,utility_funct,action_funct,game_end_funct,alpha,beta,new_depth)
                if new_v < v:
                    v = new_v
                    better_move = new_state

                if v < alpha :
                    return v, better_move
                beta = min(beta, v)
                
            return v,better_move


    def max_value(self,depth_max,state,utility_funct,action_funct,game_end_funct,alpha=-np.inf,beta=np.inf,depth_cpt=0):
        """le joueur max est le joueur blanc, il joue après le Noir.

        Args:
            depth_max (int): Depth max 
            state (State): State tested
            utility_funct (func): Return the Score of the State
            action_funct (func): Yield all the next State possible for a Player
            game_end_funct (func): Check if the game is finnished
            alpha (int): current alpha. Defaults to -np.inf.
            beta (int): current beta. Defaults to np.inf.
            depth_cpt (int, optional): _description_. Defaults to 0.

        Returns:
            Tuple[int,State]: Return the score associate with the better new State choosen by the  max Player
        """
        new_depth = depth_cpt + 1
        if game_end_funct(state) or new_depth > depth_max:
            return utility_funct(state),state
        else:
            better_move = state
            v = -np.inf
            for new_state in action_funct(state,self.max_player):
                new_v,_ = self.min_value(depth_max,new_state,utility_funct,action_funct,game_end_funct,alpha,beta,new_depth) 
                if new_v > v:
                    better_move = new_state
                    v = new_v
                if v >= beta :
                    return v,better_move
                alpha = max(alpha, v)
            return v,better_move
