import requests
from bs4 import BeautifulSoup

# url of the website
doc = "https://www.geeksforgeeks.org"

# getting response object
res = requests.get(doc)

# Initialize the object with the document
soup = BeautifulSoup(res.content.decode('latin-1'), "html.parser")

# Get the whole body tag
tag = soup.body

# Print each string recursively
for string in tag.strings:
	print(string)
