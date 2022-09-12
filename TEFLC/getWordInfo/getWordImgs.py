# 3
# getWordImgs.py

# --------------------------------------------
import requests
from bs4 import BeautifulSoup

# --------------------------------------------
# Returns a list with 3 urls to image files
# Tries 5 sources

# --------------------------------------------
# GLOBAL VARS
# --------------------------------------------
wordImgs = []
imgUrl1 = ""
imgUrl2 = ""
imgUrl3 = ""
imgUrl4 = ""
imgUrl5 = ""
# headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}

# --------------------------------------------
# SCRAPE FUNCTIONS
# --------------------------------------------
def getImgA (word):
	# print("A")
	# Source 1: CC0
	urlBase = "https://search.creativecommons.org/search?q="
	urlSearch = urlBase + word + "&license=cc0&license_type=commercial"
	page = requests.get(urlSearch)
	soup = BeautifulSoup(page.content, 'html.parser')
	results = soup.find("a", class_="search-grid_image-ctr")
	# Open Secondary Page
	imgUrlBase = "https://search.creativecommons.org"
	imgUrlResults = results["href"]
	urlSearch2 = imgUrlBase + imgUrlResults
	page2 = requests.get(urlSearch2)
	soup2 = BeautifulSoup(page2.content, 'html.parser')
	results2 = soup2.find("img", class_="photo_image")
	imgUrl1 = results2["src"]
	if imgUrl1 != "":
		wordImgs.append(imgUrl1)
	# print(wordImgs)

# --------------------------------------------
def getImgB (word):
	# print("B")
	# Source 2: Unsplash
	urlBase = "https://unsplash.com/s/photos/"
	urlSearch = urlBase + word
	page = requests.get(urlSearch)
	soup = BeautifulSoup(page.content, 'html.parser')
	results = soup.find("a", class_="_2Mc8_")
	# Open Secondary Page
	imgUrlBase = "https://unsplash.com"
	imgUrlResults = results["href"]
	urlSearch2 = imgUrlBase + imgUrlResults
	page2 = requests.get(urlSearch2)
	soup2 = BeautifulSoup(page2.content, 'html.parser')
	results2 = soup2.find("img", class_="_2UpQX")
	# Remove additional URL formatting
	imgUrl2 = results2["src"]
	imgList = imgUrl2.split("&")
	# print(imgList)
	imgUrl2 = imgList[0]
	# print(imgUrl2)
	if imgUrl2 != "":
		if len(wordImgs) < 3:
			if imgUrl2 not in wordImgs:
				wordImgs.append(imgUrl2)

# --------------------------------------------
def getImgC (word):
	# print("C")
	# Source 3: Pure PNG
	urlBase = "https://purepng.com/search?q="
	urlSearch = urlBase + word
	page = requests.get(urlSearch)
	soup = BeautifulSoup(page.content, 'html.parser')
	results = soup.find("a", class_="item hovercard")
	# Open Secondary Page
	urlSearch2 = results["href"]
	# print(urlSearch2)
	page2 = requests.get(urlSearch2)
	soup2 = BeautifulSoup(page2.content, 'html.parser')
	results2 = soup2.find("img", class_="img-responsive")
	imgUrl3 = results2["src"]
	# print(imgUrl3)
	if imgUrl3 != "":
		if len(wordImgs) < 3:
			if imgUrl3 not in wordImgs:
				wordImgs.append(imgUrl3)

# --------------------------------------------
def getImgD (word):
	# print("D")
	# Source 4: PDV
	urlBase = "https://publicdomainvectors.org/en/search/"
	urlSearch = urlBase + word
	page = requests.get(urlSearch)
	soup = BeautifulSoup(page.content, 'html.parser')
	results = soup.find("div", class_="vector-thumbnail-wrap").a
	# print(results)
	# Open Secondary Page
	imgUrlBase = "https://publicdomainvectors.org"
	imgUrlResults = results["href"]
	urlSearch2 = imgUrlBase + imgUrlResults
	# print(urlSearch2)
	page2 = requests.get(urlSearch2)
	soup2 = BeautifulSoup(page2.content, 'html.parser')
	results2 = soup2.find("img", class_="vec_veliki")
	# print(results2)
	imgUrl4 = imgUrlBase + results2["src"]
	# print(imgUrl4)
	if imgUrl4 != "":
		if len(wordImgs) < 3:
			if imgUrl4 not in wordImgs:
				wordImgs.append(imgUrl4)

