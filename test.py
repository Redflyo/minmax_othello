from minmax import AI, State
from copy import deepcopy
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import Ui_Othello
import sys
from time import sleep
import othello
def t():
    state = [[None for i in range(8)] for j in range(8)]
    state[0] = [2,2,2,2,2,2,2,2]
    state[1] = [2,2,1,1,1,2,2,1]
    state[2] = [1,2,2,2,2,2,1,1]
    state[3] = [1,2,2,2,1,1,1,1]
    state[4] = [1,1,2,2,1,2,1,1]
    state[5] = [1,None,1,1,1,1,1,1]
    state[6] = [None,None,1,2,2,2,None,None]
    state[7] = [2,2,2,2,2,2,None,None]

    for i in range(8):
        for j in range(8):
            if not state[i][j] is None:
                state[i][j] = (state[i][j]%2) +1 

    return state

state = State(t)
ia = AI()

app = QApplication(sys.argv)
MainWindow = QMainWindow()
gui = Ui_Othello.Ui_MainWindow()
gui.setupUi(MainWindow)
MainWindow.show()
gui.tour = not gui.tour
print(othello.human_play(state,6,6,2))
othello.gameloop(state,ia,gui)
sys.exit(app.exec_())