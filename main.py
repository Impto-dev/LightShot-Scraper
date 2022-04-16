import requests
import random
import os
import re

scr_not_found = "//st.prntscr.com/2021/04/08/1538/img/0_173a7b_211be8ff.png"
user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
root = __file__[:__file__.rfind("/")+1]

while True:
	digit_count = 7
	url = 'https://prnt.sc/' + "".join([x for x in [str(random.randint(0, 9)) for x in [None]*min(digit_count, 11)] if x != "0"])
	if url.endswith("/"): url = url + "1"
	html = requests.get(url, headers=user_agent)

	#print(html.status_code, url)

	if not html.ok: continue
	html = html.text

	img_url = re.search(r"<img\s*class=\"[\w\s-]+\"\s*src=\"([^\"]+)\"", html).group(1)
	if img_url == scr_not_found: continue

	extention = img_url.split(".")[-1]
	allfiles = sorted(os.listdir(root+"img/"))
	number = int(allfiles[-1][:allfiles[-1].rfind("_")])+1 if allfiles else 0
	filename = root+"img/{:05d}_{}.{}".format(number, url.split("/")[-1], extention)
	if [f for f in allfiles if f.endswith(filename.split("_")[-1])]:
		continue

	data = requests.get(img_url).content
	with open(filename, "wb") as img:
		img.write(data)

	print(f"\nCAPTURED {url} -> {repr(filename)}\n")