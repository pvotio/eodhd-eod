# EODHD End-of-Day (EOD) Data Pipeline

This project implements a robust and automated ETL pipeline to ingest **end-of-day (EOD) financial data** using the [EOD Historical Data API](https://eodhistoricaldata.com/), parse and enrich it with currency mappings, and store the results in a Microsoft SQL Server database.

## Overview

### Purpose

The pipeline automates the following tasks:
- Authenticates and queries the EODHD API for daily EOD data per exchange.
- Applies ticker and exchange-specific currency enrichment.
- Transforms the raw EOD JSON into structured tabular data.
- Inserts the final output into SQL Server tables.

This system is designed for financial analysts, portfolio managers, and data engineers who require reliable and up-to-date daily price data for instruments traded across multiple exchanges.

## Source of Data

Data is retrieved from the official **EOD Historical Data API**:

- **Endpoint used**: `eod-bulk-last-day/{exchange}`
- **Format**: JSON with optional `"extended"` fieldset
- **Authentication**: Token-based (passed as query parameter)

> Note: The pipeline defaults to retrieving data for **yesterday** in CET time zone to ensure alignment with close-of-market hours globally.

## Application Flow

Execution begins in `main.py` and follows these stages:

1. **Load Metadata**:
   - Queries the database for tickers and exchange/currency mappings.

2. **Initialize Engine**:
   - Instantiates a custom `Engine` to manage API interactions and data normalization.

3. **Fetch EOD Data**:
   - For each exchange, retrieves EOD data using the `eod-bulk-last-day` endpoint.

4. **Enrich Data**:
   - Adds currency based on ticker and exchange mapping.
   - Skips tickers with missing or malformed symbols.

5. **Transform and Save**:
   - A `transformer.Agent` module shapes the parsed JSON into SQL-ready tables.
   - Uses bulk insertion via SQLAlchemy to persist results.

## Project Structure

```
eodhd-eod-main/
├── client/               # API client and ETL engine
│   ├── engine.py         # Orchestrates data fetch and parsing
│   └── eodhd.py          # Low-level EODHD API wrapper
├── config/               # Logging and settings handler
├── database/             # MSSQL DB helpers
├── transformer/          # Data frame preparation logic
├── main.py               # Primary entrypoint
├── .env.sample           # Sample environment variable configuration
├── Dockerfile            # Docker setup
```

## Environment Variables

Create a `.env` file using `.env.sample`. Key variables:

| Variable | Description |
|----------|-------------|
| `TOKEN` | EODHD API token |
| `EXCHANGES_DB_QUERY` | SQL query to pull exchange/currency mappings |
| `TICKERS_DB_QUERY` | SQL query to retrieve instrument tickers |
| `OUTPUT_TABLE` | Target SQL Server table for insert |
| `MSSQL_*` | Connection settings for SQL Server |
| `INSERTER_MAX_RETRIES` | Retry logic for insertions |
| `REQUEST_MAX_RETRIES`, `REQUEST_BACKOFF_FACTOR` | API request resilience |

## Docker Support

Build and run this ETL pipeline in a containerized environment.

### Build
```bash
docker build -t eodhd-eod .
```

### Run
```bash
docker run --env-file .env eodhd-eod
```

## Requirements

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Core packages:
- `pandas`: Data handling
- `requests`: HTTP requests
- `SQLAlchemy` + `pyodbc`: Database access
- `fast-to-sql`: Efficient batch insertion
- `python-decouple`: Environment variable parsing

## Running the Pipeline

Ensure all environment variables are correctly configured, then run:

```bash
python main.py
```

Logging will confirm:
- Exchanges and tickers loaded
- Data fetched from EODHD API
- Data inserted into the database

## License

This project is MIT licensed. Use of the EODHD API must comply with the service's terms and conditions.
