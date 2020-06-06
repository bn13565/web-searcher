# WEBSITE SEARCHER

The project implements a website searcher that looks up
all the urls from:

https://www.notion.so/Website-Searcher-3d340bd1471e4a6b93af6103eb517061
and finds out whether a given search term exists in the retrieved
text response. The results are written in a results.txt file in the 
following form:
URL : string  BOOLEAN (True or False) : Search term appears or not.

The url request service is implemented using concurrency with the 
asyncio library.

# Prerequisites:
	Python 3.6

# Running:
	Command line : python websearcher.py
	Input the SEARCH term to look up and hit enter

# Authors:
	Bryan Kamau - bkn7@cornell.edu

# Acknowledgements:
	https://realpython.com/async-io-python/
	https://stackoverflow.com/questions/28768530/certificateerror-hostname-doesnt-match

# Bugs:
	Downgraded to use python3.6 because the following error 
	https://github.com/Rapptz/discord.py/issues/423#issuecomment-272093801
	couldn't be fixed by trying most of the suggestion I got online.
	Downgrading from python 3.8 to 3.6 and using the patch acknowledged above
	helped fix the problem.
