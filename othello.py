from minmax import AI, State
from copy import deepcopy
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import Ui_Othello
import sys
from time import sleep

SIZE_TAB = 8
NB_COUPS = 5

def init_tab():
    tab = [[None for i in range(SIZE_TAB)] for j in range(SIZE_TAB)]
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
    for i in range(SIZE_TAB):
        for j in range(SIZE_TAB):
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

                if i == SIZE_TAB-1:
                    if not border_memory[player_index][1][0]:
                        local_score += cell_score * 5
                        border_memory[player_index][1][0] = True
                    else:
                        local_score += cell_score * 2

                if j == SIZE_TAB-1:
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
    for i in range(1,SIZE_TAB):        
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
        while i < SIZE_TAB and d[2]:
            cell_target = state.get_cell(x+i*d[0], y+i*d[1])   
            if cell_target not in (player,None):        
                case_to_change_in_this_direction.append((x+i*d[0],y+i*d[1]))
            else:
                if cell_target == player and i > 1:
                    i = SIZE_TAB
                else:
                    d[2] = False
            i+=1

        if d[2]:
            #print("change detected: "+ str(d) + " len(t)= "+ str(len(case_to_change_in_this_direction)) +" position: "+ str(case_to_change_in_this_direction[0]))
            #print(state.get_cell((case_to_change_in_this_direction[0])[0],(case_to_change_in_this_direction[0])[1]))
            case_to_change += case_to_change_in_this_direction
            
    
    for c in case_to_change:
        state.set_cell(c[0],c[1],player)
    
    state.set_cell(x,y,player)
    return state


def action_funct(state,player):

    all_none_case = [(x,y) for x in range(SIZE_TAB) for y in range(SIZE_TAB) if state.get_cell(x,y) is None]

    for c in all_none_case:
        if case_can_be_play(c,state,player):
            new_state = deepcopy(state)
            new_state = add_token(new_state,c[0],c[1],player)

            # new_state.set_cell(c[0],c[1],player)
            yield new_state
    # yield state

def end_funct(state):
    new_state = next(action_funct(state,1))
    if new_state is None:
        return next(action_funct(state,2)) is None
    else:
        return False

# Main
if __name__ == "__main__":
    # init
    state = State(init_tab)
    ia = AI()

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    gui = Ui_Othello.Ui_MainWindow()
    gui.setupUi(MainWindow)
    MainWindow.show()

    # début de partie
    # print("state.tab :\n", state.tab)
    gui.refresh_grille(state)
    # 1er coups des noirs, noir = min
    if gui.couleur is gui.tour:
        gui.label_infos.setText("Humain joue les Noirs et commence !")
    else :
        gui.label_infos.setText("IA joue les Noirs et commence !")

    while not end_funct(state):
        print(state)
        if gui.couleur is gui.tour:
            # il s'agit du tour du joueur humain
            print('joueur')
            # print(state)
            while not gui.clic_joueur :
                QtCore.QCoreApplication.processEvents()
            gui.clic_joueur = False
            # print("done")
            new_state = add_token(state,gui.clicked_cells[-1][0],gui.clicked_cells[-1][1], 1 if gui.couleur else 2)
            # print(new_state)

        elif not gui.couleur:
            print("IA Noir")
            v,new_state = ia.min_value(NB_COUPS,state,utility_funct,action_funct,end_funct)

        else :
            print("IA Blanc")
            v,new_state = ia.max_value(NB_COUPS,state,utility_funct,action_funct,end_funct)

        state = new_state
        # inversion de qui joue le prochain coup
        gui.tour = not gui.tour
        print("refresh")
        gui.refresh_grille(state)
        gui.label_infos.setText("Noir joue !" if  gui.couleur and gui.tour else "Blanc joue !")


    sys.exit(app.exec_())
