
#def send_command(command):
#! /usr/bin/python3.9
# -*- coding:utf-8 -*-

import datetime  
import os        
import ldap
import pexpect     


conn = ldap.initialize('ldap://127.0.0.1')
conn.protocol_version = 3
conn.set_option(ldap.OPT_REFERRALS, 0)
conn.simple_bind_s('Administrateur@entreprise.lan','Openclassrooms#')

domain_controller = 'DC=entreprise,DC=lan'
users_ou = 'OU=Local,OU=Employee,{}'.format(domain_controller)
groups_ou = 'OU=Employee_Groups,{}'.format(domain_controller)


def create_user(username, first_name, last_name, active=False):
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

    description = "Utilisateur ajouté par script python le  {}".format(datetime.datetime.now())
    default_password = 'Azerty1#' 

    dn = '"CN={},{}"'.format(username, users_ou)
    groups = '"cn=G_Local,{}" '.format(groups_ou, groups_ou)
             
    command = 'dsadd user ' \
              '{} ' \
              '-samid "{}" ' \
              '-upn "{}" ' \
              '-fn "{}" ' \
              '-ln "{}" ' \
              '-desc "{}" ' \
              '-disabled {} ' \
              '-pwd {} ' \
              '-mustchpwd yes ' \
              '-pwdneverexpires no ' \
              '-memberof {} ' \
              '-acctexpires never ' \
              ''.format(
                dn,
                username,
                username,
                first_name,
                last_name,
                description,
                disabled,
                default_password,
                groups,
                )
    os.system(command)
    

file = open('users.csv', 'r')

for line in file:
    users_paramaters_list = line.strip().split(",")
    
    users_paramaters = {}
    users_paramaters['username'] = users_paramaters_list[0]
    users_paramaters['first_name'] = users_paramaters_list[1]
    users_paramaters['last_name'] = users_paramaters_list[2]
    
    create_user(users_paramaters['username'],users_paramaters['first_name'],users_paramaters['last_name'],active=True)
file.close()   

os.system("pause")
 
 
