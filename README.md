# EODHD EOD
## Overview
EODHD EOD is a Python-based data pipeline that retrieves end-of-day (EOD) stock data using the EOD Historical Data API. It processes and stores the collected data in a Microsoft SQL Server database for further analysis.

## Features
- Fetches EOD stock data for multiple exchanges and tickers.
- Implements a retry mechanism for reliable API communication.
- Parses and processes financial data efficiently.
- Stores structured data in a Microsoft SQL Server database.
- Supports logging and configurable settings via environment variables.
- Dockerized for easy deployment.

## Installation
### Prerequisites
- Python 3.10+
- Microsoft SQL Server
- Docker (optional, for containerized execution)

### Setup
Clone the repository:

```bash
git clone https://github.com/arqs-io/eodhd-eod.git
cd eodhd-eod
```

Install dependencies:

`pip install -r requirements.txt`

Set up environment variables:

- Copy .env.sample to .env
- Edit .env to include your database and API credentials.

Run the application:
`python main.py`

## Docker Usage

To run the application using Docker:


```bash
docker build -t eodhd-eod .
docker run --env-file .env eodhd-eod
```

## Contributing
- Fork the repository.
- Create a feature branch: git checkout -b feature-branch
- Commit changes: git commit -m "Add new feature"
- Push to the branch: git push origin feature-branch
- Open a Pull Request.