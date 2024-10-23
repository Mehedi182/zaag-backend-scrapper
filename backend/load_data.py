import os

import pandas as pd
from database import SessionLocal
from models import ScrapperDataModel
from sqlalchemy.orm import Session


def load_data_from_tsv(file_path: str):
    # Read the TSV file into a DataFrame
    df = pd.read_csv(file_path, sep="\t")

    # Remove '%' from the column names
    df.columns = df.columns.str.replace("%", "", regex=False)
    # Remove any leading/trailing whitespaces from the column names
    df.columns = df.columns.str.strip()
    # List of expected columns
    expected_columns = [
        "id",
        "Name",
        "Tax ID",
        "GTDB ID",
        "Domain",
        "Abundance Score",
        "Relative Abundance",
        "Unique Matches",
        "Total Matches",
        "Unique Matches Frequency",
        "Reads Frequency",
        "Normalized Reads Frequency",
        "GO ID",
        "GO Category",
        "GO Description",
        "Copies Per Million",
        "Enzyme ID",
        "Pfam ID",
        "Cazy ID",
    ]

    # Check for missing columns and assign None for missing ones
    for col in expected_columns:
        if col not in df.columns:
            print(f"Warning: Missing column '{col}' in file {file_path}")
            df[col] = None

    db: Session = SessionLocal()

    try:
        for _, row in df.iterrows():
            sample_data = {
                "name": row.get("Name", None),
                "tax_id": row.get("Tax ID", None),
                "gtdb_id": row.get("GTDB ID", None),
                "domain": row.get("Domain", None),
                "abundance_score": row.get("Abundance Score", None),
                "relative_abundance": row.get("Relative Abundance", None),
                "unique_matches": row.get("Unique Matches", None),
                "total_matches": row.get("Total Matches", None),
                "unique_matches_frequency": row.get("Unique Matches Frequency", None),
                "reads_frequency": row.get("Reads Frequency", None),
                "normalized_reads_frequency": row.get(
                    "Normalized Reads Frequency", None
                ),
                "go_id": row.get("GO ID", None),
                "go_category": row.get("GO Category", None),
                "go_description": row.get("GO Description", None),
                "copies_per_million": row.get("Copies Per Million", None),
                "enzyme_id": row.get("Enzyme ID", None),
                "pfam_id": row.get("Pfam ID", None),
                "cazy_id": row.get("Cazy ID", None),
            }

            # Only include 'id' if it's present in the row (not None)
            if row.get("id") is not None:
                sample_data["id"] = row.get("id")

            db_sample = ScrapperDataModel(**sample_data)
            db.add(db_sample)

        db.commit()
    except Exception as e:
        print(f"Error occurred: {e}")
        db.rollback()
    finally:
        db.close()


files_path = "../files"
for file in os.listdir(files_path):
    if file.endswith(".tsv"):
        print(f"Loading data from file: {file}")
        load_data_from_tsv(os.path.join(files_path, file))
