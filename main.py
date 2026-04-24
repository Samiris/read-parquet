from fastapi import FastAPI, Query
import duckdb

print("duckdb version: " + duckdb.__version__)

app = FastAPI(title="Parquet Reader API")

# Path to your parquet file
PARQUET_FILE = "flights-1m.parquet"


@app.get("/")
def root():
    return {"message": "API is running!"}


@app.get("/data")
def get_data(
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    page_size: int = Query(100, ge=1, le=1000, description="Rows per page")
):
    """
    Paginated endpoint using DuckDB SQL (scalable approach)
    """

    # Calculate OFFSET based on page
    offset = (page - 1) * page_size

    # Main query with pagination
    query = f"""
    SELECT *
    FROM '{PARQUET_FILE}'
    LIMIT {page_size} OFFSET {offset}
    """

    # Execute query → returns only needed rows
    df = duckdb.query(query).to_df()

    # Get total number of rows (separate query)
    count_query = f"""
    SELECT COUNT(*) as total
    FROM '{PARQUET_FILE}'
    """

    total_rows = duckdb.query(count_query).fetchone()[0]

    # Calculate total pages
    total_pages = (total_rows + page_size - 1) // page_size

    return {
        "page": page,
        "page_size": page_size,
        "total_rows": total_rows,
        "total_pages": total_pages,
        "data": df.to_dict(orient="records")
    }

@app.get("/data/search")
def get_data_search(
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=1000),

    # Optional filters
    q1: str | None = Query(None),
    q2: str | None = Query(None),
):
    """
    Paginated + filtered endpoint using DuckDB
    """

    offset = (page - 1) * page_size

    # Base query
    base_query = f"FROM '{PARQUET_FILE}' WHERE 1=1"

    # Parameters list (for safe query)
    params = []

    # Dynamic filters
    if q1:
        base_query += " AND DEP_DELAY = ?"
        params.append(int(q1))

    if q2:
        base_query += " AND ARR_DELAY = ?"
        params.append(q2)

    # Full query with pagination
    query = f"""
    SELECT *
    {base_query}
    LIMIT {page_size} OFFSET {offset}
    """

    df = duckdb.query(query, params=params).to_df()

    # Count query (same filters!)
    count_query = f"""
    SELECT COUNT(*) 
    {base_query}
    """

    total_rows =  duckdb.query(count_query, params=params).fetchone()[0]

    total_pages = (total_rows + page_size - 1) // page_size

    return {
        "page": page,
        "page_size": page_size,
        "total_rows": total_rows,
        "total_pages": total_pages,
        "data": df.to_dict(orient="records")
    }