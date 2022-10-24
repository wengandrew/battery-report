from bs4 import BeautifulSoup
import requests
import csv
from os.path import exists
from datetime import datetime

# Define constants
filepath_company_list = 'resources/company_list.csv'


def find_and_write(company, output_file, job='', 
                                         city='', 
                                         year=''):


    # Find the requested content
    url = f"https://h1bdata.info/index.php?em={company}&job={job}&city={city}&year={year}"

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    data = []

    for tr in soup.find_all("tr"):
        row = []
        for td in tr.find_all("td"):
            row.append(td.text)
        if "".join(row).strip():
            data.append(row)

    print(f'{company}: {len(data)} entries found')

    file_exists = exists(output_file)

    # Write into file
    with open(output_file, "a+") as f:

        writer = csv.writer(f)

        if not file_exists:

            writer.writerow(["company", 
                             "title", 
                             "salary", 
                             "location", 
                             "submit date", 
                             "start date"])

        writer.writerows(data)

    return len(data)


if __name__ == '__main__':

    jobs = ['Battery', 'Vehicle', 'Chemist', 'Material', 'Process', 'Cell']
    curr_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    output_file = f'output/output-{curr_time}.csv'

    print(f'Writing into {output_file}...\n')

    with open(filepath_company_list) as csvfile:

        creader = csv.reader(csvfile)
        total = 0

        for i, row in enumerate(creader):

            company = row[0]
            total += find_and_write(company, output_file)

        print(f'Finished processing {i} companies with {total} total job postings.')
