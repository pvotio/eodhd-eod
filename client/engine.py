from datetime import datetime, timedelta

import pytz

from client.eodhd import EODHD
from config import logger, settings


class Engine:

    TOKEN = settings.TOKEN

    def __init__(self, tickers, exchanges):
        self.tickers = tickers
        self.exchanges = exchanges
        self.data = []
        self.parsed_data = {}
        self.eodhd = EODHD(self.TOKEN)
        self._parse_inputs()

    def run(self):
        self._fetch_exchanges_eod()
        self._add_currency()
        return self.parsed_data

    def _fetch_exchanges_eod(self):
        today = datetime.utcnow().replace(tzinfo=pytz.timezone("CET"))
        date = (today - timedelta(2)).strftime("%Y-%m-%d")
        logger.info(f"Pulling data for {date}")
        for exchange, _ in self.exchanges:
            logger.debug(f"Fetching EOD for {exchange}")
            try:
                eod = self.eodhd.get_eod(exchange, date)
            except ValueError as e:
                logger.error(f"Cannot fetch eod data for {exchange}: {e}")
                continue

            self.data.extend(eod)

    def _add_currency(self):
        for row in self.data:
            ticker = f"{row['code']}.{row['exchange_short_name']}"
            if ticker.lower() in self.ticker_currency_map:
                _row = {**row, "currency": self.ticker_currency_map[ticker.lower()]}
            else:
                _row = {**row, "currency": None}

            self.parsed_data[ticker] = _row

    def _parse_inputs(self):
        self.ticker_currency_map = {
            ticker.lower(): currency for ticker, currency in self.tickers
        }
        self.exchange_currency_map = {}
        for exch, curr in self.exchanges:
            if not exch or not curr or len(curr) != 3:
                continue

            self.exchange_currency_map[exch.lower()] = curr

        return
