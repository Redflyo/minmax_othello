# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QMessageBox, QMainWindow

# constantes de départ issues de l'image du plateau de jeu
IMG_W, IMG_H = 791, 778
WIN_H = IMG_H + 80
PION_SIZE = 86
XO = 61
YO = 48
BORDER = 5
SQ_SIZE = 86

class Ui_MainWindow(object):
    """Classe de définition de l'interface graphique
    """
    
    def lucida_14(self):
        """Définition de la police de caractère du logiciel
        """
        lucida_font = QtGui.QFont()
        lucida_font.setFamily("Lucida Sans Unicode")
        lucida_font.setPointSize(14)
        lucida_font.setBold(True)
        lucida_font.setItalic(False)
        lucida_font.setUnderline(False)
        lucida_font.setWeight(75)
        lucida_font.setStrikeOut(False)
        lucida_font.setKerning(True)
        self.lucida_font = lucida_font


    def get_label_infos(self):
        """Créé un label texte permettant d'afficher les information de al partie en cours
        """
        label_infos = QLabel(self.centralwidget)
        label_infos.setGeometry(203, 0, 450, 75)
        label_infos.setFont(self.lucida_font)
        label_infos.setScaledContents(False)
        label_infos.setAlignment(QtCore.Qt.AlignCenter)
        label_infos.setWordWrap(False)
        label_infos.setObjectName("label_infos")
        label_infos.setText("Noir commence !")
        self.label_infos = label_infos


    def get_label_grille(self):
        """Créé un label image qui affiche al grille de jeu
        """
        label_grille = QLabel(self.centralwidget)
        label_grille.setGeometry(0, WIN_H-IMG_H, IMG_W, IMG_H)
        label_grille.setText("")
        label_grille.setPixmap(QtGui.QPixmap("GrilleOthello.png"))
        label_grille.setObjectName("label_grille")
        label_grille.mousePressEvent = self.placer_pion
        self.label_grille = label_grille


    def popup_choix_couleur(self):
        """Affiche un popup permettant de choisir la couleur du joueur
        """
        choice = QMessageBox()
        choice.setWindowTitle("Choix des pions")
        choice.setText("Choisissez votre couleur (Noir commence) :")
        choice.setFont(self.lucida_font)
        choice.addButton("Noir", QMessageBox.YesRole)
        choice.addButton("Blanc", QMessageBox.NoRole)
        self.couleur = True if choice.exec() == 0 else False
        # print("reponse : ", self.couleur)


    def setupUi(self, MainWindow : QMainWindow):
        """Mise en place de l'interface graphique PyQt5

        Args:
            MainWindow (QMainWindow): objet PyQt5.QtWidgets.MainWindow()
        """
        self.tour = True
        self.clicked_cells = []
        self.clic_joueur = False
        self.lucida_14()

        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Othello (La meilleure version)")
        MainWindow.setFixedWidth(IMG_W)
        MainWindow.setFixedHeight(WIN_H)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")

        self.popup_choix_couleur()
        self.get_label_infos()
        self.get_label_grille()

        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def refresh_grille(self, grille : list):
        """Raffraichit l'affichage de la double liste à chaque fin de tour

        Args:
            grille (list): liste 2D à lire pour affihcer les pièces correspondantes
        """
        for r in range(len(grille.tab)):
            for c in range(len(grille.tab[r])):
                if grille.tab[r][c] !=None : 
                    self.get_piece(r, c, grille.tab[r][c])

    def get_piece(self, row : int, col : int, clr : int):
        """Affiche une pièce de couleur donnée sur la grille dans la cellule donnée en paramètre

        Args:
            row (int): indice de ligne
            col (int): indice de colonne
            clr (int): indice de couleur
        """
        # Définition des coordonnées de positionnement pour la pièce
        new_x = int((XO+SQ_SIZE/2+col*(SQ_SIZE+BORDER))-PION_SIZE*0.5)
        new_y = int((YO+SQ_SIZE/2+row*(SQ_SIZE+BORDER))+PION_SIZE*0.45)
        print("ligne : ", new_x," colonne : ", new_y, " couleur : ", "noir" if clr == 1 else "blanc")
        self.label_piece = QLabel(self.centralwidget)
        self.label_piece.setGeometry(new_x, new_y, PION_SIZE, PION_SIZE)
        self.label_piece.setText("")
        self.label_piece.setPixmap(QtGui.QPixmap("pion_noir.png" if clr == 1 else "pion_blanc.png")) 
        self.label_piece.setObjectName("label_piece")
        self.label_piece.show()


    def placer_pion(self, clic):
        """Conversion des coordonnées du clic en cellule de grille "1A" "5C" etc afin que tout clic dans une cellule soit défini au centre de cette cellule.

        Args:
            clic (mousePressEvent): évènement du clic, contient la position en pixels.
        """

        # Coordonnées du clic en pixels
        x = clic.pos().x()
        y = clic.pos().y()
        # print("\nclicked ! x : ", x," y : ", y)

        # Définition de la cellule cliquée   
        row = (y - YO)//(SQ_SIZE+BORDER) 
        col = (x - XO)//(SQ_SIZE+BORDER)
        # print("row : ", row," col : ", col)

        # Création de la nouvelle pièce à la bonne position
        # self.get_piece(row, col, True if self.couleur else False)
        self.clicked_cells.append((row,col))
        self.clic_joueur = True
