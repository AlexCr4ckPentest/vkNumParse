#!/usr/bin/env python3

import os
import vk_api
import urllib.request as ureq
import urllib.error as uerr

from getpass import getpass
from time import ctime
from termcolor import colored
from bs4 import BeautifulSoup
from argparse import ArgumentParser

VK_PAGE_PREFIX = "https://vk.com/id"

arg_parser = ArgumentParser()
arg_parser.add_argument("-o", "--out", action="store", dest="out_file", help="output filename")
args = arg_parser.parse_args()


def clear_scr():
    if os.sys.platform == "win32":
        os.system("cls")
    else:
        os.system("clear")


def get_vk_api_session(login: str, password: str):
    vk = vk_api.VkApi(login, password)
    return vk.auth().get_api()


def parse_page(page):
    page_parser = BeautifulSoup(page, "lxml")
    phone_number_tag = page_parser.find("body").find_all("a", class_="si_phone")
    return phone_number_tag


def get_group_members(vk_session, group_id: int):
    offset = 0
    members = []
    while True:
        resp = vk_session.groups.getMembers(group_id=group_id, offset=offset)
        members.append(resp["items"])
        offset += 1000
        if offset > resp["count"]:
            break
    return members


def write_to_file(filename, nums_list: list):
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
        login = input(colored("[Auth]", "cyan", attrs=["bold"]) + " Enter your login: ")
        password = getpass(colored("[Auth]", "cyan", attrs=["bold"]) + " Enter your password: ")
        vk_session = get_vk_api_session(login, password)

        clear_scr()
        print(colored("[+]", "green", attrs=["bold"]), "Successful authorization!")

        grp_id = input(colored("[id]", "cyan", attrs=["bold"]) + " Enter target group id: ")
        group_members = get_group_members(vk_session, grp_id)
        print(colored("[+]", "green", attrs=["bold"]), f"Found {len(group_members)} members!")

        clear_scr()
        print(colored("[+]", "green", attrs=["bold"]), "Parsing startetd at:", ctime())
        print(colored("[!]", "yellow", attrs=["bold"]), "Please be patient :)")

        for _id in group_members:
            html_page = ureq.urlopen(VK_PAGE_PREFIX+str(_id))
            phone_number_tag = parse_page(html_page.read())
            print(colored("[*]", "cyan", attrs=["bold"]), f"Scanning {VK_PAGE_PREFIX+str(_id)}",
                    colored(f"(Found: {have_num})", "cyan", attrs=["bold"]), end="\r")
            if phone_number_tag:
                nums_list.append(
                    [(lambda a_len: phone_number_tag[0].get("href")+"/"+phone_number_tag[1].get("href") if a_len == 2
                        else phone_number_tag[0].get("href"))(len(phone_number_tag)), VK_PAGE_PREFIX+str(_id)]
                )
                have_num += 1

        clear_scr()
        print(colored("[+]", "green", attrs=["bold"]), "Parsing finished at:", ctime())
        print(colored("[+]", "green", attrs=["bold"]), f"Found {have_num} numbers")

    except uerr.HTTPError:
        print(colored("[-]", "red", attrs=["bold"]), "An HTTP error has occurred! The page may not be found!")
        exit(1)

    except ValueError:
        print(colored("[-]", "red", attrs=["bold"]), "Error: A value error has occurred! This is not a url!")
        exit(2)

    except vk_api.exceptions.AuthError:
        print(colored("[-]", "red", attrs=["bold"]), "Error: An authorization error has occurred! Wrong login or password")
        print(colored("[-]", "red", attrs=["bold"]), "Or switch-off your double factor authorization!")
        exit(3)

    except vk_api.exceptions.Captcha:
        print(colored("[-]", "red", attrs=["bold"]), "Error: An authorization error has occurred! Captcha needed!")
        exit(4)

    except KeyboardInterrupt:
        print(colored("[!]", "yellow", attrs=["bold"]), "Interrupt signal handled! Exiting...")
        exit(5)
    finally:
        write_to_file(output_file, nums_list)


if __name__ == "__main__":
    main()
