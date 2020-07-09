#!/usr/bin/env python
import os
import sys
import pickle
import shutil
import re

usr = os.path.expanduser('/usr')
etc = os.path.expanduser('/etc')
hp = os.path.join(etc, 'hosts')
base = os.path.join(usr, 'share', 'blocker')
act = os.path.join(base, 'act.pkl')

def save(object, fp):
    pickle.dump(object, open(fp, 'wb'))

def load(fp):
    return pickle.load(open(fp, 'rb'))

def export_block(name, fp):
    cp = get_cp(name)
    shutil.copy(cp, fp)

def import_block(name, fp):
    shutil.copy(fp, base)
    activites = get_activity()
    activites[name] = False
    save(activites, act)
    update_block(name)

def get_activity():
    return load(act)

def get_bp(name):
    return os.path.join(base, name + '.block')

def get_cp(name):
    return os.path.join(base, name + '.cont')

def check_dir(fp):
    if not os.path.exists(fp):
        os.makedirs(fp)

def check_base():
    check_dir(base)
    if not os.path.exists(act):
        activity = {'default':False}
        save(activity, act)
        new_block('default', [])

def setup():
    check_base()

def reset():
    os.system('rm -rf ' + str(base))
    setup()

def new_string(name, domains):
    header = '# </blocker=' + str(name) + '>'
    footer = '# <blocker=' + str(name) + '/>'
    block_string = header + '\n'
    for domain in domains:
        block_string += '127.0.0.1	' + domain + '\n'
        block_string += '127.0.0.1	www.' + domain + '\n'
    block_string += footer + '\n'
    return block_string

def new_block(name, domains):
    block_string = new_string(name, domains)
    check_base()
    bp = get_bp(name)
    block_file = open(bp, 'w')
    block_file.write(block_string)
    block_file.close()
    cp = get_cp(name)
    save(set(domains), cp)
    activity = get_activity()
    activity[name] = False
    save(activity, act)

def delete_block(name):
    bp = get_bp(name)
    cp = get_cp(name)
    os.remove(bp)
    os.remove(cp)
    activity = get_activity()
    activity.pop(name)
    save(activity, act)

def add_to_block(name, add_domains):
    cp = get_cp(name)
    old_domains = load(cp)
    add_domains = set(add_domains)
    new_domains = old_domains | add_domains
    save(new_domains, cp)
    update_block(name)

def rem_from_block(name, rem_domains):
    cp = get_cp(name)
    old_domains = load(cp)
    rem_domains = set(rem_domains)
    new_domains = old_domains - rem_domains
    save(new_domains, cp)
    update_block(name)

def clear_block(name):
    cp = get_cp(name)
    save(set(), cp)
    update_block(name)

def see_block(name):
    cp = get_cp(name)
    domains = load(cp)
    active = get_activity()
    if active[name]:
        status = 'Enabled'
    else:
        status = 'Disabled'
    print('Domains in ' + str(name) + ' [' + status + ']:')
    for domain in domains:
        print(' - ' + str(domain))

def see_all():
    active = get_activity()
    for name in active.keys():
        see_block(name)

def rename_block(old_name, new_name):
    old_bp = get_bp(old_name)
    old_cp = get_cp(old_name)
    new_cp = get_cp(new_name)
    domains = load(old_cp)
    os.remove(old_bp)
    os.remove(old_cp)
    save(domains, new_cp)
    update_block(new_name)
    activity = get_activity()
    activity[new_name] = activity[old_name]
    activity.pop(old_name)
    save(activity, act)

def update_block(name):
    cp = get_cp(name)
    domains = load(cp)
    new_block(name, domains)
    update_hosts()

def set_active(name, on):
    activity = get_activity()
    activity[name] = on
    save(activity, act)
    update_hosts()

def see_active(search='*'):
    search = search.replace('*', '.')
    r = re.compile(search)
    activity = get_activity()
    names = list(activity.keys())
    results = list(filter(r.match, names))
    print('Block lists:')
    for name in results:
        space = 40 - len(name)
        if activity[name]:
            blocking = 'Enabled'
        else:
            blocking = 'Disabled'
        print(' - ' + name + space * '.' + blocking)

def enable():
    activity = get_activity()
    for name in list(activity.keys()):
        set_active(name, True)

def disable():
    activity = get_activity()
    for name in list(activity.keys()):
        set_active(name, False)

