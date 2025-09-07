from pathlib import Path
import pandas as pd

folder = Path("data")   # e.g., Path("data")
files = sorted(folder.glob("*.csv"))

# Read all and stack vertically
df = pd.concat(
    (pd.read_csv(f) for f in files),
    ignore_index=True
)

df = df[df["product"] == "pink morsel"]

clean_price = (df["price"].str.strip()
               .str.replace(r"[^\d.\-()]", "", regex=True)
               .str.replace(r"^\((.*)\)$", r"-\1", regex=True))

df["price_num"] = pd.to_numeric(clean_price, errors="coerce")

newdf = pd.DataFrame({
    "Sales":df["price_num"] * df["quantity"],
    "date":df["date"],
    "region":df["region"]
    }
)

# optional: write it back out
newdf.to_csv("all_data.csv", index=False)
