import pandas as pd
from pathlib import Path


# ==================================================
# 1. LOAD CLEANED MEDICINE DATASET
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MEDICINE_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "medicine_information_cleaned.csv"
)

medicine_df = pd.read_csv(MEDICINE_FILE)


# ==================================================
# 2. MEDICINE RETRIEVAL FUNCTION
# ==================================================

def search_medicines(condition, max_results=10):
    """
    Search the medicine database using the condition
    and selected fallback keywords.

    This function retrieves medicine information only.
    It does not diagnose or prescribe medicines.
    """

    if not condition or not isinstance(condition, str):
        return pd.DataFrame()

    condition = condition.strip().lower()

    # --------------------------------------------------
    # Primary search: exact condition phrase
    # --------------------------------------------------

    uses_text = (
        medicine_df["Uses"]
        .fillna("")
        .astype(str)
        .str.lower()
    )

    matches = medicine_df[
        uses_text.str.contains(condition, regex=False)
    ].copy()


    # --------------------------------------------------
    # Fallback search for terminology differences
    # --------------------------------------------------

    if len(matches) == 0:

        fallback_keywords = {
            "bronchial asthma": "asthma",
            "paroymsal positional vertigo": "vertigo",
            "dimorphic hemmorhoids(piles)": "piles",
            "osteoarthristis": "osteoarthritis",
            "peptic ulcer diseae": "peptic ulcer",
            "gastroenteritis": "gastroenteritis"
        }

        keyword = fallback_keywords.get(condition)

        if keyword:

            matches = medicine_df[
                uses_text.str.contains(keyword, regex=False)
            ].copy()


    # --------------------------------------------------
    # Select useful medicine information
    # --------------------------------------------------

    result_columns = [
        "Name",
        "Uses",
        "Composition",
        "Side_effects",
        "How_to_use",
        "Alcohol",
        "Pregnancy",
        "Breast feeding",
        "Driving",
        "Kidney",
        "Liver",
        "manufacturer"
    ]

    matches = matches[result_columns]


    # --------------------------------------------------
    # Limit number of results
    # --------------------------------------------------

    return matches.head(max_results)


# ==================================================
# 2b. FREE-TEXT SEARCH (medicine name or use)   <-- NEW
# ==================================================

_NAME_LOWER = medicine_df["Name"].fillna("").astype(str).str.lower()
_USES_LOWER = medicine_df["Uses"].fillna("").astype(str).str.lower()

_RESULT_COLUMNS = [
    "Name", "Uses", "Composition", "Side_effects", "How_to_use",
    "Alcohol", "Pregnancy", "Breast feeding", "Driving", "Kidney",
    "Liver", "manufacturer",
]


def search_medicines_by_query(query, max_results=20):
    """
    Search medicines by name or reported use (case-insensitive).
    Name matches are ranked before use matches.
    """

    if not query or not isinstance(query, str):
        return []

    q = query.strip().lower()

    if len(q) < 2:
        return []

    name_starts = _NAME_LOWER.str.startswith(q)
    name_has = _NAME_LOWER.str.contains(q, regex=False)
    uses_has = _USES_LOWER.str.contains(q, regex=False)

    ranked = pd.concat([
        medicine_df[name_starts],
        medicine_df[name_has & ~name_starts],
        medicine_df[uses_has & ~name_has],
    ]).head(max_results)

    ranked = ranked[_RESULT_COLUMNS].fillna("Information not available")

    medicines = []

    for _, row in ranked.iterrows():
        medicines.append({
            "name": row["Name"],
            "uses": row["Uses"],
            "composition": row["Composition"],
            "side_effects": row["Side_effects"],
            "how_to_use": row["How_to_use"],
            "alcohol": row["Alcohol"],
            "pregnancy": row["Pregnancy"],
            "breast_feeding": row["Breast feeding"],
            "driving": row["Driving"],
            "kidney": row["Kidney"],
            "liver": row["Liver"],
            "manufacturer": row["manufacturer"],
        })

    return medicines


# ==================================================
# 3. CLEAN MEDICINE INFORMATION FUNCTION
# ==================================================

def get_medicine_information(condition, max_results=5):
    """
    Retrieve medicine information in a clean dictionary format.

    This provides medicine information only.
    It does not diagnose or prescribe medicines.
    """

    results = search_medicines(
        condition,
        max_results=max_results
    )


    # --------------------------------------------------
    # No matching medicine information
    # --------------------------------------------------

    if results.empty:

        return {
            "condition": condition,
            "match_found": False,
            "medicines": []
        }


    # --------------------------------------------------
    # Convert DataFrame rows into dictionaries
    # --------------------------------------------------

    medicines = []

    for _, row in results.iterrows():

        medicine = {

            "name": row["Name"],

            "uses": row["Uses"],

            "composition": row["Composition"],

            "side_effects": row["Side_effects"],

            "how_to_use": row["How_to_use"],

            "alcohol": row["Alcohol"],

            "pregnancy": row["Pregnancy"],

            "breast_feeding": row["Breast feeding"],

            "driving": row["Driving"],

            "kidney": row["Kidney"],

            "liver": row["Liver"],

            "manufacturer": row["manufacturer"]

        }

        medicines.append(medicine)


    # --------------------------------------------------
    # Final structured response
    # --------------------------------------------------

    return {

        "condition": condition,

        "match_found": True,

        "medicines": medicines

    }


# ==================================================
# 4. TEST THE MEDICINE RETRIEVAL SYSTEM
# ==================================================

if __name__ == "__main__":

    result = get_medicine_information(
        "Diabetes",
        max_results=2
    )


    # --------------------------------------------------
    # Display basic result information
    # --------------------------------------------------

    print("Condition:", result["condition"])

    print("Match found:", result["match_found"])

    print(
        "Number of medicines:",
        len(result["medicines"])
    )


    # --------------------------------------------------
    # Display first medicine
    # --------------------------------------------------

    if result["match_found"]:

        print("\nFirst medicine:")

        print(
            result["medicines"][0]
        )

    else:

        print(
            "\nNo sufficiently matched medicine information found."
        )