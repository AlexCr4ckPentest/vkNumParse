#!/usr/bin/env python3
# Parsing phone numbers from vk groups
# Coded by: AlexCr4ckPentest
# https://github.com/AlexCr4ckPentest/vkNumParse

import vk_api
import urllib.request as ur
import urllib.error as ue
from bs4 import BeautifulSoup
from termcolor import colored
from argparse import ArgumentParser as argp

parser = argp()
parser.add_argument("-o", "--out", action="store", dest="out",
                            help="Output file name with phone numbers")
args = parser.parse_args()

have_num = 0

def log_vk(login, passwd):
    vk_s = vk_api.VkApi(login, passwd)
    vk_s.auth()
    vk = vk_s.get_api()
    return vk

def get_html_page(url):
    page = ur.urlopen(url)
    return page.read()

def parse_html_pages(html_page, profile):
    soup = BeautifulSoup(html_page, "lxml")
    body = soup.find("body")
    a_num = body.find("a", class_="si_phone")
    if (a_num != None):
        for num in a_num: number = num
        if (args.out):
            with (open(args.out, "a")) as out_file:
                out_file.write("[%s] Phone number found: %s\n" %(profile, number))
        else:
            print(colored("[%s] Phone number found: %s" %(profile, number), "green"))
        global have_num
        have_num += 1
    else:
        # Uncomment next line if you want outputting of profiles without phone number
        #print(colored("[%s] Phone number is not found" %profile, "red"))
        pass

def main():
    global have_num
    offset = 0
    count = 0
    members = []
    try:
        log = str(input(colored("[Auth] Enter your vk login: ", "cyan")))
        passwd = str(input(colored("[Auth] Enter vk password: ", "cyan")))
        vk_session = log_vk(log, passwd)
        grp_id = str(input(colored("Enter id of group: ", "cyan")))
        while (True):
            resp = vk_session.groups.getMembers(group_id=grp_id, offset=offset) # get group members
            members += resp["items"]
            offset += 1000
            if (offset > resp["count"]):
                break
        print(colored("[+] Found %d members!" %len(members), "green"))
        for id in members:
            #print("https://vk.com/id"+str(id)) # for test only!
            page = get_html_page("https://vk.com/id"+str(id))
            parse_html_pages(page, "https://vk.com/id"+str(id))
        print(colored("[+] Found %d members with phone number!" %have_num, "green"))
    except ue.HTTPError:
        print(colored("[-] Page '%s' is not found!" %url, "red"))
    except ValueError:
        print(colored("[-] This is not a url!", "red"))
    except vk_api.exceptions.AuthError:
        print(colored("[-] Wrong password or login!", "red"))
        print(colored("[-] Or switch-off double-factor auth!", "red"))
    except KeyboardInterrupt:
        print("Exit...")

if (__name__ == '__main__'):
    main()
