import pandas as pd
from bs4 import BeautifulSoup

# Function to get user inputs for file number and job location
def get_user_inputs():
    file_number = input("Enter the Page Number that You scraped: ")
    location = input("What is the location of the job: ")
    return file_number, location


# Function to remove quotes from a file
def remove_quotes_from_file(path):
    with open(path, 'r') as file:
        # Read file content and replace single quotes
        content = file.read().replace("'", "")
    with open(path, 'w') as file:
        # Write modified content back to file
        file.write(content)

# Function to read HTML content from a file
def read_html_from_file(path):
    with open(path, 'r') as file:
        return file.read()
    
# Function to parse job details from HTML soup
def parse_job_details(soup):
    jobs = soup.find_all('div', class_='job_seen_beacon')
    job_titles, companies, locations, salaries, job_types, descriptions, dates, links = [], [], [], [], [], [], [], []

    # Loop through each job listing
    for job in jobs:
        # Get job titles
        title_elements = job.find_all('h2', class_=['jobTitle css-198pbd eu4oa1w0', 'jobTitle jobTitle-newJob css-198pbd eu4oa1w0'])
        for h2 in title_elements:
            job_name_span = h2.find('span', id=lambda x: x and x.startswith('jobTitle-'))
            if job_name_span:
                job_name = job_name_span.get('title', job_name_span.text)
                job_titles.append(job_name)

        # Get company and location details
        company_div = job.find('span', {'data-testid': 'company-name'})
        location_div = job.find('div', {'data-testid': 'text-location'})
        if company_div:
            companies.append(company_div.text)
        if location_div:
            locations.append(location_div.text)

        # Get salary and job type details
        pay_div = job.find('div', class_='salary-snippet-container')
        type_div = job.find('div', class_='metadata css-5zy3wz eu4oa1w0')
        salaries.append(pay_div.text.strip() if pay_div else 'Not Provided')
        job_types.append(type_div.find('div', {'data-testid': 'attribute_snippet_testid'}).text.strip() if type_div else 'Not Provided')

        # Get job description
        descr = job.find('div', class_='css-1u8dvic eu4oa1w0')
        if descr:
            descriptions.append(descr.find('ul').text.strip() if descr.find('ul') else '')
        
        # Get job posting date
        date_element = job.find('span', class_='css-qvloho eu4oa1w0')
        if date_element:
            dates.append(date_element.text.strip())

        # Get job link
        a_tag = job.find('h2', class_='jobTitle').find('a') if job.find('h2', class_='jobTitle') else None
        if a_tag:
            links.append("https://www.indeed.com" + a_tag.get('href', ''))

    return job_titles, companies, locations, salaries, job_types, descriptions, dates, links

# Function to save DataFrame to CSV
def save_to_csv(dataframe, location, file_number):
    output_text = f"onepage-csvfiles/AI-{location}-Page({file_number}).csv"
    dataframe.to_csv(output_text, index=False)

# Main function to run the script
def main():
    # Get user inputs
    file_number, location = get_user_inputs()
    
    # Process the HTML file
    remove_quotes_from_file("temp.txt")
    html_data = read_html_from_file("temp.txt")
    soup = BeautifulSoup(html_data, 'html.parser')

    # Parse job details from the HTML
    job_titles, companies, locations, salaries, job_types, descriptions, dates, links = parse_job_details(soup)

    # Create a DataFrame from the parsed data
    df = pd.DataFrame({
        'Job Title': job_titles,
        'Company': companies,
        'Location': locations,
        'Salary($)': salaries,
        'Job-Type': job_types,
        'Job-Description': descriptions,
        'Raw_Link': links
    })

    # Print the DataFrame
    print(df)
    
    # Save the DataFrame to CSV
    save_to_csv(df, location, file_number)

# Entry point for the script
if __name__ == "__main__":
    main()

