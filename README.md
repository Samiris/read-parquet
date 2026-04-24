```
|--project
    |-- main.py
    |-- requirements.txt
    |-- file.parquet
```

#### pip

python --version  <br>
git clone https://github.com/Samiris/read-parquet.git  <br>
cd read-parquet  <br>
python -m venv venv  <br>
pip install -r requirements.txt  <br>
uvicorn main:app --reload  <br>

#### uv   

Win Op1: irm https://astral.sh/uv/install.ps1 | iex  <br>
Win Op2: pip install uv  <br>
uv --version  <br>
uv init  <br>
uv add fastapi uvicorn pandas pyarrow duckdb  <br>
uv export --format requirements-txt > requirements.txt  <br>
uvicorn main:app --reload  <br>

#### GET  
http://127.0.0.1:8000/docs  <br>
http://127.0.0.1:8000/data/search?page=1&page_size=100&q1=-4&q2=%204
