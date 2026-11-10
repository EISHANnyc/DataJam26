
from pathlib import Path
import re
import numpy as np
import pandas as pd

# Set the folders containing the original and cleaned datasets.
raw_folder = Path("Raw Data/Supplementary Data")
clean_folder = Path("Clean Data/Supplementary Data")

clean_folder.mkdir(parents=True, exist_ok=True)

# Check that the supplementary data folder exists.
if not raw_folder.exists():
    raise FileNotFoundError(f"Folder not found: {raw_folder}")


# Standardize column names so they are easier to work with.
def clean_column_names(columns):
    cleaned_columns = []
    column_counts = {}

    for index, column in enumerate(columns):
        name = str(column).strip().lower()
        name = name.replace("%", "percent")
        name = re.sub(r"[^a-z0-9]+", "_", name)
        name = name.strip("_")

        if not name:
            name = f"unnamed_{index}"

        if name in column_counts:
            column_counts[name] += 1
            name = f"{name}_{column_counts[name]}"
        else:
            column_counts[name] = 1

        cleaned_columns.append(name)

    return cleaned_columns


# Remove unnecessary blank rows and columns while preserving useful values.
def clean_dataframe(data, first_column_name=None):
    data = data.copy()

    # Remove cells containing only blank spaces.
    data = data.replace(r"^\s*$", np.nan, regex=True)

    # Remove extra spaces from text values.
    data = data.apply(
        lambda column: column.map(
            lambda value: value.strip() if isinstance(value, str) else value
        )
    )

    # Give the first column a meaningful name when needed.
    if first_column_name and len(data.columns) > 0:
        data = data.rename(
            columns={data.columns[0]: first_column_name}
        )

    # Standardize the column names.
    data.columns = clean_column_names(data.columns)

    # Remove rows and columns that contain no data.
    data = data.dropna(axis=0, how="all")
    data = data.dropna(axis=1, how="all")

    return data


# Record the cleaning results for each supplementary dataset.
cleaning_log = []


# Clean the supplementary CSV files.
csv_files = {
    "RentalMarketStatistics.csv": "zone",
    "Vancouver-Price Percentiles for homwowner and condominium units.csv": "month"
}

for filename, first_column_name in csv_files.items():
    source_file = raw_folder / filename
    output_file = clean_folder / f"{source_file.stem}_clean.csv"

    try:
        print(f"\nCleaning CSV: {filename}")

        # Read the CSV after skipping its report title rows.
        data = pd.read_csv(
            source_file,
            encoding="cp1252",
            skiprows=2
        )

        # Clean the column names and values.
        cleaned_data = clean_dataframe(
            data,
            first_column_name=first_column_name
        )

        # Save the cleaned CSV file.
        cleaned_data.to_csv(output_file, index=False)

        print("Saved:", output_file)
        print("Rows:", len(cleaned_data))
        print("Columns:", len(cleaned_data.columns))

        cleaning_log.append({
            "source_file": filename,
            "output_file": output_file.name,
            "status": "cleaned",
            "rows": len(cleaned_data),
            "columns": len(cleaned_data.columns),
            "notes": "Headers, blank rows, empty columns and text spaces cleaned."
        })

    except Exception as error:
        print(f"ERROR cleaning {filename}: {error}")

        cleaning_log.append({
            "source_file": filename,
            "output_file": output_file.name,
            "status": "error",
            "rows": None,
            "columns": None,
            "notes": str(error)
        })


# Set the header row for each Excel workbook.
excel_files = {
    "urban-rental-market-survey-data-number-units-building-size-2023-en.xlsx": 3,
    "urban-rental-market-survey-data-rent-quartiles-2023-en.xlsx": 3,
    "urban-rental-market-survey-data-vacancy-rates-rent-quartile-2023-en.xlsx": 4,
    "average-median-price-unabsorbed-row-apartment-units-2023-en(outside Data).xlsx": 4,
    "absorbed-units-price-range-canada-provinces-all-dwelling-types-2026-q3-en(outside data).xlsx": 4
}

# Clean each Excel workbook while preserving its separate sheets.
for filename, header_row in excel_files.items():
    source_file = raw_folder / filename
    output_file = clean_folder / f"{source_file.stem}_clean.xlsx"

    try:
        print(f"\nCleaning Excel file: {filename}")

        # Read each sheet using its actual header row.
        excel_file = pd.ExcelFile(source_file)

        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
            total_rows = 0
            total_columns = 0

            for sheet in excel_file.sheet_names:
                print(f"Cleaning sheet: {sheet}")

                data = pd.read_excel(
                    source_file,
                    sheet_name=sheet,
                    header=header_row
                )

                # Clean the sheet's column names and values.
                cleaned_data = clean_dataframe(data)

                # Save the cleaned sheet.
                cleaned_data.to_excel(
                    writer,
                    sheet_name=sheet[:31],
                    index=False
                )

                total_rows += len(cleaned_data)
                total_columns = max(
                    total_columns,
                    len(cleaned_data.columns)
                )

        print("Saved:", output_file)

        cleaning_log.append({
            "source_file": filename,
            "output_file": output_file.name,
            "status": "cleaned",
            "rows": total_rows,
            "columns": total_columns,
            "notes": f"Excel sheets cleaned using header row {header_row + 1}."
        })

    except Exception as error:
        print(f"ERROR cleaning {filename}: {error}")

        cleaning_log.append({
            "source_file": filename,
            "output_file": output_file.name,
            "status": "error",
            "rows": None,
            "columns": None,
            "notes": str(error)
        })


# Record supplementary files that need further review.
deferred_files = [
    "percentile-rents-urban-centres-pooled-small-centre-rental-market-2025-en.xlsx"
]

for filename in deferred_files:
    print(f"\nDeferred for further review: {filename}")

    cleaning_log.append({
        "source_file": filename,
        "output_file": None,
        "status": "deferred",
        "rows": None,
        "columns": None,
        "notes": "Multi-row headers and relevance to the selected market need review."
    })


# Keep the benchmark prices PDF as a reference document.
pdf_filename = "Greater-Vancouver-benchmark-prices.pdf"

print(f"\nPDF kept as reference: {pdf_filename}")

cleaning_log.append({
    "source_file": pdf_filename,
    "output_file": None,
    "status": "reference",
    "rows": None,
    "columns": None,
    "notes": "Original PDF retained for reference; not converted into a table."
})


# Save a record of the cleaning work.
log_data = pd.DataFrame(cleaning_log)
log_data.to_csv(
    clean_folder / "cleaning_log.csv",
    index=False
)

print("\nCLEANING PROCESS COMPLETE")
print("\nCLEANING SUMMARY:")
print(log_data[["source_file", "status"]].to_string(index=False))
print(f"\nCleaned files saved in: {clean_folder}")
