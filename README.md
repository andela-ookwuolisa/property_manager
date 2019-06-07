### This is a simple CRUD API
#### To run the file, clone this repo
- clone this repo 
- install the dependencies (pip install requirements.txt)
- create the sql database like so in a python3 environment:
  ```
  from app import create_db
  create_db()
  ```
#### Running the app
```
flask run
```
  
#### Running the test
```
export FLASK_ENV=testing
python -m unittest discover -s test
```

#### Endpoints

* **URL**

  /register

* **Method:**
  
  `POST`

* **Data Params**

  **Required:**
 
   `first_name=[string]`

   `last_name=[string]`

   `username=[string]`

   `password=[string]`


* **URL**

  /login

* **Method:**
  
  `POST`

* **Data Params**

  **Required:**

   `username=[string]`

   `password=[string]`

* **URL**

  /logout

* **Method:**
  
  `GET`

  
* **URL**

  /user

* **Method:**
  
  `POST`

* **Data Params**

  **Required:**
 
   `first_name=[string]`

   `last_name=[string]`

   `username=[string]`

   `password=[string]`

* **URL**

  /user

* **Method:**
  
  `Get`

* **URL**

  /owner

* **Method:**
  
  `POST`

* **Data Params**

  **Required:**
 
   `user_id=[int]`
  
* **URL**

  /owner

* **Method:**
  
  `GET`

* **URL**

  /tenant

* **Method:**
  
  `POST`

* **Data Params**

  **Required:**
 
   `user_id=[int]`

   `property_id=[int]`

* **URL**

  /tenant

* **Method:**
  
  `GET`

* **URL**

  /tenant

* **Method:**
  
  `PUT`

* **Data Params**

  **Required:**
 
   `tenant_id=[int]`

   `user_id=[int]`

   `property_id=[int`
  
* **URL**

  /tenant

* **Method:**
  
  `DELETE`

* **Data Params**

  **Required:**
 
   `tenant_id=[int]` 

* **URL**

  /properties

* **Method:**
  
  `POST`

* **Data Params**

  **Required:**
 
   `owner_id=[int]`

   `property_type=[string]`

  **Optional:**

   `property_name=[string]`

   `location=[string]`

* **URL**

  /properties

* **Method:**
  
  `GET`

* **URL**

  /properties

* **Method:**
  
  `PUT`

* **Data Params**

  **Required:**
   `property_id=[int]`

   `owner_id=[int]`

   `property_type=[string]`

  **Optional:**
   `property_name=[string]`

   `location=[string]`
* **URL**

  /properties

* **Method:**
  
  `DELETE`

* **Data Params**

  **Required:**

   `property_id=[int]`

