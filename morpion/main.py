from minmax import State, AI
import copy

size_tab = 3
def create_morpion_tab():
    return [[None for i in range(size_tab)] for i in range(size_tab)]


def morpion_end(state):
    return morpion_utility(state)!= 0 or any([None in t for t in state.tab]) == False

def morpion_utility(state):
    result = 0
    r = 0
    for player in [1,2]:

        diag1=True
        diag2=True
        for x in range(len(state.tab)):
            
            diag1 = diag1 and state.get_cell(x,x) == player
            diag2 = diag2 and state.get_cell(len(state.tab)-1 - x,x) == player

            v = True
            h = True

            for y in range(len(state.tab)):

                if state.get_cell(x,y) != player:
                    v = False
                if state.get_cell(y,x) != player:
                    h = False
        if diag1 or diag2 or v or h:
            if player == 1:
                return -1
            else:
                return 1
    return 0


def morpion_new_state(state,player):
    
    for x in range(len(state.tab)):
        for y in range(len(state.tab)):
            if state.get_cell(x,y) is None:
                t = copy.deepcopy(state.tab)
                new_s = State(create_morpion_tab)
                new_s.tab = t
                new_s.set_cell(x,y,player)
                print(new_s)
                yield new_s
                
                
    



first_state = State(create_morpion_tab)
print(first_state.tab)
ai = AI()
v=ai.min_value(4,first_state,morpion_utility,morpion_new_state,morpion_end)
# Le min max trouve bien de manière générale un match null
print(v)
