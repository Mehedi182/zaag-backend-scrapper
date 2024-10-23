# Web Scrapper and Backend App

## Setting Up a Virtual Environment

1. **Create a venv**

   ```
   python3 -m venv venv
   ```

2. **Activate the virtual environment**:

   - **Linux**:
     ```bash
     source venv/bin/activate
     ```
   - **macOS**:
     ```bash
     source venv/bin/activate
     ```
   - **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```

3. **Install the requirements**:
   ```
   pip install -r requirements.txt
   ```

## Run the scrapper

```
python scrapper.py
```

This will scrapped through the website and export the **tsv** files to the **../files** folder

## Backend Application

1. **Setup .env file. a sample is added in .env_sample**
```
DB_NAME = "zaag"
DB_USER = "postgres"
DB_PASSWORD = "1234"
DB_HOST = "localhost"
DB_PORT = "5432"
SECRET_KEY = "zaag"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

```
cd backend
```

2. **Run The Application**

```
uvicorn main:app --reload
```

3. **load the data**

```
python load_data.py
```

this will load the data to db

4. **check the api**: postman collection added
