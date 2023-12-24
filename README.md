# Vendor Management System with Performance Metrics

## How to Run the Application

Follow these steps to set up and run the Vendor Management System's API's:

### 1. Download and Extract the Project

Download the zip file of the project from the repository. After downloading, extract the contents of the zip file to a directory of your choice.

### 2. Navigate to the Project Directory

Open a terminal or command prompt and navigate to the "movies-api" folder using the `cd` command:

```bash
cd path/to/vendorManagement
```
### 3. setup the virtual enviroment
```bash
python -m venv venv
```

### 4. Run the following commands in terminal to configure the project (It requires Internet)
```bash
pip install -r requirements.txt
```

### 5.Type the following url in browser
```bash
http://127.0.0.1:5000/api/schema/docs/
```
above url will give access to swaggerUI to interact with provided API's.

### 6. Steps required for Interaction with API Documention
#### i. Register a new user by making Post request to the auth/users:
#### ii. Make post request on auth/token/login to login and get auth token.
#### iii. Now authorize by entering credentials by clicking Authorize button at start of SwaaggerUI page.
#### iv. now we can make appropriate request to Vendor Management API's.
