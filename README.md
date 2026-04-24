project/
│── main.py
│── requirements.txt
│── flights-1m.parquet   

---- Install

python --version
git clone <replace>
cd read-parque
python -m venv venv
pip install -r requirements.txt
uvicorn main:app --reload

alternative uv
Win op 1: irm https://astral.sh/uv/install.ps1 | iex
Win op 2: pip install uv
uv --version
uv init
uv add fastapi uvicorn pandas pyarrow duckdb
uv export --format requirements-txt > requirements.txt

----

GET
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/data/search?page=1&page_size=100&q1=-4&q2=%204
