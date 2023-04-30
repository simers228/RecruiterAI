## Steps to install dependencies in a virtual environment

1. Clone this repository to local computer

2. Rename the directory to reflect the new project name

3. Create a new virtual environment

   - Windows: `python -m venv ./venv`
   - Mac: `python3 -m venv ./venv`

4. Activate the new virtual environment

   - Windows: `.\venv\Scripts\activate`
   - Mac: `source ./venv/bin/activate`

5. Install the dependencies `pip install -r requirements.txt`

## Run the Applicatoin

Run the app `scrapy crawl linkedin_people_profile`

(pip install any modules if not found)