def update_hosts():
    activity = get_activity()
    header = '\n# </hblock>\n'
    footer = '# <hblock/>\n'
    hosts = open(hp, 'r')
    h_string = hosts.read()
    if h_string.find(header) > -1:
        start = h_string.find(header)
        end = h_string.find(footer) + len(footer)
        old_update = h_string[start:end]
        h_string = h_string.replace(old_update, '')
    h_string += header
    for name in list(activity.keys()):
        if activity[name]:
            bp = get_bp(name)
            b = open(bp, 'r')
            b_string = b.read()
            b.close()
            h_string += b_string
    h_string += footer
    hosts.close()
    hosts = open(hp, 'w')
    hosts.write(h_string)
    hosts.close()

command = sys.argv[1:]
try:
    if command[0] == 'active':
        try:
            see_active(command[1])
        except:
            see_active()
    elif command[0] == 'add':
        name = command[1]
        add_domains = command[2:]
        add_to_block(name, add_domains)
        print('Added ' + str(len(add_domains)) + ' domains to ' + name + '.')
    elif command[0] == 'remove':
        name = command[1]
        rem_domains = command[2:]
        rem_from_block(name, rem_domains)
        print('Removed ' + str(len(rem_domains)) + ' domains from ' + name + '.')
    elif command[0] == 'show':
        name = command[1]
        see_block(name)
    elif command[0] == 'everything':
        see_all()
    elif command[0] == 'set':
        name = command[1]
        enable = command[2]
        if enable == 'on':
            enable = True
            print('Enabled ' + name + '.')
        else:
            enable = False
            print('Disabled ' + name + '.')
        set_active(name, enable)
    elif command[0] == 'new':
        name = command[1]
        domains = command[2:]
        new_block(name, domains)
        print('Created ' + name + ' with ' + str(len(domains)) + ' domains in it.')
    elif command[0] == 'delete':
        name = command[1]
        delete_block(name)
        print('Deleted ' + name + '.')
    elif command[0] == 'rename':
        old_name = command[1]
        new_name = command[2]
        rename_block(old_name, new_name)
        print('Renamed ' + old_name + ' to ' + new_name + '.')
    elif command[0] == 'setup':
        print('Attempting setup.')
        setup()
        print('Setup complete.')
    elif command[0] == 'reset':
        print('Attempting reset.')
        reset()
        print('Reset complete.')
    elif command[0] == 'update':
        print('Forcing update of hosts.')
        update_hosts()
        print('Update of hosts complete.')
    elif command[0] == 'enable':
        enable()
        print('All ' + str(len(get_activity().keys())) + ' block lists enabled.')
    elif command[0] == 'disable':
        disable()
        print('All ' + str(len(get_activity().keys())) + ' block lists disabled.')
    elif command[0] == 'import':
        name = command[1]
        fp = command[2]
        import_block(name, fp)
        print('Imported ' + name + ' from ' + fp + '.')
    elif command[0] == 'export':
        name = command[1]
        fp = command[2]
        export_block(name, fp)
        print('Exported ' + name + ' to ' + fp + '.')
    elif command[0] == 'help':
        print(
            'Available commands:\n' +
            ' - active..................................Shows which block lists are active.\n' +
            ' - add [block list] [domains]..............Adds domains to block list.\n' +
            ' - remove [block list] [domains]...........Removes domains from block list.\n' +
            ' - show [block list].......................Shows all the domains in the block list.\n' +
            ' - everything..............................Shows all domains in all block lists.\n' +
            ' - set [block list] [on/off]...............Turns the block list on or off.\n' +
            ' - enable..................................Turns on all block lists.\n' +
            ' - disable.................................Turns off all block lists.\n' +
            ' - new [block list] [domains]..............Makes a new block list with specified domains.\n' +
            ' - delete [block list].....................Deletes block list.\n' +
            ' - rename [block list] [new name]..........Renames block list to the new name.\n' +
            ' - setup...................................Automatically sets up hblock on first install.\n' +
            ' - reset...................................Reset hblock to its default state.\n' +
            ' - update..................................Forces update of hosts file.\n' +
            ' - import [block list] [path]..............Imports block list with specified name.\n' +
            ' - export [block list] [path]..............Exports block list to specified path.\n' +
            ' - help....................................Shows available commands.'
        )
    else:
        print("Invalid command. Try entering 'sudo hblock help' to see available commands.")
except:
    print("Invalid command. Try entering 'sudo hblock help' to see available commands.")