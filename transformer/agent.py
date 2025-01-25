from datetime import datetime

import pandas as pd

from config import settings


class Agent:

    FIELDS = {
        settings.OUTPUT_TABLE: [
            "date",
            "MarketCapitalization",
            "open",
            "high",
            "low",
            "close",
            "adjusted_close",
            "volume",
            "hi_250d",
            "lo_250d",
            "avgvol_14d",
            "avgvol_50d",
            "avgvol_200d",
            "currency",
        ],
    }

    def __init__(self, data):
        self.data = data
        self.result = {}

    def transform(self):
        for ticker in self.data:
            for table in self.FIELDS:
                if not table in self.result:
                    self.result[table] = []

                row = {"eodhd_ticker": ticker}

                for k in self.FIELDS[table]:
                    if "#" in k:
                        k, name = k.split("#")
                    else:
                        name = k

                    if k in self.data[ticker]:
                        if self.data[ticker][k] != "NA":
                            if "date" in name.lower():
                                row[name] = self.valcheck_date(self.data[ticker][k])
                            else:
                                row[name] = self.valcheck(self.data[ticker][k])

                row["timestamp_created_utc"] = self.timenow()
                if len(row) > 2:
                    self.result[table].append(row)

        return {t: pd.DataFrame(d) for t, d in self.result.items()}

    @staticmethod
    def valcheck(value):
        if value in ["NA", "NaN", "", 0, "0", None]:
            return None

        elif isinstance(value, int):
            return round(float(value), 4)

        else:
            return value

    @staticmethod
    def valcheck_date(value):
        if value in ["NA", "NaN", "", 0, "0", None]:
            return None

        if "T" in value:
            value = value.split("T")[0]
        try:
            x = datetime.strptime(value, "%Y-%m-%d")
            if x.year < 1900:
                return None

            return value
        except Exception:
            return None

    @staticmethod
    def timenow():
        return datetime.utcnow()
