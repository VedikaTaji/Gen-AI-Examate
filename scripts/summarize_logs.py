import json
import statistics
from pathlib import Path

rows = [json.loads(x) for x in Path("logs/requests.jsonl").read_text().splitlines() if x]
ok = [r for r in rows if r["status"] == 200]
live = [r for r in ok if not r["cache_hit"]]
lat = sorted(r["latency_ms"] for r in live) or [0]
print(f"requests logged      : {len(rows)}")
print(f"cache hits           : {sum(r['cache_hit'] for r in rows)}")
print(f"blocked/failed       : {len(rows) - len(ok)}")
print(f"latency p50 / p95 ms : {statistics.median(lat):.0f} / {lat[min(len(lat) - 1, int(len(lat) * .95))]:.0f}")
print(f"avg tokens in / out  : {statistics.mean([r['tokens_in'] for r in live] or [0]):.0f} / {statistics.mean([r['tokens_out'] for r in live] or [0]):.0f}")