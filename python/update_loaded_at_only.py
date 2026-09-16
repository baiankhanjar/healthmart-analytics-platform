from pathlib import Path
from datetime import datetime, timezone

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw_sources"


def add_loaded_at(
    csv_name: str,
    source_date_column: str,
) -> None:
    csv_path = RAW_DIR / csv_name

    if not csv_path.exists():
        raise FileNotFoundError(f"File not found: {csv_path}")

    df = pd.read_csv(csv_path)

    if source_date_column not in df.columns:
        raise ValueError(
            f"Column '{source_date_column}' not found in {csv_name}"
        )

    pd.to_datetime(df[source_date_column], errors="raise")

    batch_loaded_at = datetime.now(timezone.utc).replace(microsecond=0)

    df["loaded_at"] = batch_loaded_at  

    df.to_csv(csv_path, index=False)

    print(f"{csv_name} updated successfully")
    print(df[[source_date_column, "loaded_at"]].head())
    print(f"Rows: {len(df)}")


add_loaded_at(
    csv_name="transactions.csv",
    source_date_column="transaction_date",
)

add_loaded_at(
    csv_name="inventory.csv",
    source_date_column="last_updated_date",
)