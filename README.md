# Inventory-Dashboard
git clone https://github.com/kazimmsyed/Inventory_Dashboard.git
### Change directory
cd Inventory_Dashboard
### Install the virtual env, run the following command
python3 -m venv fastapienv && source fastapienv/bin/activate

## Image
<img width="390" height="227" alt="image" src="https://github.com/user-attachments/assets/c2bd1c94-5669-4474-b125-0c434864c4ee" />

### Install all the requirements
python install -r requirements.txt

### Change directory
cd fastapi/Inventory_Management 
### Execute the following command
python3 -m uvicorn main:app --reload
## Image:
<img width="863" height="200" alt="image" src="https://github.com/user-attachments/assets/a09f8dfb-ecd1-4620-8a94-8f94debff605" />
### Insert Northwind db records into sqlite
sqlite3 inventory_management.db < seed/data.sql

### Open the Swagger docs to test the endpoints
URL: http://127.0.0.1:8000/docs#/

<img width="703" height="727" alt="image" src="https://github.com/user-attachments/assets/ec29b633-d749-4f02-97d0-401c6c97a878" />

### Access the Web Application
URL: http://127.0.0.1:8000/auth/login

<img width="1440" height="684" alt="image" src="https://github.com/user-attachments/assets/043db040-1f7e-462e-9c77-bb282d12e059" />

### In order to deactivate the virtual environment
deactivate

