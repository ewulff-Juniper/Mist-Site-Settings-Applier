import json
import os.path
import datetime
import mistapi
import UIToolsP3
import sys
import getopt

env_file_path = "./mist_env"
settings_dir_path = './settings_files/'
pulled_settings_dir_path = './settings_files/pulled_settings_files/'

def build_session():
    #Build session, preferably with env file
    if os.path.isfile(env_file_path):
        session = mistapi.APISession(env_file=env_file_path)
    else:
        print('Could not find mist_env file at '+env_file_path+'. Consider adding one to make log in easier')
        session = mistapi.APISession()
    return session

def get_org_id(no_env_file=False):
    #Check of the org idea is in the env file
    if not no_env_file:
        if not os.path.isfile(env_file_path):
            print('Could not find mist_env file. Consider adding one with MIST_ORG_ID')
        else:
            f = open(env_file_path, 'r')
            for l in f:
                if l.startswith('MIST_ORG_ID = '):
                    org_id = l[14:50]
                    return org_id
            print("Could not find MIST_ORG_ID in mist_env file, consider adding it")

    org_id = mistapi.cli.select_org(mist_session)[0]
    return org_id

def pull_site_settings():
    UIToolsP3.printSubHeader('Pull Site Settings')

    #Select sites and pull
    site_ids = mistapi.cli.select_site(mist_session, org_id=org_id, allow_many=True)
    if len(site_ids) > 1:
        org_name = mistapi.api.v1.orgs.orgs.getOrg(mist_session, org_id).data['name']
        dir_name = org_name+datetime.datetime.now().strftime('%b-%d-%Y_%H-%M-%S')
        path = pulled_settings_dir_path+dir_name+'/'
        os.mkdir(path)
    else:
        path = pulled_settings_dir_path

    for site_id in site_ids:
        site_settings = mistapi.api.v1.sites.setting.getSiteSetting(mist_session, site_id)
        site_info = mistapi.api.v1.sites.sites.getSiteInfo(mist_session, site_id) #Site info is just for site name for file name
        file_name = site_info.data['name']+'__'+datetime.datetime.now().strftime('%b-%d-%Y_%H-%M-%S')+'.json' #Name file with date/time
        with open(path+file_name, 'w+') as f:
            f.write(json.dumps(site_settings.data, indent=4))

def push_site_settings():
    UIToolsP3.printSubHeader('Push Site Settings')

    #Find and list files, user named files first
    l1 = []
    l2 = []
    for f in os.listdir(settings_dir_path):
        if os.path.isfile(settings_dir_path+f):
            if '__' in f:
                l2.append(f)
            else:
                l1.append(f)
    files = l1 + l2

    #Select and load a file
    sel_file = UIToolsP3.getFromNumberdList(files)
    with open(settings_dir_path+sel_file, 'r') as of:
        json_data = json.load(of)

    #Select and apply to sites
    site_ids = mistapi.cli.select_site(mist_session, org_id=org_id, allow_many=True)
    for site_id in site_ids:
        response = mistapi.api.v1.sites.setting.updateSiteSettings(mist_session, site_id, json_data)
        site_info = mistapi.api.v1.sites.sites.getSiteInfo(mist_session, site_id)
        print(site_info.data['name']+' status code: '+str(response.status_code))

def change_org():
    #If use wants to change the org then we shouldn't use the env file
    get_org_id(no_env_file=True)

def print_org():
    #Get org name and print
    getOrg = mistapi.api.v1.orgs.orgs.getOrg(mist_session, org_id)
    UIToolsP3.printSubHeader('Current Org: '+getOrg.data['name'])


try:
    opts, args = getopt.getopt(sys.argv[1:], 'e:', ['env_file='])
    print(sys.argv)
except getopt.GetoptError as err:
    print("Error with system arguments. Options are -e or --env_file to specify environment file")
    print(err)
    quit()
for opt, arg, in opts:
    print('opt: '+opt+', arg: '+arg)
    if opt in ('-e', '--env_file'):
        env_file_path = arg
    else:
        print("Unhandled argument: "+opt)

#Set mist_session and org_id globals
UIToolsP3.printHeader('Mist Site Settings Applier')
mist_session = build_session()
mist_session.login()
org_id = get_org_id()

#Build main menu obj
main_menu = UIToolsP3.Menu('Main Menu')
main_menu.menuOptions = {'Pull Site Settings': pull_site_settings, 'Push Site Settings': push_site_settings, 'Change Org': change_org, 'Quit': 'Quit'}
main_menu.print_func = print_org

main_menu.show()
