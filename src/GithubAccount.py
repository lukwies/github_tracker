import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import tz
import logging
import os

class GithubAccount:

	def __init__(self, username):
		self.username    = username    	# Github username
		self.realname    = ""          	# Real name
		self.userinfo    = ""          	# User info/description
		self.location    = ""          	# User location
		self.followers   = 0           	# Number of followers
		self.following   = 0           	# Number of following
		self.avatar_url  = ""          	# Url to avatar image
		self.avatar_file = ""		# Local path to avatar file
		self.repos       = []          	# List with repositories
		self.last_commit = None		# Last commit date


	def download(self, avatar_directory=None):

		logging.info(f"Downloading account '{self.username}' ...")

		url  = f"https://github.com/{self.username}?tab=repositories"
		soup = self._get_soup(url)

		if not soup:
			return False

		self.realname  = self._parse_real_name(soup)
		self.userinfo  = self._parse_user_info(soup)
		self.location  = self._parse_user_location(soup)
		self.followers = self._parse_followers(soup)
		self.following = self._parse_following(soup)
		self.avatar_url= self._parse_avatar_url(soup)
		self.repos     = self._parse_repositories(soup)

		# download/save avatar image
		self._download_avatar(avatar_directory)

		# Store last commit date (If there's any repo)
		if len(self.repos) > 0:
			self.last_commit = self.repos[0]['last_update']

		return True

	def commited_today(self):
		'''
		Returns True if any repository of this account has
		been updated.
		'''
		if not self.has_repos():
			return False
		elif self.repos[0]['last_update'].date() != datetime.today().date():
			return False
		else:
			return True


	def has_repos(self):
		'''
		Returns True if account has any repositories.
		'''
		return True if len(self.repos) > 0 else False


	def print(self):
		print(f'Username:  {self.username}')
		print(f'Realname:  {self.realname}')
		print(f'Userinfo:  {self.userinfo}')
		print(f'Location:  {self.location}')
		print(f'Follower:  {self.followers}')
		print(f'Following: {self.following}')
		print(f'Avatar:    {self.avatar}')
		print('Repositories')
		print(self.repos)




	def _parse_repositories(self, soup):
		'''
		Parse information for all repositories.
		Return:
		    List with repositories as dictionaries
		'''

		def get_localtime_from_utcstr(timestr):
			''' Parses UTC time string in format "%Y-%m-%dT%H:%M:%SZ" to localtime. '''
			dt = datetime.strptime(timestr, "%Y-%m-%dT%H:%M:%SZ")
			dt = dt.replace(tzinfo=tz.gettz('UTC'))
			return dt.astimezone(tz.tzlocal())

		repos = []

		# Parse repository infos from html
		for li in soup.find_all('li', {'itemprop':'owns'}):
			repo = {}
			repo['name'] = li.h3.a.get_text().strip() # Name of repository
			repo['type'] = li.attrs['class'][8]       # source or fork ?
			repo['url']  = li.h3.a['href']            # Url of repository

			# Get programming language
			x = li.find('span', {'itemprop':'programmingLanguage'})
			repo['language'] = x.get_text() if x != None else ""

			# Get last commit time and convert to localtime
			x = li.find('relative-time')['datetime'] #.get_text()
			repo['last_update'] = get_localtime_from_utcstr(x)

			# Get url where repo is forked from
			x = li.find('a', {'class', 'Link--muted'})
			repo['forked_from'] = '' if not x else x['href']

			# Get repository descriptioin
			x = li.find('p', {'class':'col-9', 'itemprop':'description'})
			repo['description'] = '' if not x else x.get_text().strip()

			repos.append(repo)

		# If there's a next page with repository, download/parse it ...
		x = soup.find('a', {'class':'next_page', 'rel':'next'})
		if x:
			url  = 'https://github.com' + x['href']
			soup = self._get_soup(url)
			repos.extend(self._parse_repositories(soup))

		return repos


	def _parse_avatar_url(self, soup):
		img = soup.find('img', {'alt':'Avatar'})
		return '' if not img else img['src']

	def _parse_real_name(self, soup):
		name = soup.find('span', {'class':'p-name'})
		return '' if not name else name.get_text().strip()

	def _parse_user_info(self, soup):
		info = soup.find('div', {'class':'p-note'})
		return '' if not info else info['data-bio-text']

	def _parse_followers(self, soup):
		x = soup.find_all('span', {'class':'text-bold color-fg-default'})
		return 0 if not x else int(x[0].get_text())

	def _parse_following(self, soup):
		x = soup.find_all('span', {'class':'text-bold color-fg-default'})
		return 0 if not x else int(x[1].get_text())

	def _parse_user_location(self, soup):
		loc = soup.find('span', {'class':'p-label'})
		return '' if not loc else loc.get_text()

	def _get_soup(self, url):
		resp = requests.get(url)

		if resp.status_code != 200:
			print(f"! Error: Failed to send request to {url}")
			print(f"         Status-code={resp.status_code}")
			return None

		return BeautifulSoup(resp.text, 'html.parser')

	def _download_avatar(self, avatar_directory):
		self.avatar_file = os.path.join(avatar_directory, self.username + '.jpg')

		# Only download avatar image if it does not already exist
		if not os.path.isfile(self.avatar_file):

			logging.info(f"Downloading avatar to '{self.avatar_file}' ...")
			img_data = requests.get(self.avatar_url).content

			with open(self.avatar_file, 'wb') as file:
				file.write(img_data)

