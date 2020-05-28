#!/usr/bin/env python3

import os
import vk_api
import urllib.request as ureq
import urllib.error as uerr

from time import ctime
from termcolor import colored
from bs4 import BeautifulSoup
from argparse import ArgumentParser

VK_PAGE_PREFIX = "https://vk.com/id"

arg_parser = ArgumentParser()
arg_parser.add_argument("-o", "--out", action="store", dest="out_file", help="output filename")
args = arg_parser.parse_args()


def clear_scr(): os.system("clear")


def get_vk_api_session(login, password):
    vk = vk_api.VkApi(login, password)
    vk.auth()
    return vk.get_api()


def parse_page(page):
    page_parser = BeautifulSoup(page, "lxml")
    phone_number_tag = page_parser.find("body").find_all("a", class_="si_phone")
    return phone_number_tag


def get_group_members(vk_session, group_id):
    offset = 0
    members = []

    while True:
        resp = vk_session.groups.getMembers(group_id=group_id, offset=offset)
        members.append(resp["items"])
        offset += 1000
        if offset > resp["count"]:
            break

    return members


def write_to_file(filename, nums_list):
    if nums_list:
        with open(filename, "w") as file:
            file.write(f"Report of parsing at: {ctime()}\n")
            for i in range(len(nums_list)):
                for j in range(len(nums_list[i])):
                    file.write(nums_list[i][j]+"\t")
                file.write("\n")


def main():
    if not args.out_file or not os.sys.argv:
        arg_parser.print_help()
        exit(0)

    have_num = 0
    nums_list = []
    output_file = args.out_file

    try:
        log = input(colored("[Auth] Enter your vk login: ", "cyan"))
        passwd = input(colored("[Auth] Enter vk password: ", "cyan"))
        vk_session = get_vk_api_session(log, passwd)

        clear_scr()
        print(colored("[+] Successful authorization!", "green"))

        grp_id = input(colored("[id] Enter id of group: ", "cyan"))
        members_lst = get_group_members(vk_session, grp_id)
        print(colored(f"[+] Found {len(members_lst)} members!", "green"))

        clear_scr()
        print(colored(f"[+] Parsing startetd at: {ctime()}", "green"))
        print(colored("[!] Please be patient :)", "yellow"))

        for id in members_lst:
            html_page = ureq.urlopen(VK_PAGE_PREFIX+str(id))
            phone_number_tag = parse_page(html_page.read())
            print(colored(f"[*] Scanning {VK_PAGE_PREFIX+str(id)}", "cyan"), colored(f"(Found: {have_num})", "cyan"), end="\r")
            if phone_number_tag:
                nums_list.append(
                    [(lambda a_len: phone_number_tag[0].get("href")+"/"+phone_number_tag[1].get("href") if a_len == 2
                        else phone_number_tag[0].get("href"))(len(phone_number_tag)), VK_PAGE_PREFIX+str(id)]
                )
                have_num += 1

        clear_scr()
        print(colored(f"[+] Parsing finished at: {ctime()}", "green"))
        print(colored(f"[+] Found {have_num} numbers", "green"))
        write_to_file(output_file, nums_list)

    except uerr.HTTPError:
        print(colored("\n[-] An HTTP error has occurred! The page may not be found!", "red"))
        write_to_file(output_file, nums_list)
        exit(1)

    except ValueError:
        print(colored("[-] Error: A value error has occurred! This is not a url!", "red"))
        exit(2)

    except vk_api.exceptions.AuthError:
        print(colored("[-] Error: An authorization error has occurred! Wrong password or login!", "red"))
        print(colored("[-] Error: Or turn off two-factor authorization!", "red"))
        exit(3)

    except vk_api.exceptions.Captcha:
        print(colored("[-] Error: An authorization error has occurred! Captcha needed!", "red"))
        exit(4)

    except KeyboardInterrupt:
        print(colored("\n[-] Interrupt signal handled! Exiting...", "red"))
        write_to_file(output_file, nums_list)
        exit(5)

if __name__ == "__main__":
    main()
