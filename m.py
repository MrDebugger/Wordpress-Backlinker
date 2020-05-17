import threading,time
from requests import get,post
from bs4 import BeautifulSoup as bs 
import json
import urllib3
from urllib.parse import urlparse
start=time.perf_counter()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#links = open('links.txt').read().splitlines()
headers = {
    'authority': 'rzcracks.com',
    'cache-control': 'max-age=0',
    'origin': 'https://rzcracks.com',
    'upgrade-insecure-requests': '1',
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
    'sec-fetch-dest': 'document',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'referer': 'https://rzcracks.com/wondershare-mobilego-crack-free-download/',
    'accept-language': 'en-US,en;q=0.9',
}

data = json.load(open('postData.json'))
def love(link):
	print(f"[+] Loading Comment Id at {link}")
	try:
		r = get(link,verify=False)
	except Exception as e:
		print("[-] Invalid Link:",link)
		return
	if not r:
		print("[-] 404 Not found at:",link)
		print()
	soup = bs(r.text,'lxml')
	form = soup.find(id='commentform')
	if not form:
		print("[-] No Comment Form found at {link}")
		print()
		return
	print("[+] Form Found in",link)
	inputs = {inp['name']:inp.get('value','') for inp in form.findAll(attrs={"name":True})}
	for field in ['comment_post_ID','comment_parent','ak_js']:
		if field in inputs:
			data[field] = inputs.get(field,'')
	linkParse = urlparse(link)
	postLink = form.get('action',f"{linkParse.scheme}://{linkParse.netloc}/wp-comments-post.php")
	print(f"[+] Submitting Form at {link}")
	headers['referer'] = link
	headers['origin'] = f"{linkParse.scheme}://{linkParse.netloc}"
	headers['authority'] = f"{linkParse.netloc}"
	try:
		r = post(postLink,verify=False,data=data,headers=headers)
		print(f"[+] Post Submitted at {link}")
	except:
		print(f"[-] Failed to Submit Form at {link}")
		print()
		return
	open('success.txt','a').write(f'{link}\n')
	print()
def th(num,link):
	index = links.index(link)
	try:
		for i in range(num):
			t=threading.Thread(target=love,args=[links[index+i]])
			t.start()
		t.join()
	except:
		pass
with open('links.txt', 'r') as inp:
	links = list(set([x.rstrip() for x in inp.readlines()]))
	threads = 5
	for a in links[::threads]:
		th(threads, a)

finish=time.perf_counter()
print(f'Job done in {round(finish-start, 2)}')