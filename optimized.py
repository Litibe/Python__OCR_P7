import csv
import time


def open_csv_and_extract(file, min_win_per_action=0.5):
    actions = []
    with open(file, 'r') as csvfile:
        csvfile_open = csv.reader(csvfile, delimiter=',', quotechar='|')
        i = 0
        for row_csv in csvfile_open:
            # suppressions des actions corrompues:
            if i != 0 and float(row_csv[1]) > float(0) and float(
                    row_csv[2]) > float(0) and (float(row_csv[1]) * float(
                                        row_csv[2])/100) > float(
                                            min_win_per_action):
                # calcul beneficie en index 3
                # ajout dans liste sous forme tuple si ok
                actions.append((row_csv[0],
                                float(row_csv[1]),
                                row_csv[2],
                                round(
                                    float(row_csv[1]) * float(
                                        row_csv[2])/100, 2)))
            i += 1
    return actions


def construction_tableau(actions, budget):
    # array double
    # abscisse avec recherche budget, première case 0 pour initialiser
    # ordonnées liste des actions , première case 0 pour initialiser
    array = [[0 for x in range(budget + 1)] for x in range(len(actions) + 1)]

    #  on commence par index 1 et Non 0 pour faire comparaison de l'action
    #  en cours avec action précédente
    for n_action in range(1, len(actions) + 1):
        # extraction de l'index des actions pour search_actions
        for monnaie in range(1, budget + 1):
            # extraction de chaque euro issue du budget pour comparatif
            # (NAME_ACTION, cost, %profit)
            # si l'action en cours a un cout d'achat < au budget en cours
            if actions[n_action-1][1] <= monnaie:
                array[n_action][monnaie] = round(max(
                    actions[n_action-1][3] + float(
                        array[n_action-1][round(monnaie -
                            actions[n_action-1][1])]),
                        array[n_action-1][round(monnaie)]),2)
            else:
                array[n_action][round(monnaie)] = round(array[n_action-1][round(monnaie)],2)

    n_actions = len(actions)
    actions_to_buy = []
    while budget > 0 and n_actions > 0:
        # on selectionne dernière action de la liste
        action_to_compare = actions[n_actions-1]
        # pour comparaison ci dessous
        budget_after_buy_action = array[n_actions-1][round(budget-action_to_compare[1])]
        win_previous_action = actions[n_actions-1][3]

        if array[n_actions][
            round(budget)] == budget_after_buy_action + win_previous_action:
            actions_to_buy.append(action_to_compare)
            budget -= action_to_compare[1]
        n_actions -= 1
    cost = sum([action[1] for action in actions_to_buy])
    return array[-1][-1], sorted(actions_to_buy), cost


def main():
    choice_file = 0
    while choice_file not in [1,2,3]:
        print("""Poissibilité d'extraction : 
        Choix 1 : data_20actions.csv
        Choix 2 : dataset1_Python+P7.csv
        Choix 3 : dataset2_Python+P7.csv""")
        try:
            choice_file = int(input(
                "Merci de saisir le choix de votre fichier : "))
            if choice_file == 1:
                link_file = 'csv/data_20actions.csv'
            elif choice_file == 2:
                link_file = 'csv/dataset1_Python+P7.csv'
            elif choice_file == 3:
                link_file = 'csv/dataset2_Python+P7.csv'
            else:
                print("Merci de faire un choix valide")
        except ValueError:
            print("Merci de faire un choix valide")
    return link_file


if __name__ == "__main__":
    link_file = main()
    start_time = time.time()
    print("Ouverture du fichier : ", link_file.split("/")[1])
    actions = open_csv_and_extract(link_file)
    max_benefice, actions_to_buy, min_cost = construction_tableau(
        actions, budget=499)
    print(f"\nPour un bénéfice de {max_benefice}€ "
          f"et pour un coût d'achat de {min_cost}€, "
          f"voici les actions à acheter :")
    print("Action_Name, Cost, %_Profit, €_Profit")
    for action in actions_to_buy :
        print(action)
    print("--- %s seconds ---" % (time.time() - start_time))
