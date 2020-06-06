import urllib
import ssl
import certifi
import requests
import re
import aiohttp
import aiofiles
import asyncio

# patches the ssl certificate error
ssl.match_hostname = lambda cert, hostname: True
# get all urls from the s3 text file
urls_site = "https://s3.amazonaws.com/fieldlens-public/urls.txt"
# resp = urllib.request.urlopen(urls_site, timeout = 10, context=ssl.create_default_context(cafile=certifi.where()))
resp = urllib.request.urlopen(urls_site, timeout = 10, context=ssl.create_default_context(cafile=certifi.where()))


url_token = "https://"
urls = []
count = 0
for entry in resp:	
	url_tail = entry.decode("utf-8").split(",")[1]
	url = (url_token+url_tail).replace("\"","")
	urls.append(url)

# search a given term on the url returned:
# make the program concurrent

async def search_page(link_url, session, **kwargs):
	"""
	Returns : string of url info
	Parameters : string link_url, ClientSession session
	"""
	response = await session.request(method="GET", url=link_url, **kwargs)
	url_info = await response.text()
	return url_info

async def check_results(link_url, term, session, **kwargs):
	boolean = None
	try:
		info = await search_page(link_url=link_url, session=session, **kwargs)
	except:
		return "The link {} is unresponsive ".format(link_url)
	else:
		search_results = term.findall(info)
		boolean = "{} occurences match your search term".format(len(search_results))
		return boolean

async def write_result(results, link_url, term, **kwargs):
	"""
	Returns : None
			Appends the url search results into the result text file.
	Parameters : IO file results, string link_url
	"""
	res = await check_results(link_url=link_url, term=term, **kwargs)
	if not res:
		return None
	async with aiofiles.open(results, "a") as f:
		await f.write(f'{link_url}\t{res}\n')

async def mass_search(results, urls, term, **kwargs): 
	"""
	Returns: None
		Waits for all results to be appended to the results file
	Parameters : IOfile results, urls : string list of all urls
	"""
	connections = aiohttp.TCPConnector(limit=20)
	async with aiohttp.ClientSession(connector=connections) as session:
		find_links = []
		for url in urls[1:]:
			find_links.append(write_result(link_url=url,results=results, term=term, session=session, **kwargs))
		await asyncio.gather(*find_links)

if __name__ == "__main__":
	# change the search term to whatever you'd like to lookup
	search_term = "inClude"
	search_term = re.compile(search_term.lower())
	r_file = "results.txt"
	# asyncio.run(mass_search(r_file, urls)) --> python 3.8+
	loop = asyncio.get_event_loop()
	loop.run_until_complete(mass_search(r_file, urls, search_term))
