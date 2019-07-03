#!/usr/bin/env python3
'''import vk_api'''
import subprocess as sp
import urllib.request as ur
import urllib.error as ue
from bs4 import BeautifulSoup
from termcolor import colored
from argparse import ArgumentParser as argp

parser = argp()
parser.add_argument("-f", "--file", action="store", dest="file",
                            help="Input file to parse addresses")
parser.add_argument("-o", "--out", action="store", dest="out",
                            help="Output file name with phone numbers")
args = parser.parse_args()

'''
def log_vk(login, passwd):
    try:
        vk_s = vk_api.VkApi(login, passwd)
        vk_s.auth()
        vk = vk_s.get_api()
        return vk
    except vk_api.exceptions.AuthError:
        print(colored("[-] Wrong password or login!", "red"))
        print(colored("[-] Or switch-off double-factor auth!", "red"))
'''

def get_html_page(url):
    page = ur.urlopen(url)
    return page.read()

def parse_html_pages(html_page, prof):
    soup = BeautifulSoup(html_page, "html.parser")
    body = soup.find("body")
    a_num = body.find("a", class_="si_phone")
    if (a_num != None):
        for num in a_num: number = num
        if (args.out):
            with (open(args.out, "w")) as out_file:
                out_file.write("[%s] Phone number found: %s" %(prof, number))
        else:
            print(colored("[%s] Phone number found: %s" %(prof, number), "green"))
    else:
        pass
        #print(colored("[%s] Phone number is not found" %prof, "red"))

def main():
    if (args.file): name = args.file
    else:
        parser.print_help()
        exit(1)
    try:
        with (open(name, "r")) as file:
            for url in file:
                page = get_html_page(url)
                parse_html_pages(page, url.rstrip("\n"))
    except ue.HTTPError:
        print(colored("[-] Page '%s' is not found!" %url, "red"))
    except ValueError:
        print(colored("[-] This is not a url!", "red"))
    except FileNotFoundError:
        print(colored("[-] No such file: %s" %name, "red"))
    except KeyboardInterrupt:
        print("Exit...")

if (__name__ == '__main__'):
    main()
