## Podcasts Api

- Create a virtual environment in python to be able to raise the files **python -m venv "environment"**
- Raising the virtual environment: **"dir"\scripts\activate.bat**
- Sometimes it is helpful to execute this command when the virtual environment is new: **python -m pip install --upgrade pip**
- Locate the file called "*requirements.txt*" and at its level execute the command **pip install -r requirements.txt**
- Now we must create the database and load it with its initial data at the same time we do this by running the file that calls : "*create_database.py*" with the **python command create_database.py**
- Now we run the api rest locally by running the file called "*api.py*" with the command **python api.py**
-We realize that the application is running as local in : **http://127.0.0.1:5000/**

---

## API endpoint(s)

- **Login:** http://127.0.0.1:5000/login Setting up in postman the following: 
  - GET Request
  - Authorization type: Basic Auth
  - Username: **jorge**
  - Password: **pass1234**
  - If we send the request this will answer us with what a token that will give us access to others endpoint(s)
  
For the use of these endpoint(s) only two headers must be configured, one of which includes the token obtained in the previous process
  - Content-Type: application/json
  - x-access-token: "*token*"
- **Podcasts search by name:** http://127.0.0.1:5000/podcast/< value >
   - value: Any word we would like to search by name in the stored podcasts
- **Save the top 20 podcasts:** http://127.0.0.1:5000/podcast/top20
   - In addition to showing us the top 20, it generates a new json file where it saves them. The file it creates is called **podcasts_separate_data.json**.
- **Replace the top 20 podcasts for bottom 20:** http://127.0.0.1:5000/podcast/bottom20
   - In the file podcasts_separate_data.json replace the top 20 with the bottom 20
- **Delete podcasts by id:** http://127.0.0.1:5000/podcast/< id >
   -  Delete a podcast by receiving the parameter id 
- **Podcasts group_by_genre:** http://127.0.0.1:5000/podcast/group_by_genre
   - Return all podcasts grouped by category

---
    
## Implemented Solutions

- **Database:** To implement what is the database, first the classes of the tables are invoked and with them the scheme is created, and having the scheme is sent to call the json data file and browse to insert the generereos as a first step, then at the same time the podcasts and their related table of generopodcasts.
- **Login:** For login we implemented the jwt protoco, and created a decorator to implement the token requirement in all urls.
- **Podcasts search by name:** We implemented a search engine that receives any text as a parameter and created a query that is not sensitive to letters so you can search for any type of phrase.
- **Save the top 20 podcasts:** A query was made where it was limited to call only the first 20 then these are printed in a response json and also saved a separate file.
- **Replace the top 20 podcasts for bottom 20:** First all the records were ordered downwards, then they were limited to choose the first 20 so we already had the 20 worst ones then they were replaced to the ones that already had the file created previously.
- **Delete podcasts by id:** It was created what is an elimination by the id key of the table, this elimination in turn eliminates the record of the table that has related, where the genres are stored, as it is a table of many to many.
- **Podcasts group_by_genre:** We made what is a custom query where all the podcasts ordered by gender, we used the table genre_podcasts, then json object was formatted to give the answer to be seen by groups.

---

### Note
I have attached a POSTMAN collection file where you can see examples of endpoints is named: "*focus-api.postman_collection.json*"