import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

file_number = input("Enter the Page Number that You scraped: ")
aalocation = input("What is the locaiton of the job: ")
def removal(path):   #to remove any ' from the string so that it doesnot stop
    with open(path, 'r') as file:
        content = file.read()
        content = f" {content} "
        content = content.replace("'", "")
    return content
path = "temp.txt"
content = removal(path) # update the current file
with open(path, 'w') as file:
    file.write(content) #open the updated file
with open('temp.txt', 'r') as file:
    file_contents = file.read()

data = file_contents #data has all the html code necessary
soup = BeautifulSoup(data, 'html.parser')
everything = soup.find_all('div', class_='job_seen_beacon')
job_titles = []
company = []
location = []
salary = []
job_types = []
for jobs in everything:
    h2_elements1 = jobs.find_all('h2', class_='jobTitle css-198pbd eu4oa1w0') #get the title
    h2_elements2 = jobs.find_all('h2', class_='jobTitle jobTitle-newJob css-198pbd eu4oa1w0')
    h2_elements = h2_elements1 + h2_elements2
    for h2 in h2_elements:
        job_name_span = h2.find('span', id=lambda x: x and x.startswith('jobTitle-'))
        if job_name_span:
            job_name = job_name_span.get('title', job_name_span.text)
            job_titles.append(job_name)  #append the title
            
    div_elements = jobs.select('div.company_location') #get company and location details
    for div in div_elements:
        company_div = div.find('span', {'data-testid': 'company-name'}) #company
        location_div = div.find('div', {'data-testid': 'text-location'}) #location
        if company_div:
            company.append(company_div.text)    
        if location_div:
            location.append(location_div.text) 
            #now we get the salary and the type of the job 
    pay_elements = jobs.find_all('div', class_='jobMetaDataGroup css-pj786l eu4oa1w0') #get payment&job-type details
    for pay in pay_elements:
        pay_div = pay.find('div', class_='salary-snippet-container') 
        type_div = pay.find('div', class_='metadata css-5zy3wz eu4oa1w0')
        if pay_div:
            salary.append(pay_div.text.strip())
        else:
            salary.append('Not Provided') #salary
        if type_div:
            job_types.append(type_div.find('div', {'data-testid': 'attribute_snippet_testid'}).text.strip())
        else:
            job_types.append('Not Provided')
all_descriptions = []
all_dates = []
for description in everything:
        descr = description.find('div', class_='css-1u8dvic eu4oa1w0') 
        if descr:
            output = descr.find('ul').text.strip()
            all_descriptions.append(output)
        # Find the date element
        date_element = description.find('span', class_='css-qvloho eu4oa1w0')
        if date_element:
        # Extract and append the date text to the list
            date_text = date_element.text.strip()
            all_dates.append(date_text)
            
all_links = []
for link in everything:
    h2_elements1 = link.find_all('h2', class_='jobTitle css-198pbd eu4oa1w0') #get the title
    h2_elements2 = link.find_all('h2', class_='jobTitle jobTitle-newJob css-198pbd eu4oa1w0')
    h2_elements = h2_elements1 + h2_elements2
    # Loop through each h2 element
    for h2 in h2_elements:
        # Find the anchor tag (a) within the h2 element
        a_tag = h2.find('a')
        if a_tag:
            # Extract the 'href' attribute value from the anchor tag
            job_link = a_tag.get('href', '')
            all_links.append(job_link)

base_url = "https://www.indeed.com"
links = all_links  # assuming all_links is your list of job links
indeed_urls = []

for link in links:
    indeed_urls.append(base_url + link)


df = pd.DataFrame({
    'Job Title': job_titles,
    'Company': company,
    'Location': location,
    'Salary($)': salary,
    'Job-Type' : job_types,
    'Job-Description': all_descriptions,
    'Raw_Link': indeed_urls
})

print(df)
output_text = "datasets\AI-" + aalocation + "-Page(" + file_number +").csv"
df.to_csv(output_text)