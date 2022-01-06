
## FastAPI with mongoDB

To run this app follow the below steps:

### Create a file called *.env* containing DB urls
>DB_URL="mongo link"
>DATABASE_NAME="name of your db"

### Create the virtual enviroment <br>

> python -m venv venv <br>


### Activate the virtual enviroment <br>

> source venv/bin/activate <br>

### Install the requirements <br>

> pip install requirements.txt <br>
> 
### Run the api

> uvicorn main:app --reload