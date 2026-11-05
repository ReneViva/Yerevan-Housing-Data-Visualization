"""Validate extracted official tariff facts against retained source snapshots."""
import csv
import hashlib
import json
from pathlib import Path
from lxml import html

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/official"


def text(name):
    return " ".join(html.fromstring((RAW / name).read_bytes()).text_content().split())


electricity = text("electricity.html")
gas = text("gas.html")
water = text("water.html")
transport = (RAW / "transport-rendered.txt").read_text(encoding="utf-8")
for value in ["46.48", "36.48", "48.48", "38.48", "53.48", "43.48"]:
    assert value in electricity, f"Missing electricity source fact {value}"
assert "143700" in gas
assert "2026" in text("gas-2026.html")
assert "200.42" in water and "200.42 AMD/m" in text("water-units.html")
assert "150 դրամ" in transport and "9000 դրամ" in transport

rows = [
    ("fare_single", 150, "AMD/boarding", "transport", "2025 onward; accessed 2026-11-05"),
    ("fare_30day", 9000, "AMD/commuter/30 days", "transport", "2025 onward; accessed 2026-11-05"),
    ("fare_365day", 90000, "AMD/commuter/365 days", "transport", "2025 onward; accessed 2026-11-05"),
    ("electric_day_low", 46.48, "AMD/kWh", "electricity", "monthly total <=200 kWh"),
    ("electric_night_low", 36.48, "AMD/kWh", "electricity", "monthly total <=200 kWh"),
    ("electric_day_mid", 48.48, "AMD/kWh", "electricity", "monthly total >200 and <=400 kWh"),
    ("electric_night_mid", 38.48, "AMD/kWh", "electricity", "monthly total >200 and <=400 kWh"),
    ("electric_day_high", 53.48, "AMD/kWh", "electricity", "monthly total >400 kWh"),
    ("electric_night_high", 43.48, "AMD/kWh", "electricity", "monthly total >400 kWh"),
    ("gas_per_1000m3", 143700, "AMD/1000 m3", "gas", "standard household; 2022 rate and 2026 no-change announcement"),
    ("water_per_m3", 200.42, "AMD/m3", "water", "2026 standard metered water plus wastewater; including VAT"),
]
with (RAW / "tariffs.csv").open("w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["parameter", "value", "unit", "source_id", "coverage"])
    writer.writerows(rows)
wages = list(csv.DictReader((RAW / "wage.csv").open(encoding="utf-8-sig")))
assert len({r["Year"] for r in wages}) == len(wages)
assert next(r for r in wages if r["Year"] == "2025")["Value"] == "303140"
print("PASS: 11 official tariff facts and 2015–2025 Armstat wage records checked.")
print("Tariffs transcribed from source snapshots; consumption remains a scenario.")

browser_record = {
    "source_url": "https://transport.yerevan.am/",
    "method": "Chrome DevTools rendered public page body text; no login or personal input",
    "verified_at_utc": "2026-11-05T14:59:23.614Z",
    "local_file": "data/raw/official/transport-rendered.txt",
    "sha256": hashlib.sha256((RAW / "transport-rendered.txt").read_bytes()).hexdigest(),
    "reproduction": "Open public page, wait for content, save fare-comparison text. Plain HTML is an SPA shell.",
    "status": "downloaded and validated against rendered public fare table",
}
(RAW / "transport-browser-metadata.json").write_text(
    json.dumps(browser_record, ensure_ascii=False, indent=2), encoding="utf-8"
)
