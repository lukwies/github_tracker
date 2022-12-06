import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import tz


class GithubAccount:
	def __init__(self, username, avatar_path=''):
		self.username  = username    # Github username
		self.name      = ""          # Real name
		self.info      = ""          # User info/description
		self.location  = ""          # User location
		self.followers = 0           # Number of followers
		self.following = 0           # Number of following
		self.avatar    = avatar_path # Local path to avatar
		self.repos     = []          # List with repositories

	def download(self):
		url  = f"https://github.com/{self.username}?tab=repositories"
		resp = requests.get(url)

		if resp.status_code != 200:
			print(f"! Error: Failed to send request to {url}")
			print(f"         Status-code={resp.status_code}")
			return False

		soup = BeautifulSoup(resp.text, 'html.parser')

		self.name      = self._parse_real_name(soup)
		self.info      = self._parse_user_info(soup)
		self.location  = self._parse_user_location(soup)
		self.followers = self._parse_followers(soup)
		self.following = self._parse_following(soup)
		self.repos     = self._parse_repositories(soup)

		# TODO: download/save avatar image
		#img_data = requests.get(self._parse_avatar_url(soup)).content
		#with open(file, 'wb') as file:
		#    file.write(img_data)
		return True


	def print(self):
		print(f'Username:  {self.username}')
		print(f'Realname:  {self.name}')
		print(f'Userinfo:  {self.info}')
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
			repo['lastupdate'] = get_localtime_from_utcstr(x)

			repos.append(repo)

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
