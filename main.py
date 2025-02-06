from bs4 import BeautifulSoup
import requests
import sqlite3
import os
import pandas as pd

def fetch_website(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def setup_database():
    if os.path.exists("data.db"):  
        os.remove("data.db")
    
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS task_data (id INTEGER PRIMARY KEY AUTOINCREMENT,text_data TEXT NOT NULL,html_tag TEXT NOT NULL)")

    conn.commit()
    conn.close()

def store_html_data(data):
    soup = BeautifulSoup(data, 'html.parser')

    unique_tags = {tag.name for tag in soup.find_all()}  

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    for tag in unique_tags:
        elements = soup.find_all(tag)
        for element in elements:
            text = element.get_text(strip=True)  
            if text:  
                cursor.execute("INSERT INTO task_data (text_data, html_tag) VALUES (?, ?)", (text, tag))

    conn.commit()
    conn.close()

def store_in_excel(data):
    soup = BeautifulSoup(data, 'html.parser')

    unique_tags = {tag.name for tag in soup.find_all()}  

    extracted_data = []

    for tag in unique_tags:
        elements = soup.find_all(tag)
        for element in elements:
            text = element.get_text(strip=True)
            if text:  
                extracted_data.append((text, tag))

    df = pd.DataFrame(extracted_data, columns=["Text Data", "HTML Tag"])
    df.to_excel("scraped_data.xlsx", index=False)

    print("Data successfully stored in Excel (scraped_data.xlsx)!")

def main():
    url = 'https://en.wikipedia.org/wiki/India'  
    
    setup_database()  

    data = fetch_website(url)

    if data:
        print("HTML data scraped successfully!")
        store_html_data(data)
        print("Data stored successfully in database!")
        store_in_excel(data)
        print("Data stored successfully in excel sheet!")

    else:
        print("Failed to fetch website data.")

if __name__ == "__main__":
    main()
