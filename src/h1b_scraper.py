from bs4 import BeautifulSoup
import requests
import csv
from os.path import exists
import time

def search(company, job, city, year, t):
    url = "https://h1bdata.info/index.php?em={}&job={}&city={}&year={}".format(company, job, city, str(year))
    print("Fetching Data from: " + url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    data = []
    for tr in soup.find_all("tr"):
        row = []
        for td in tr.find_all("td"):
            row.append(td.text)
        if "".join(row).strip():
            data.append(row)

    output_file = "output-"+str(t)+".csv"
    print("Writing " + str(len(data)) + " Entries out to: " + output_file)
    file_exists = exists(output_file)
    with open(output_file, "a+") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["company", "title", "salary", "location", "submit date", "start date"])
        writer.writerows(data)
    print("Done.")
    return len(data)
jobs = ['Battery', 'Vehicle', 'Chemist', 'Material']
city = {'Panasonic Corporation Of North America': 'Sparks, NV' }

with open('companies.csv') as csvfile:
    t= time.time()
    creader = csv.reader(csvfile)
    i =0
    total = 0
    for row in creader:
        i += 1
        comp = row[0]
        for job in jobs:
            ci = ''
            if comp in city:
                ci = city[comp]
            total += search(comp, job, ci, '', t)
    print('processed:' + str(i) + " companies.")
    print('found:' + str(total) + " job postings.")

#search('Tesla', '', '', 2021)