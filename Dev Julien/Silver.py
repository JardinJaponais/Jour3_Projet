import re
from datetime import datetime
import pandas as pd

LOG_PATTERN = re.compile(
    r'^(?P<ip>\S+)\s+'
    r'(?P<ident>\S+)\s+'
    r'(?P<user>\S+)\s+'
    r'\[(?P<ts_raw>[^\]]+)\]\s+'
    r'"(?P<method>\S+)\s+(?P<path>\S+)\s+(?P<protocol>[^"]+)"\s+'
    r'(?P<status>\d{3})\s+'
    r'(?P<bytes>\d+|-)\s+'
    r'"(?P<referer>[^"]*)"\s+'
    r'"(?P<user_agent>[^"]*)"\s*$'
)



def parse_log_line(line: str) -> dict | None:
    m = LOG_PATTERN.match(line.strip())
    if not m:
        return None
    d = m.groupdict()

    # Types
    d["status"] = int(d["status"])
    d["bytes"] = None if d["bytes"] == "-" else int(d["bytes"])

    # Date (ex: 14/Jan/2026:13:00:04 )
    # Il y a un espace avant le ']' dans ton fichier, on strip ts_raw.
    ts_clean = d["ts_raw"].strip()
    d["ts"] = datetime.strptime(ts_clean, "%d/%b/%Y:%H:%M:%S")

    # Nettoyages simples
    d["ident"] = None if d["ident"] == "-" else d["ident"]
    d["user"] = None if d["user"] == "-" else d["user"]
    d["referer"] = None if d["referer"] in ("", "-") else d["referer"]
    d["user_agent"] = None if d["user_agent"] in ("", "-") else d["user_agent"]

    return d


def parse_log_file(filepath: str) -> pd.DataFrame:
    rows = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            parsed = parse_log_line(line)
            if parsed:
                rows.append(parsed)

    df = pd.DataFrame(rows)

    # Ajouts utiles
    df["is_error"] = df["status"] >= 400
    df["path_category"] = df["path"].str.split("/", n=2).str[1].fillna("")

    return df
