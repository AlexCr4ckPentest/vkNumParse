#!/usr/bin/env python3
import urllib.request as ur
import urllib.error as ue
from bs4 import BeautifulSoup
from termcolor import colored
from argparse import ArgumentParser as argp

parser = argp()
parser.add_argument("-f", "--file", action="store", dest="file",
                            help="Input file to parse addresses")
args = parser.parse_args()

def get_html_page(url):
    page = ur.urlopen(url)
    return page.read()

def parse_html_page(html_page):
    soup = BeautifulSoup(html_page, "html.parser")
    body = soup.find("body")
    div = body.find("div")
    a = div.find("a", class_="si_phone")
    if (a != None):
        for num in a: number = num
        print(colored("Phone number found: %s" %number, "green"))
    else:
        print(colored("[-] Phone number is not found", "red"))

def main():
    if (args.file): name = args.file
    try:
        with (open(name, "r")) as file:
            for url in file:
                page = get_html_page(url)
                parse_html_page(page)
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
