import os
import pandas as pd
from datetime import datetime


# ============================================================
# MARK ATTENDANCE
# ============================================================

def mark_attendance(name):
    """
    Mark attendance only once per student per day.

    Returns:
        True  -> attendance successfully added
        False -> attendance already exists or an error occurred
    """

    # ========================================================
    # BASE FOLDER
    # ========================================================

    base_folder = os.path.dirname(
        os.path.abspath(__file__)
    )

    # ========================================================
    # ATTENDANCE FOLDER
    # ========================================================

    attendance_folder = os.path.join(
        base_folder,
        "attendance"
    )

    os.makedirs(
        attendance_folder,
        exist_ok=True
    )

    # ========================================================
    # ATTENDANCE FILE
    # ========================================================

    file_name = os.path.join(
        attendance_folder,
        "attendance.xlsx"
    )

    # ========================================================
    # CURRENT DATE AND TIME
    # ========================================================

    now = datetime.now()

    date = now.strftime(
        "%d-%m-%Y"
    )

    time = now.strftime(
        "%H:%M:%S"
    )

    # ========================================================
    # CLEAN NAME
    # ========================================================

    name = str(name).strip()

    if not name:
        return False

    # ========================================================
    # LOAD EXISTING ATTENDANCE
    # ========================================================

    if os.path.exists(file_name):

        try:

            df = pd.read_excel(
                file_name
            )

        except Exception as e:

            print(
                "Unable to read attendance file:",
                e
            )

            return False

    else:

        df = pd.DataFrame(
            columns=[
                "Name",
                "Date",
                "Time"
            ]
        )

    # ========================================================
    # REQUIRED COLUMNS
    # ========================================================

    required_columns = [
        "Name",
        "Date",
        "Time"
    ]

    for column in required_columns:

        if column not in df.columns:

            df[column] = ""

    df = df[
        required_columns
    ].copy()

    # ========================================================
    # CLEAN EXISTING DATA
    # ========================================================

    df["Name"] = (
        df["Name"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # ========================================================
    # NORMALIZE DATE
    # ========================================================

    def normalize_date(value):

        if pd.isna(value):
            return ""

        # Excel/Pandas datetime
        if isinstance(
            value,
            (datetime, pd.Timestamp)
        ):

            return value.strftime(
                "%d-%m-%Y"
            )

        value = str(
            value
        ).strip()

        # Already correct format
        if value == date:
            return value

        date_formats = [
            "%d-%m-%Y",
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%Y/%m/%d",
            "%m-%d-%Y",
            "%m/%d/%Y"
        ]

        for date_format in date_formats:

            try:

                converted = datetime.strptime(
                    value,
                    date_format
                )

                return converted.strftime(
                    "%d-%m-%Y"
                )

            except ValueError:

                pass

        # Excel serial date
        try:

            number = float(
                value
            )

            converted = (
                pd.Timestamp(
                    "1899-12-30"
                )
                +
                pd.to_timedelta(
                    number,
                    unit="D"
                )
            )

            return converted.strftime(
                "%d-%m-%Y"
            )

        except Exception:

            pass

        # Final Pandas conversion
        try:

            converted = pd.to_datetime(
                value,
                errors="coerce"
            )

            if not pd.isna(
                converted
            ):

                return converted.strftime(
                    "%d-%m-%Y"
                )

        except Exception:

            pass

        return value

    df["Date"] = (
        df["Date"]
        .apply(normalize_date)
    )

    # ========================================================
    # CHECK DUPLICATE ATTENDANCE
    # ========================================================

    already_marked = df[
        (df["Name"].str.lower() == name.lower()) &
        (df["Date"] == date)
    ]

    # ========================================================
    # ALREADY MARKED
    # ========================================================

    if not already_marked.empty:

        # IMPORTANT:
        # Do not print anything here.
        # camera.py controls the messages.

        return False

    # ========================================================
    # NEW ATTENDANCE RECORD
    # ========================================================

    new_record = pd.DataFrame(
        [
            {
                "Name": name,
                "Date": date,
                "Time": time
            }
        ]
    )

    df = pd.concat(
        [
            df,
            new_record
        ],
        ignore_index=True
    )

    # ========================================================
    # SAVE ATTENDANCE
    # ========================================================

    try:

        df.to_excel(
            file_name,
            index=False
        )

        return True

    except Exception as e:

        print(
            "Unable to save attendance:",
            e
        )

        return False