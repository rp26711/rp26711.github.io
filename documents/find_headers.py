import requests
import pyreadstat
import pandas as pd
from bs4 import BeautifulSoup

df, metadata = pyreadstat.read_sav("mn.sav")

# Get the variable names from mn.sav
variables = metadata.column_names

# Download webpage with variable descriptions
url = "https://microdata.worldbank.org/catalog/4180/data-dictionary/F7?file_name=mn.sav"
response = requests.get(url)

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Find all links as the page contains links where the variable name and description are both linked.
links = soup.find_all("a")

# Create a dictionary of links
link_text = [
    link.get_text(" ", strip=True)
    for link in links
]

# Match variables to descriptions
results = []

for variable in variables:

    # Find the variable in the links
    if variable in link_text:

        # Get its position
        position = link_text.index(variable)

        # The next link is the description
        if position + 1 < len(link_text):

            description = link_text[position + 1]

        else:

            description = None

    else:

        description = None

    # Store result
    results.append({
        "variable": variable,
        "header": description
    })

# Create a DataFrame
headers = pd.DataFrame(results)


# Save as CSV

headers.to_csv(
    "mn_headers.csv",
    index=False
)
