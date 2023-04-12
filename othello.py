from minmax import AI, State
from copy import deepcopy
size_tab = 8
def init_tab():
    tab = [[None for i in range(size_tab)] for j in range(size_tab)]
    (tab[3])[3] = 1
    (tab[4])[4] = 1
    (tab[3])[4] = 2
    (tab[4])[3] = 2
    return tab

def get_score(player):
    if player==1:
        return 1
    elif player==2:
        return -1
    else:
        return 0

def utility_funct(state):
    score = 0
    border_memory = [[[False,False],[False,False]],[[False,False],[False,False]]]
    for i in range(size_tab):
        for j in range(size_tab):
            cell_value = state.get_cell(i,j)
            if cell_value is not None:
                local_score = 0
                cell_score = get_score(cell_value)
                player_index = cell_value - 1
                if i == 0:
                    if not border_memory[player_index][0][0]:
                        local_score += cell_score * 5
                        border_memory[player_index][0][0] = True
                    else:
                        local_score += cell_score * 2
                if j == 0:
                    if not border_memory[player_index][0][1]:
                        local_score += cell_score * 5
                        border_memory[player_index][0][1] = True
                    else:
                        local_score += cell_score * 2
                if i == size_tab-1:
                    if not border_memory[player_index][1][0]:
                        local_score += cell_score * 5
                        border_memory[player_index][1][0] = True
                    else:
                        local_score += cell_score * 2
                if j == size_tab-1:
                    if not border_memory[player_index][1][1]:
                        local_score += cell_score * 5
                        border_memory[player_index][1][1] = True
                    else:
                        local_score += cell_score * 2

                if local_score == 0:
                    local_score += cell_score

                score += local_score
                

    return score
            


def get_direction_possible():
    return [[i,j,True] for i in range(-1,2,1) for j in range(-1,2,1) if not(i == j and i == 0) ]

def case_can_be_play(coordinate,state,player):
    x,y = coordinate
    direction_possible = get_direction_possible()
    for i in range(1,size_tab):        
        for d in direction_possible:
            if d[2]:
                cell_target = state.get_cell(x+i*d[0], y+i*d[1])
                if cell_target==player and i > 1:
                    return True
                else:
                    d[2] = cell_target not in (player,None)
    return False

def add_token(state,x,y,player):
    case_to_change = []
    for d in get_direction_possible():
        case_to_change_in_this_direction = []
        i=1
        while i < size_tab and d[2]:
            cell_target = state.get_cell(x+i*d[0], y+i*d[1])   
            if cell_target not in (player,None):        
                case_to_change_in_this_direction.append((x+i*d[0],y+i*d[1]))
            else:
                if cell_target == player and i > 1:
                    i = size_tab
                else:
                    d[2] = False
            i+=1

        if d[2]:
            #print("change detected: "+ str(d) + " len(t)= "+ str(len(case_to_change_in_this_direction)) +" position: "+ str(case_to_change_in_this_direction[0]))
            #print(state.get_cell((case_to_change_in_this_direction[0])[0],(case_to_change_in_this_direction[0])[1]))
            case_to_change += case_to_change_in_this_direction
            
    
    for c in case_to_change:
        state.set_cell(c[0],c[1],player)
    

    return state


def action_funct(state,player):

    all_none_case = [(x,y) for x in range(size_tab) for y in range(size_tab) if state.get_cell(x,y) is None]

    for c in all_none_case:
        if case_can_be_play(c,state,player):
            new_state = deepcopy(state)
            new_state = add_token(new_state,c[0],c[1],player)

            new_state.set_cell(c[0],c[1],player)
            yield new_state

def end_funct(state):
    new_state = next(action_funct(state,1))
    if new_state is None:
        return next(action_funct(state,2)) is None

# Main
# init
state = State(init_tab)
ia = AI()

# début de partie
# 1er coups des noirs, noir = min
v,next_move = ia.min_value(5,state,utility_funct,action_funct,end_funct)
print(next_move)
