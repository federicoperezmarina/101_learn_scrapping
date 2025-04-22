import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import random
import time
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get MongoDB credentials from environment variables
mongodb_user = os.getenv('MONGODB_USER')
mongodb_password = os.getenv('MONGODB_PASSWORD')
mongodb_host = os.getenv('MONGODB_HOST')
mongodb_database = os.getenv('MONGODB_DATABASE')
mongodb_collection = os.getenv('MONGODB_COLLECTION')

# MongoDB connection with authentication
mongo_uri = f"mongodb+srv://{mongodb_user}:{mongodb_password}@{mongodb_host}"
client = MongoClient(mongo_uri)
db = client[mongodb_database]
collection = db[mongodb_collection]

urls = [
    'https://www.meetup.com/auckland-mongodb-meetup-group/',
    'https://www.meetup.com/barcelona-mongodb-user-group/',
    'https://www.meetup.com/madrid-database-professionals-meetup-group/',
    'https://www.meetup.com/seville-mongodb-meetup-group/',
    'https://www.meetup.com/paris-mongodb-user-group/',
    'https://www.meetup.com/northern-england-mongodb-user-group/',
    'https://www.meetup.com/london-mug/',
    'https://www.meetup.com/dublin-mongodb-user-group/',
    'https://www.meetup.com/milano-mongodb-user-group/',
    'https://www.meetup.com/zurich-mongodb-user-group/',
    'https://www.meetup.com/belgrade-mongodb-user-group/',
    'https://www.meetup.com/mugmunich/',
    'https://www.meetup.com/frankfurt-mongodb-user-group/',
    'https://www.meetup.com/belgium-mongodb-user-group/',
    'https://www.meetup.com/amsterdam-mongodb-user-group/',
    'https://www.meetup.com/mongodb-user-group-berlin/',
    'https://www.meetup.com/helsinki-mongodb-user-group/',
    'https://www.meetup.com/stockholm-mongodb-user-group/',
    'https://www.meetup.com/israel-mongodb-user-group/',
    'https://www.meetup.com/meetup-group-miwqboat/',
    'https://www.meetup.com/kuala-lumpur-mongodb-user-group/',
    'https://www.meetup.com/mug-sg/',
    'https://www.meetup.com/jakarta-mongodb-user-group/',
    'https://www.meetup.com/brisbane-mongodb-user-group/',
    'https://www.meetup.com/sydney-mongodb-user-group/',
    'https://www.meetup.com/canberra-mongodb-user-group',
    'https://www.meetup.com/mongodb-melb/',
    'https://www.meetup.com/wellington-mongodb-user-group/',
    'https://www.meetup.com/christchurch-mongodb-user-group/',
    'https://www.meetup.com/sao-paulo-mongodb-user-group/',
    'https://www.meetup.com/mexico-mongodb-user-group/',
    'https://www.meetup.com/la-mug',
    'https://www.meetup.com/sv-mug/',
    'https://www.meetup.com/sanfrancisco-mongodb-user-group/',
    'https://www.meetup.com/colorado-mongodb-user-group/',
    'https://www.meetup.com/austin-mongodb-usergroup/',
    'https://www.meetup.com/dallas-mongodb-meetup-group/',
    'https://www.meetup.com/chicago-mongodb-usergroup/',
    'https://www.meetup.com/mongodb-user-group-detroit/',
    'https://www.meetup.com/new-york-mongodb-user-group/',
    'https://www.meetup.com/boston-mongodb-usergroup',
    'https://www.meetup.com/montreal-mongodb-user-group/',
    'https://www.meetup.com/toronto-mongodb-usergroup/',
    'https://www.meetup.com/seattle-mongodb-user-group/',
    'https://www.meetup.com/vanmug/',
    'https://www.meetup.com/santa-catarina-florianopolis-mongodb-user-group/'
     ]

headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0'
}

for url in urls:

    time.sleep(random.randint(1, 5))

    # Send a GET request to the page
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        exit()

    today = datetime.now().strftime("%Y-%m-%d")

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    h1 = 'N/A'
    h1 = soup.find('h1').text

    members = 'N/A'
    members = soup.find('h2', id="members-section").text

    # Extract just the number using regex
    members_match = 'N/A'
    # First extract the number with commas using regex
    members_match = re.search(r'\(([\d,]+)\)', members)

    if members_match:
        # Remove commas and convert to integer
        members = int(members_match.group(1).replace(',', ''))
    else:
        members = 0
    
    location = 'N/A'
    location = soup.find('a', id='city-link').text
        
    # Split location into parts
    parts = [part.strip() for part in location.split(',')]

    if len(parts) == 3:
        # Format: City, State, Country
        city = parts[0]
        state = parts[1]
        country = parts[2]
    elif len(parts) == 2:
        # Format: City, Country
        city = parts[0]
        state = 'N/A'
        country = parts[1]
    else:
        # Single value or unexpected format
        city = location
        state = 'N/A'
        country = 'N/A'

    # Find image and get its src with error handling
    url_img = 'N/A'
    img_element = soup.find('img', {'alt': f'{h1} cover photo'})
    if img_element and 'src' in img_element.attrs:
        url_img = img_element['src'].strip()



    description = ''
    description = soup.find('div', class_="break-words utils_description__BlOCA").text

    print(today);
    print(h1);
    print(members);
    print(location);
    print(city);
    print(country);
    print(url_img);
    print(description);

    document = {
        'date': today,
        'scraped_at': datetime.now(),
        'name': h1,
        'members': members,
        'city': city,
        'state': state,
        'country': country,
        'url_img': url_img,
        'description': description
    }

    print(document)

    # Define the filter for upsert
    filter_doc = {
        'name': h1,
        'date': today
    }

    result = collection.update_one(
    filter_doc,
    {'$set': document},
    upsert=True
    )

    print('--------------------------------')
