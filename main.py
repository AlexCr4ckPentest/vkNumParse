#!/usr/bin/env python3
# Parsing phone numbers from vk groups
# Coded by: AlexCr4ckPentest
# https://github.com/AlexCr4ckPentest/vkNumParse

from os import system, sys
import vk_api
import urllib.request as ureq
import urllib.error as uerr
from bs4 import BeautifulSoup as BS
from termcolor import colored
from argparse import ArgumentParser as argp

parser = argp()

parser.add_argument("-v", "--vebrose", action="store_true",
					help="Show all information")

parser.add_argument("-w", "--write", action="store", dest="out_file",
					help="Filename to write-out")

args = parser.parse_args()

def clear_scr():
	if (sys.platform == "win32"):
		system("cls")
	else:
		system("clear")

def log_vk(login, password):
	vk = vk_api.VkApi(login, password)
	vk.auth()
	return vk.get_api()

def parse_page(page):
	soup = BS(page, "lxml")
	a_num = soup.find("body").find_all("a", class_="si_phone")
	#print(a_num)
	return a_num

def main():
	# Объявление переменных и списков
	grp_members = []
	nums_list = []
	nums_refs = {}
	count = 0
	offset = 0
	have_num = 0
	have_two_num = 0
	
	# Авторизация
	print(colored("-----------------------------------------", "cyan"))
	log = str(input(colored("[Auth] Enter your vk login: ", "cyan")))
	passwd = str(input(colored("[Auth] Enter vk password: ", "cyan")))
	vk_session = log_vk(log, passwd)
	clear_scr()
	print(colored("[+] Successful auth!", "green"))
	
	# Добыча id группы и всех ее пользователей
	grp_id = str(input(colored("[id] Enter id of group: ", "cyan")))
	while (True):
		resp = vk_session.groups.getMembers(group_id=grp_id, offset=offset) # get group members
		grp_members += resp["items"]
		offset += 1000
		if (offset > resp["count"]):
			break
	print(colored("[+] Found %d members!" %len(grp_members), "green"))
	
	# Парсинг всех страниц
	for id in grp_members:
		url = ureq.urlopen("https://vk.com/id"+str(id))
		nums_list.append(parse_page(url.read())) # Добавление телефонов в список
	
if (__name__ == "__main__"):
	try:
		main()
	except uerr.HTTPError:
		print(colored("[-] Page is not found!", "red"))
	except ValueError:
		print(colored("[-] This is not a url!", "red"))
	except vk_api.exceptions.AuthError:
		print(colored("[-] Wrong password or login!", "red"))
		print(colored("[-] Or switch-off double-factor auth!", "red"))