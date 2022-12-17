#
#
# -d, --basedir=PATH
#
#
#
#

from getopt import getopt, GetoptError
from GithubTracker import *

HELP="""
 github-tracker

 A tool for scraping github accounts to see if someone
 created a new repository or there are recent commits.

 Usage: python main.py [OPTIONS ...]

 -h, --help            Show this helptext and exit
 -d, --basedir=PATH    Set alternate base directory
"""


def main(args):

	basedir = None

	try:
		opts,rem = getopt(args, 'hd:',
				['help', 'basedir='])
	except GetoptError as ge:
		print('Error: {}'.format(ge))
		return

	for opt,arg in opts:
		if opt in ('-h', '--help'):
			print(HELP)
			return
		elif opt in ('-d', '--basedir'):
			basedir = arg

	GithubTracker().run(basedir)


if __name__ == '__main__':
	main(sys.argv[1:])
