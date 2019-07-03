#!/usr/bin/env python3
import vk_api
import subprocess as sp
import urllib.request as ur
import urllib.error as ue
from bs4 import BeautifulSoup
from termcolor import colored
from argparse import ArgumentParser as argp

parser = argp()
parser.add_argument("-o", "--out", action="store", dest="out",
                            help="Output file name with phone numbers")
args = parser.parse_args()

def log_vk(login, passwd):
    vk_s = vk_api.VkApi(login, passwd)
    vk_s.auth()
    vk = vk_s.get_api()
    return vk

def get_html_page(url):
    page = ur.urlopen(url)
    return page.read()

def parse_html_pages(html_page, profile):
    soup = BeautifulSoup(html_page, "html.parser")
    body = soup.find("body")
    a_num = body.find("a", class_="si_phone")
    if (a_num != None):
        for num in a_num: number = num
        if (args.out):
            with (open(args.out, "w")) as out_file:
                out_file.write("[%s] Phone number found: %s" %(profile, number))
        else:
            print(colored("[%s] Phone number found: %s" %(profile, number), "green"))
    else:
        #print(colored("[%s] Phone number is not found" %profile, "red"))
        pass

def main():
    offset = 0
    count = 0
    members = []
    try:
        log = str(input("Enter your vk login: "))
        passwd = str(input("Enter vk password: "))
        vk_session = log_vk(log, passwd)
        gr_id = str(input("Enter id of group: "))
        while True:
            resp = vk_session.groups.getMembers(group_id=gr_id, offset=offset)
            members += resp["items"]
            offset += 1000
            if (offset > resp["count"]):
                break
        for id in members:
            #print("https://vk.com/id"+str(id))
            page = get_html_page("https://vk.com/id"+str(id))
            parse_html_pages(page, "https://vk.com/id"+str(id))
    except ue.HTTPError:
        print(colored("[-] Page '%s' is not found!" %url, "red"))
    except ValueError:
        print(colored("[-] This is not a url!", "red"))
    except FileNotFoundError:
        print(colored("[-] No such file: %s" %name, "red"))
    except vk_api.exceptions.AuthError:
        print(colored("[-] Wrong password or login!", "red"))
        print(colored("[-] Or switch-off double-factor auth!", "red"))
    except KeyboardInterrupt:
        print("Exit...")

if (__name__ == '__main__'):
    main()
