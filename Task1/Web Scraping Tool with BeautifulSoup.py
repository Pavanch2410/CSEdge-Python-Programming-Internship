import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website to scrape
url = "http://books.toscrape.com/"

# Send a GET request to the website
response = requests.get(url)

# Parse the content of the request with BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Extract book titles and prices
books = []
for book in soup.find_all("article", class_="product_pod"):
    title = book.h3.a["title"]
    price = book.find("p", class_="price_color").text
    books.append({"title": title, "price": price})

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(books)

# Display the DataFrame
print(df)

# Save to CSV
csv_file = "books.csv"
df.to_csv(csv_file, index=False)

# Save to JSON
json_file = "books.json"
df.to_json(json_file, orient="records", indent=4)

print("Data has been saved to books.csv and books.json")

