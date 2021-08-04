from bs4 import BeautifulSoup as bs
import requests
import itertools
import json

r = requests.get('https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films').text

def scrape_website(r):
    soup = bs(r, 'html.parser')

    all_tables = soup.find_all('table', class_="wikitable sortable")

    #We want to find ALL the tr's in each table and the first td for each tr
    all_names = []
    names_map_to_href = {}
    for table in all_tables:

        #Find all tr in tbody, excluding the first one which is in relation to colour coding and structure, and not film data
        temp1 = table.find('tbody').find_all('tr')[1:]
        for e in temp1:

            #Use a try-except to ensure code runs despite any possible exceptions
            try:

                #If an a element exits find the contents and append them to all_names, if not find an i and do the same, if that doesnt exist append invalid message
                if e.find_all('td')[1].find('a') is None:

                    if e.find_all('td')[1].find('i') is None:
                        temp2 = ['Invalid name']
                        temp3 = ['Invalid href']
                    else:
                        temp2 = e.find_all('td')[1].find('i').contents
                        temp3 = e.find_all('td')[1].find('i')['href']

                else:
                    temp2 = e.find_all('td')[1].find('a').contents
                    temp3 = e.find_all('td')[1].find('a')['href']

                all_names.append(temp2)
                names_map_to_href[temp2[0]] = temp3

            except Exception as e:
                print('Exception occured')

    #Print out the list with all names after converting matrices to simple vectors
    print('----------------')
    all_names = list(itertools.chain.from_iterable(all_names))
    print(all_names)
    print(names_map_to_href)

    #Print out terminating message
    print('----------------')
    print('All names sucessfully scraped. Process terminated.')

    return all_names

#Save data into a file
def save_data(data, file_name):
    with open(file_name + '.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

variable = scrape_website(r)
save_data(variable, 'disney_movies')