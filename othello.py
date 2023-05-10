from minmax import AI, State
from copy import deepcopy
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import Ui_Othello
import sys
from time import time

SIZE_TAB = 8
NB_COUPS = 5

POINT_SIDE = 2
CORNER = 20
SIDE = 5
NONE_CASE_BETWEEN_ON_SIDE=3

def init_tab():
    tab = [[None for i in range(SIZE_TAB)] for j in range(SIZE_TAB)]
    (tab[3])[3] = 2
    (tab[4])[4] = 2
    (tab[3])[4] = 1
    (tab[4])[3] = 1
    return tab

def __hash__(self):
    return hash(self.__str__())

def get_score(player):
    if player==1:
        return -1
    elif player==2:
        return 1
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
                        local_score += cell_score * SIDE
                        border_memory[player_index][0][0] = True
                    else:
                        local_score += cell_score * POINT_SIDE
                    
                    if j == 0:
                        local_score += cell_score * CORNER
                    elif j == SIZE_TAB - 1:
                        local_score += cell_score * CORNER

                if j == 0:
                    if not border_memory[player_index][0][1]:
                        local_score += cell_score * SIDE
                        border_memory[player_index][0][1] = True
                    else:
                        local_score += cell_score * POINT_SIDE

                if i == SIZE_TAB-1:
                    if not border_memory[player_index][1][0]:
                        local_score += cell_score * SIDE
                        border_memory[player_index][1][0] = True
                    else:
                        local_score += cell_score * POINT_SIDE
                    
                    if j == 0:
                        local_score += cell_score * CORNER
                    elif j == SIZE_TAB - 1:
                        local_score += cell_score * CORNER

                if j == SIZE_TAB-1:
                    if not border_memory[player_index][1][1]:
                        local_score += cell_score * SIDE
                        border_memory[player_index][1][1] = True
                    else:
                        local_score += cell_score * POINT_SIDE

                if local_score == 0:
                    local_score += cell_score
                score += local_score

        local_score=0
        for offset_x in [0,SIZE_TAB-1]:
            for offset_y in [0,SIZE_TAB-1]:
                x_player1_none_case_between = False
                x_player2_none_case_between = False
                y_player1_none_case_between = False
                y_player2_none_case_between = False
                for i in range(SIZE_TAB-1):
                    if state.get_cell(i,offset_y) == state.get_cell(i+2,offset_y) and state.get_cell(i+1,offset_y) is None:
                        if state.get_cell(i,offset_y) == 1:
                            x_player1_none_case_between = not x_player1_none_case_between
                        elif state.get_cell(i,offset_y) == 2:
                            x_player2_none_case_between = not x_player2_none_case_between

                    if state.get_cell(offset_x,i) == state.get_cell(offset_x,i+2) and state.get_cell(offset_x,i+1) is None:
                        if state.get_cell(offset_x,i) == 1:
                            y_player1_none_case_between = not y_player1_none_case_between
                        elif state.get_cell(offset_x,i) == 2:
                            y_player2_none_case_between = not y_player2_none_case_between


                if y_player1_none_case_between:
                    local_score += get_score(2) * NONE_CASE_BETWEEN_ON_SIDE
                if y_player2_none_case_between:
                    local_score += get_score(1) * NONE_CASE_BETWEEN_ON_SIDE

                if x_player1_none_case_between:
                    local_score += get_score(2) * NONE_CASE_BETWEEN_ON_SIDE
                if x_player2_none_case_between:
                    local_score += get_score(1) * NONE_CASE_BETWEEN_ON_SIDE
    score+=local_score
    print(score)
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
        can_eat = False
        while not(can_eat) and d[2]:
            cell_x = x+i*d[0]
            cell_y = y+i*d[1]
            cell_target = state.get_cell(cell_x, cell_y )   
            if cell_target not in (player,None):        
                case_to_change_in_this_direction.append((x+i*d[0],y+i*d[1]))
            else:
                if cell_target == player and i > 1:
                    can_eat = True
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
    new_move = False
    for c in all_none_case:
        if case_can_be_play(c,state,player) == True:
            new_state = deepcopy(state)
            new_move = True
            new_state = add_token(new_state,c[0],c[1],player)

            # new_state.set_cell(c[0],c[1],player)
            yield new_state
    if not new_move:
        yield state