# --------------------------------------------
def getImgE (word):
	# print("E")
	# Source 5: Stock Snap
	urlBase = "https://stocksnap.io/search/"
	urlSearch = urlBase + word
	page = requests.get(urlSearch)
	soup = BeautifulSoup(page.content, 'html.parser')
	results = soup.find("a", class_="photo-grid-preview")
	# print(results)
	# Open Secondary Page
	imgUrlBase = "https://stocksnap.io"
	imgUrlResults = results["href"]
	urlSearch2 = imgUrlBase + imgUrlResults
	# print(urlSearch2)
	page2 = requests.get(urlSearch2)
	soup2 = BeautifulSoup(page2.content, 'html.parser')
	results2 = soup2.find("div", class_="img-col").img
	# print(results2)
	imgUrl5 = results2["src"]
	# print(imgUrl5)
	if imgUrl5 != "":
		if len(wordImgs) < 3:
			if imgUrl5 not in wordImgs:
				wordImgs.append(imgUrl5)


# --------------------------------------------
def getWordImgs (word):
	global wordImgs
	wordImgs = []
	try: 
		# print("A")
		getImgA (word)
		# Continue if no error
		# print("B")
		getImgB (word)
		# Continue if no error
		# print("C")
		getImgC(word)
		# Continue if no error
		# print("D")
		getImgD(word)
		# Continue if no error
		# print("E")
		getImgE(word)
	except:
		try:
			# print("BB")
			getImgB (word)
			# Continue if no error
			# print("CC")
			getImgC(word)
			# Continue if no error
			# print("DD")
			getImgD(word)
			# Continue if no error
			# print("EE")
			getImgE(word)
		except:
			try:
				# print("CCC")
				getImgC(word)
				# Continue if no error
				# print("DDD")
				getImgD(word)
				# Continue if no error
				# print("EEE")
				getImgE(word)
			except:
				try:
					# print("DDDD")
					getImgD(word)
					# Continue if no error
					# print("EEEE")
					getImgE(word)
				except:	
					try:
						# print("EEEEE")
						getImgE(word)
					except:
						print("oops")
	# print(wordImgs)
	return wordImgs

# --------------------------------------------
# TEST

# word = "art"	
# wordImgs = getWordImgs(word)
# print(wordImgs)

# --------------------------------------------
# FAILED BUT GONNA KEEP HERE ANYWAYS

'''
# Can't bypass CloudFlare

# Source 3: Pexels 
urlBase = "https://www.pexels.com/search/"
urlSearch = urlBase + word + '/'
scraper = cfscrape.create_scraper()
page = scraper.get(urlSearch).content
print(page)
# page = requests.get(urlSearch, headers=headers)
# soup = BeautifulSoup(page.content, 'html.parser')
# print(soup)
# results = soup.find("a", class_="js-photo-link photo-item__link")
results = page.find("a", class_="js-photo-link photo-item__link")
print(results)
# Open Secondary Page
imgUrlBase = "https://www.pexels.com"
imgUrlResults = results["href"]
urlSearch2 = imgUrlBase + imgUrlResults
page2 = requests.get(urlSearch2, headers=headers)
soup2 = BeautifulSoup(page2.content, 'html.parser')
results2 = soup2.find("img", class_="js-photo-page-image-img")
imgUrl3 = results2["src"]
# print(imgUrl3)
if imgUrl3 != "":
	if imgUrl3 not in wordImgs:
		wordImgs.append(imgUrl3)

'''