
from pathlib import Path
import pandas as pd
import sys
import fitz

sys.stdout.reconfigure(encoding="utf-8")

# Find the folder containing the supplementary datasets.
folder = Path("Raw Data/Supplementary Data")

print("\nSUPPLEMENTARY DATA INSPECTION")

# Check each file in the supplementary data folder.
for file in folder.iterdir():

    try:
        # Inspect Excel files and list their sheets.
        if file.suffix == ".xlsx":
            print(f"\nEXCEL FILE: {file.name}")

            excel_file = pd.ExcelFile(file)

            for sheet in excel_file.sheet_names:
                print(f"\nSHEET: {sheet}")

                preview = pd.read_excel(
                    file,
                    sheet_name=sheet,
                    nrows=5
                )

                print("COLUMNS:", preview.columns.tolist())
                print("PREVIEW:")
                print(preview.to_string(index=False))

        # Inspect CSV files and preview their contents.
        elif file.suffix == ".csv":
            print(f"\nCSV FILE: {file.name}")

            preview = pd.read_csv(
                file,
                nrows=5,
                encoding="cp1252",
                skiprows=2
            )

            print("COLUMNS:", preview.columns.tolist())
            print("PREVIEW:")
            print(preview.to_string(index=False))

        # Identify PDF files for separate inspection.
        elif file.suffix == ".pdf":
            print(f"\nPDF FILE: {file.name}")
            print("PDF will be inspected separately.")

    except Exception as error:
        print(f"ERROR: {error}")

# Display the first lines of the CSV files to locate their actual headers.
csv_files = [
    "RentalMarketStatistics.csv",
    "Vancouver-Price Percentiles for homwowner and condominium units.csv"
]

for filename in csv_files:
    print(f"\nRAW LINES: {filename}")

    with open(folder / filename, encoding="cp1252") as csv_file:
        for line_number, line in enumerate(csv_file, start=1):
            if line_number > 12:
                break

            print(f"{line_number}: {line.rstrip()!r}")

# Check the column names and data types in the supplementary CSV files.
for filename in csv_files:
    print(f"\nCSV DETAILS: {filename}")

    data = pd.read_csv(
        folder / filename,
        encoding="cp1252",
        skiprows=2,
        nrows=5
    )

    print("Column names:")
    print(data.columns.tolist())

    print("\nData types:")
    print(data.dtypes)

# Extract text from the supplementary PDF report.
pdf_file = folder / "Greater-Vancouver-benchmark-prices.pdf"

print(f"\nPDF FILE: {pdf_file.name}")

document = fitz.open(pdf_file)

for page_number, page in enumerate(document, start=1):
    print(f"\nPAGE {page_number}:")
    print(page.get_text()[:2000])

document.close()

print("\nINSPECTION COMPLETE")
