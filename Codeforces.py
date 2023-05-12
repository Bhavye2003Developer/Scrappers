import requests
import html_to_json
from bs4 import BeautifulSoup


def getProblemLink():
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    table = str(soup.find('table', {"class":"problems"}))
    tableToJson = html_to_json.convert(table)['table'][0]['tr']
    linkList = []

    for i in range(1, len(tableToJson)):
        link = f"https://codeforces.com{tableToJson[i]['td'][0]['a'][0]['_attributes']['href']}"
        linkList.append(link)
    return linkList

def extractQuestionAddToFile(link):
    res = BeautifulSoup(requests.get(link).content, 'html.parser')
    problem_statement = res.find('div', {'class':'problem-statement'})
    if (problem_statement!=None):
        # problem_statement = html_to_json.convert(problem_statement)
        # print(problem_statement)
        # input_spec = problem_statement.find("div",{'class':'input-specification'}).get_text(strip=True)

        # output_spec = problem_statement.find("div",{'class':'output-specification'}).get_text(strip=True)
        # print(output_spec)

        problem_statement = problem_statement.get_text(strip=True)
        f = open("questions.txt","a+")
        f.write(problem_statement)
        f.write("\n\n\n\n")
        f.close()
        return 1
    return 0

total_pages = 85

for i in range(1,total_pages):
    print(f"\nOn Page -> {i}\n\n")

    f = open("questions.txt","a+")
    f.write(f"On Page -> {i}\n\n")
    f.close()
    
    url = f"https://codeforces.com/problemset/page/{i}"
    response = requests.get(url=url)

    if (response.ok):
        print("Starting extracting text...")
        linkList = getProblemLink()
        for link in linkList:
            status = extractQuestionAddToFile(link)
            if (status):
                print(f'{link} -> Successfull')
            else:
                print(f'{link} -> Unsuccessfull')

else:
    print("Unable to connect to the url")
