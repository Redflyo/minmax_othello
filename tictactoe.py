#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version : 3.10.6

__author__ = "Yacine Lefebvre-Aladawi"
__copyright__ = "Copyright 2023, Projet final tic-tac-toe"
__credits__ = ["Yacine Lefebvre-Aladawi"]
__license__ = "All rights reserved"
__version__ = "0.1"


# ----------Import----------
import numpy as np
import pandas as pd
# --------------------------


# ----------Consts----------

# --------------------------


# ---------Functions--------
def get_grille()->pd.DataFrame:
    df = pd.DataFrame(data=np.zeros((3, 3), dtype=str), index=range(0,3), columns=("a","b","c"))
    return df


def utility(grille_util : pd.DataFrame)->int:
    """Calcule la valeur de l’état final

    Returns:
        int: 1 si x gagne, 0 si match nul, -1 si x perd
    """
    return 0


def player(grille_player : pd.DataFrame)->str:
    """décrit le joueur qui doit déplacer un pion sur l’état grille_player

    Args:
        grille_player pd.DataFrame: _description_
    """
    return "x"


def action(grille_action : pd.DataFrame)->list():
    """retourne toutes les actions possibles à partir de grille_action

    Args:
        grille_action pd.DataFrame: _description_
    """


def result(grille_etat : pd.DataFrame, df_action : pd.DataFrame)->pd.DataFrame:
    """retourne un état après avoir appliqué l’action df_action sur l’état grille_etat

    Args:
        grille_etat pd.DataFrame: _description_
        df_action pd.DataFrame: _description_
    """


def terminal_test(grille_test : pd.DataFrame)->bool:
    """Teste si la grille est un etat final

    Args:
        grille_test (pd.DataFrame): _description_

    Returns:
        bool: final ou pas
    """
    termine = False

    # test des colonnes gagnantes
    # print("cols")
    for c in grille_test.columns:
        test = grille_test[c].value_counts().eq(3).any()
        # print(test)
        if test :
            termine = True
            break
    
    # test des lignes gagnantes si pas de cols gagnantes
    if not termine :
        # print("\nlignes")
        for i in range(len(grille_test)):
            test = grille_test.iloc[i].value_counts().eq(3).any()
            # print(test)
            if test :
                termine = True
                break

    # test des diagonales gagnantes, notre grille est carrée
    # diag1 = \ et diag2 = /
    if not termine :
        diag1 = ""
        diag2 = ""
        for i in range(len(grille_test)):
            diag1 += grille_test.iloc[i][i]
            diag2 += grille_test.iloc[i][len(grille_test)-1-i]
            # print("diag : ", diag)
        test = (diag1.count(diag1[0]) == len(diag1)) or (diag2.count(diag2[0]) == len(diag2))

        # print(test)
        if test :
            termine = True

    # grille pleine mais pas gagnante, match nul
    if (not termine) and (grille_test.replace("", np.nan).isna().sum().sum() == 0) :
        termine = True

    return termine

def utility(grille_util : pd.DataFrame):
    return 0

def alpha_beta_search(grille_search : pd.DataFrame):
    v = max_value(grille_search, -np.inf, np.inf)
    # return a in actions(grille_search) if a = v

def max_value(grille_max : pd.DataFrame, alpha, beta):
    if terminal_test(grille_max):
        return utility(grille_max)
    v = -np.inf
    for a in actions(grille_max) :
        v = max(v,min_value(result(s,alpha), alpha, beta))
        if v >= beta :
            return v
        alpha = max(alpha, v)

def min_value(grille_min : pd.DataFrame, alpha, beta):
    if terminal_test(grille_min):
        return utility(grille_min)
    v = np.inf
    for a in actions(grille_min) :
        v = min(v,max_value(result(s,alpha), alpha, beta))
        if v <= alpha :
            return v
        beta = min(beta, v)

def main():
    # initialisation du plateau, "" = case vide, "o" = o, "x" = x
    grille =  get_grille()
    grille.iloc[0]["a"] = "o"
    grille.iloc[0]["b"] = "o"
    grille.iloc[0]["c"] = "x"

    grille.iloc[1]["a"] = "x"
    grille.iloc[1]["b"] = "x"
    grille.iloc[1]["c"] = "o"

    grille.iloc[2]["a"] = "o"
    grille.iloc[2]["b"] = "o"
    grille.iloc[2]["c"] = "x"
    print("grille :")
    print(grille.to_markdown(tablefmt=("grid")))

    return 0
# --------------------------


# -----------Main-----------
if __name__ == '__main__' :
    main()
    exit()
# --------------------------
