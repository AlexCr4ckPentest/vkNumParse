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
from time import ctime, sleep

parser = argp()

parser.add_argument("-w", "--write", action="store", dest="out_file",
					help="Filename to write-out result")

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
	return soup.find("body").find_all("a", class_="si_phone")

def get_group_members(vk_session, grp_id, group_m_list):
	offset = 0
	count = 0
	while (True):
		resp = vk_session.groups.getMembers(group_id=grp_id, offset=offset)
		group_m_list += resp["items"]
		offset += 1000
		if (offset > resp["count"]):
			break

def main():
	# Объявление переменных и списков
	grp_members = []
	nums_list = []
	have_num = 0
	
	# Авторизация
	print(colored("-----------------------------------------", "cyan"))
	log = str(input(colored("[Auth] Enter your vk login: ", "cyan")))
	passwd = str(input(colored("[Auth] Enter vk password: ", "cyan")))
	vk_session = log_vk(log, passwd)
	clear_scr()
	print(colored("[+] Successful auth!", "green"))
	
	# Добыча id группы и всех ее пользователей
	grp_id = str(input(colored("[id] Enter id of group: ", "cyan")))
	get_group_members(vk_session, grp_id, grp_members)
	print(colored("[+] Found %d members!" %len(grp_members), "green"))
	sleep(2)
	clear_scr()
	print(colored("[+] Parsing startetd at: %s" %ctime(), "green"),
		colored("\n[!] Please be patient :)", "yellow"))
	print(colored("-------------------------------------------------", "cyan"))
	
	# Парсинг всех страниц
	for id in grp_members:
		html_page = ureq.urlopen("https://vk.com/id"+str(id))
		a_num = parse_page(html_page.read())
		print(colored("[*] Scanning "+"https://vk.com/id"+str(id), "cyan"),
				colored("(Found: %d)" %have_num, "cyan"), end="\r")
		if (len(a_num) != 0):
			nums_list.append(
				[(lambda a_len: a_num[0].get("href")+"/"+a_num[1].get("href") if a_len == 2
					else a_num[0].get("href"))(len(a_num)), "https://vk.com/id"+str(id)]
			)
			have_num += 1

	clear_scr()
	print(colored("[+] Parsing ended at: %s" %ctime(), "green"))
	if (len(nums_list) != 0):
		print(colored("[+] Found %d numbers" %have_num, "green"))
		if (args.out_file):
			with open(args.out_file, "w") as file:
				file.write("Report of parsing at: "+ctime()+"\n")
				for i in range(len(nums_list)):
					for j in range(len(nums_list[i])):
						file.write(nums_list[i][j]+"\t")
					file.write("\n")
		else:
			for i in range(len(nums_list)):
				for j in range(len(nums_list[i])):
					print(colored(nums_list[i][j], "green"), end="\t")
				print(end="\n")

	else:
		print(colored("[-] Found %d numbers" %have_num, "red"))

if (__name__ == "__main__"):
	try:
		main()
	except uerr.HTTPError:
		print(colored("[-] Page not found!", "red"))
		exit(1)
	except ValueError:
		print(colored("[-] This is not a url!", "red"))
		exit(1)
	except vk_api.exceptions.AuthError:
		print(colored("[-] Wrong password or login!", "red"))
		print(colored("[-] Or switch-off double-factor auth!", "red"))
		exit(1)
	except KeyboardInterrupt:
		print(colored("\n[-] Interrupted! Exiting...", "red"))
		exit(1)