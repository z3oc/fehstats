#!/usr/bin/env python3

import json, argparse, prettytable, requests, html

# URL_hmdir = "https://s3.us-east-2.amazonaws.com/gamepress-json/fe/"
URL_hmdir = "https://fireemblem.gamepress.gg/sites/fireemblem/files/feh-jsons/"
URL_3star = URL_hmdir + "heroes-3star.json"
URL_4star = URL_hmdir + "heroes-4star.json"
URL_5star = URL_hmdir + "heroes-5star.json"

# parse args
parser = argparse.ArgumentParser(description="Collect FEH stats from GamePress")
parser.add_argument('-c')
parser.add_argument('-s', default='5')
parser.add_argument('other', nargs='*')
args = parser.parse_args()
character, stars, other = args.c, args.s, args.other 

if character: character = character.replace("'", "&#039;").casefold()
for i in range(len(other)):
    other[i] = other[i].replace("'", "&#039;").casefold()

# update json files
if 'update' in other:
    with open(URL_3star[-10:], 'w') as f3, open(URL_4star[-10:], 'w') as f4, open(URL_5star[-10:], 'w') as f5:
        f3.write(requests.get(URL_3star).text)
        f4.write(requests.get(URL_4star).text)
        f5.write(requests.get(URL_5star).text)
    print('Json files updated.')

# load json file
jsondata = None
filename = stars + "star.json"
with open(filename, 'r') as f:
    jsondata = json.load(f)

character_list = sorted([hero['title'] for hero in jsondata])

if 'list' in other:
    for c in character_list: print(html.unescape(c))

tmp = ({c.casefold() for c in character_list} & set(other))
if tmp: character = tmp.pop()
if not character: exit()

# adjust keys according to rarity ... their naming patterns are inconsistent
key_hp = 'field_hp_level_1_middle'
key_atk = 'field_atk_level_1_middle'
key_spd = 'field_spd_level_1_middle'
key_def = 'field_def_level_1_middle'
key_res = 'field_res_level_1_middle'
if stars == '4':
    key_hp += '_4star'
    key_atk += '_4star'
    key_spd += '_4star'
    key_def += '_4star'
    key_res += '_4star'
if stars == '3':
    key_hp = 'field_hp_level_1_mid_3star'
    key_atk = 'field_attack_level_1_mid_3star'
    key_spd = 'field_speed_level_1_mid_3star'
    key_def = 'field_def_level_1_mid_3star'
    key_res = 'field_res_level_1_mid_3star'

# get target hero data
targethero = None
for hero in jsondata:
    if hero['title'].casefold() != character.casefold():
        continue
    targethero = hero 
if not targethero:
    print("Data not found.")
    exit()

# output
print("Character:", html.unescape(targethero['title']))
print("Stars:", stars)
print("Neutral Stats at Lv.1:")
t = prettytable.PrettyTable(['HP','ATK','SPD','DEF','RES'])
t.add_row([targethero[key_hp], targethero[key_atk], targethero[key_spd], targethero[key_def], targethero[key_res]])
print(t)
print("Neutral Stats at Lv.40:")
t.del_row(0)
t.add_row([targethero['field_hp_level_40_middle'], targethero['field_atk_level_40_middle'], targethero['field_spd_level_40_middle'], targethero['field_def_level_40_middle'], targethero['field_res_level_40_middle']])
print(t)
