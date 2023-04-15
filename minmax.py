import numpy as np
class State:
    def _init_tab(self,init_tab_funct):
        self.tab = init_tab_funct()
    

    def __init__(self,size_tab):
        self._init_tab(size_tab)


    def get_cell(self,x,y):
        if (x < len(self.tab) and x >= 0) and (y < len(self.tab) and y >= 0):
            return (self.tab[x])[y]
        else:
            return None
        

    def set_cell(self,x,y,value):
        (self.tab[x])[y] = value


    def __str__(self):
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
            depth_max (_type_): _description_
            state (_type_): _description_
            utility_funct (_type_): _description_
            action_funct (_type_): _description_
            game_end_funct (_type_): _description_
            alpha (_type_, optional): _description_. Defaults to -np.inf.
            beta (_type_, optional): _description_. Defaults to np.inf.
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
            depth_max (_type_): _description_
            state (_type_): _description_
            utility_funct (_type_): _description_
            action_funct (_type_): _description_
            game_end_funct (_type_): _description_
            alpha (_type_): _description_
            beta (_type_): _description_
            depth_cpt (int, optional): _description_. Defaults to 0.

        Returns:
            _type_: _description_
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
