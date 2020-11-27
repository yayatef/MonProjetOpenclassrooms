
#def send_command(command):
#! /usr/bin/python3.9
# -*- coding:utf-8 -*-

import datetime  # importe le module datetime pour gérer la date et l'heure
import os        # importe le module os pour interagir avec le système d'exploitation
import ldap      # importe le module ldap pour gérer le serveur ldap

# initialisation d'un nouvel objet de connexion pour accéder au serveur ldap 
conn = ldap.initialize('ldap://127.0.0.1')
conn.protocol_version = 3
conn.set_option(ldap.OPT_REFERRALS, 0) # Pour avoir accès à Active Directory
conn.simple_bind_s('Administrateur@entreprise.lan','Openclassrooms#') # Authentification de l'admin du domaine

# Déclaration des variables
domain_controller = 'DC=entreprise,DC=lan'
users_ou = 'OU=Distant,OU=Employee,{}'.format(domain_controller)
groups_ou = 'OU=Employee_Groups,{}'.format(domain_controller)

# Création de l'utilisateur dans Active Directory en utilisant la fonction create_user() 
# avec les arguments suivants: nom d'ouverture de session, prénom, nom, nom cmplet
def create_user(username, first_name, last_name, display_name, active=False):
    """
    Create New user in AD
    :param username:
    :param first_name:
    :param last_name:
    :param display_name:
    :param active:
    :return:
    """
    if active:
        disabled = 'no'
    else:
        disabled = 'yes'

    description = "Utilisateur ajouté par script python le  {}".format(datetime.datetime.now()) #
    default_password = 'Azerty1#' # Mot de passe par défaut de l'utilisateur à créer
    
    dn = '"CN={},{}"'.format(username, users_ou) # Dans la variable dn, on affecte le nom unique et l'OU de l'utilisant
    groups = '"cn=G_Distant,{}" '.format(groups_ou, groups_ou) # Dans la variable groups, on affecte l'utilisateur dans le groupe G_Distant
    
    # On affecte dans la variable command la ligne de commande qui permet d'ajouter un utilisateur à l'annuaire
    command = 'dsadd user ' \
              '{} ' \                       
              '-sameid "{}" ' \            # Spécifie le nom du gestionnaire de comptes sécurité comme nom de compte unique pour l'utilisateur
              '-upn "{}" ' \               # Spécifie le nom d'utilisateur principal 
              '-fn "{}" ' \                # Spécifie le prénom de l'utilisateur
              '-ln "{}" ' \                # Spécifie le nom de famille de l'utilisateur
              '-display "{}" ' \           # Spécifie le nom d'affichage de l'utilisateur
              '-desc "{}" ' \              # Spécifie la description de l'utilisateur
              '-disabled {} ' \            # Spécifie si dsadd désactive le compte d'utilisateur pour la connexion
              '-pwd {} ' \                 # Spécifie le mot de passe de l'utilisateur
              '-mustchpwd yes ' \          # Spécifie que l'utilisateur doit modifier son mot de passe à la première connexion
              '-pwdneverexpires no ' \     # Spécifie que le mot de passe utilisateur expire
              '-memberof {} ' \            # Spécifie les noms distinctifs des groupes dont l'utilisateur sera membre
              '-acctexpires never ' \      # Spécifie que le compte d'utilisateur n'expire jamais
              ''.format(
                dn,
                username,
                username,
                first_name,
                last_name,
                display_name,
                description,
                disabled,
                default_password,
                groups,
                )
    os.system(command)

# On affecte à la variable reponse 'oui' ou 'non'
reponse = input("Souhaitez-vous ajouter un utilisateur (oui/non)?\n")
reponse = str(reponse) 

# Tant que la réponse est 'oui', on saisie le prénom et le nom de l'utilisateur
# ensuite, on crée le compte utilisateur 
while reponse == 'oui':
    
    prenom = input("Saisissez le prenom de l'utilisateur\n")
    prenom = str(prenom)
    nom = input("Saisissez le nom de l'utilisateur\n")
    nom = str(nom)
    display = prenom + " " + nom
    sameid = prenom[0] + nom
    print("Le nom complet de l'utilisateur est :", display)
    print("Et son nom d'ouverture de session est: ", sameid)
    create_user(sameid,prenom,nom,display,active=True)
    reponse = input("Souhaitez-vous ajouter un autre utilisateur (oui/non)?\n")


os.system("pause")
 
 