def end_funct(state):
    new_state = next(action_funct(state,1)) == state
    if new_state :
        return next(action_funct(state,2)) == state
    else:
        return False

def human_play(state,x,y,player):
    if state.get_cell(x,y) is None:
        print("boucle")
        states = list([n for n in action_funct(state,player)])
        for n in states:
            print("value:",n.get_cell(x,y))
            if n.get_cell(x,y) == player:
                print("one time")
                return n
        if len(states) == 1:
            print("normal")
            return states[0]
    [print(s) for s in states]
    print("none:")
    return None

def qt_wait(delay : int):
    """Permet de laisser un délai qui permet de voir les coups de l'IA

    Args:
        delay (int): délai en secondes
    """
    loop = QtCore.QEventLoop()
    QtCore.QTimer.singleShot(delay*1000, loop.quit)
    loop.exec_()
        

def gameloop(state : State, ia : AI, gui : Ui_Othello.Ui_MainWindow):
    """Boucle principale de jeu, alterne entre les joueurs, rafraichit l'affichage et les informations, calule les temps de jeu.

    Args:
        state (State): état initial du plateau
        ia (AI): framework minmax
        gui (Ui_Othello.Ui_MainWindow): objet de l'interface graphique
    """
    gui.refresh_grille(state)

    if gui.couleur is gui.tour:
        gui.label_infos.setText("Humain joue les Noirs et commence !")

    else :
        gui.label_infos.setText("IA joue les Noirs et commence !")

    chrono = 0
    tour = 1
    while not end_funct(state):
        new_state = None
        if gui.couleur is gui.tour:
            # il s'agit du tour du joueur humain
            # print(state)
            print("Human to play")
            while new_state is None:
                if next(action_funct(state,1 if gui.couleur else 2)) != state:
                    while not gui.clic_joueur:
                        QtCore.QCoreApplication.processEvents()
                    gui.clic_joueur = False
                        # print("done")
                    new_state = human_play(state,gui.clicked_cells[-1][0],gui.clicked_cells[-1][1], 1 if gui.couleur else 2)
                else:
                    new_state = state

        elif not gui.couleur:
            qt_wait(1)
            print("IA Noir")
            start = time()
            _,new_state = ia.min_value(NB_COUPS,state,utility_funct,action_funct,end_funct)
            chrono += time()-start
            # gui.label_temps.setText(f"Temps IA : {chrono:.3f}s\nTest")
            

        else :
            qt_wait(1)
            print("IA Blanc")
            start = time()
            _,new_state = ia.max_value(NB_COUPS,state,utility_funct,action_funct,end_funct)
            chrono += time()-start
            # gui.label_temps.setText(f"Temps IA : {chrono:.3f}s\nTest")

        if not(new_state is None):
            state = new_state
            # inversion de qui joue le prochain coup
            gui.tour = not gui.tour
            print("refresh")
            gui.refresh_grille(state)
            msg = f"\nTour n°{tour}\nTemps IA : {chrono:.3f}s"
            gui.label_infos.setText(f"Noir joue !{msg}" if  gui.couleur and gui.tour else f"Blanc joue !{msg}")
            tour += 1
        print("Current state:")
        print(state)
    print("end of the game")

if __name__ == "__main__":
    # minmax init
    state = State(init_tab)
    ia = AI()

    # UI init
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    gui = Ui_Othello.Ui_MainWindow()
    gui.setupUi(MainWindow)
    MainWindow.show()

    # Lancement du jeu
    gameloop(state,ia,gui)
    
    # Sortie de l'application graphique
    sys.exit(app.exec_())
