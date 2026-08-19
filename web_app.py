import streamlit as st
import face_recognition
import pickle
import json
import numpy as np
import pandas as pd
from datetime import datetime


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Face Attendance System",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# LOAD FACE ENCODINGS
# ============================================================

try:

    with open("encodings/encodings.pkl", "rb") as f:
        known_encodings, known_names = pickle.load(f)

    encodings_loaded = True

except Exception as e:

    encodings_loaded = False
    known_encodings = []
    known_names = []

    st.error(f"Could not load face encodings: {e}")


# ============================================================
# LOAD STUDENT INFORMATION
# ============================================================

try:

    with open("students.json", "r", encoding="utf-8") as f:
        students = json.load(f)

except Exception as e:

    students = []

    st.error(f"Could not load student information: {e}")


# ============================================================
# FIND STUDENT DETAILS
# ============================================================

def get_student_details(name):

    # Convert names such as:
    # tharun_1 -> tharun
    # ranga_1  -> ranga

    clean_name = name.lower().strip()

    if clean_name.endswith("_1"):
        clean_name = clean_name[:-2]

    for student in students:

        student_name = student["name"].lower().strip()

        if student_name == clean_name:
            return student

    return None


# ============================================================
# SAVE ATTENDANCE
# ============================================================

def save_attendance(name):

    file_path = "attendance/attendance.xlsx"

    current_date = datetime.now().strftime("%d-%m-%Y")
    current_time = datetime.now().strftime("%I:%M:%S %p")

    try:

        df = pd.read_excel(file_path)

    except FileNotFoundError:

        df = pd.DataFrame(
            columns=["Name", "Date", "Time"]
        )

    # Make sure required columns exist
    required_columns = ["Name", "Date", "Time"]

    for column in required_columns:

        if column not in df.columns:
            df[column] = ""

    # Check whether this student already has
    # attendance for today's date

    already_marked = (
        (
            df["Name"]
            .astype(str)
            .str.strip()
            .str.lower()
            == name.strip().lower()
        )
        &
        (
            df["Date"]
            .astype(str)
            .str.strip()
            == current_date
        )
    ).any()

    # --------------------------------------------------------
    # ALREADY MARKED
    # --------------------------------------------------------

    if already_marked:

        return False, current_date, current_time

    # --------------------------------------------------------
    # NEW ATTENDANCE
    # --------------------------------------------------------

    new_row = pd.DataFrame(
        [[name, current_date, current_time]],
        columns=["Name", "Date", "Time"]
    )

    df = pd.concat(
        [df, new_row],
        ignore_index=True
    )

    df.to_excel(
        file_path,
        index=False
    )

    return True, current_date, current_time


# ============================================================
# PAGE HEADER
# ============================================================

st.title("🤖 AI Face Attendance System")

st.write(
    "Browser-based AI face recognition and attendance system"
)

st.divider()


# ============================================================
# CAMERA SECTION
# ============================================================

col1, col2 = st.columns([2, 1])


with col1:

    st.subheader("📷 Camera")

    picture = st.camera_input(
        "Take a photo"
    )


# ============================================================
# STUDENT INFORMATION SECTION
# ============================================================

with col2:

    st.subheader("👤 Student Information")

    # --------------------------------------------------------
    # NO PHOTO
    # --------------------------------------------------------

    if picture is None:

        st.info(
            "Take a photo to recognize a student."
        )

        st.write("**Name:** —")
        st.write("**Roll No:** —")
        st.write("**Department:** —")
        st.write("**Status:** —")
        st.write("**Date:** —")
        st.write("**Time:** —")

    # --------------------------------------------------------
    # PHOTO TAKEN
    # --------------------------------------------------------

    else:

        # ----------------------------------------------------
        # LOAD IMAGE
        # ----------------------------------------------------

        image = face_recognition.load_image_file(
            picture
        )

        # ----------------------------------------------------
        # DETECT FACES
        # ----------------------------------------------------

        face_locations = face_recognition.face_locations(
            image
        )

        face_encodings = face_recognition.face_encodings(
            image,
            face_locations
        )

        recognized_student = None
        recognized_name = None

        # ----------------------------------------------------
        # NO FACE
        # ----------------------------------------------------

        if len(face_encodings) == 0:

            st.warning(
                "⚠️ No face detected. Please take another photo."
            )

            st.write("**Name:** —")
            st.write("**Roll No:** —")
            st.write("**Department:** —")
            st.write("**Status:** UNKNOWN")

        # ----------------------------------------------------
        # FACE FOUND
        # ----------------------------------------------------

        else:

            for face_encoding in face_encodings:

                if not known_encodings:
                    break

                # Compare captured face with stored faces

                matches = face_recognition.compare_faces(
                    known_encodings,
                    face_encoding,
                    tolerance=0.5
                )

                # Calculate face distances

                face_distances = face_recognition.face_distance(
                    known_encodings,
                    face_encoding
                )

                # Find closest face

                best_match_index = np.argmin(
                    face_distances
                )

                best_distance = face_distances[
                    best_match_index
                ]

                # ------------------------------------------------
                # CHECK MATCH
                # ------------------------------------------------

                if matches[best_match_index]:

                    recognized_name = known_names[
                        best_match_index
                    ]

                    recognized_student = (
                        get_student_details(
                            recognized_name
                        )
                    )

                    if recognized_student:
                        break

            # ----------------------------------------------------
            # RECOGNIZED STUDENT
            # ----------------------------------------------------

            if recognized_student:

                # ------------------------------------------------
                # SAVE ATTENDANCE
                # ------------------------------------------------

                attendance_saved, current_date, current_time = (
                    save_attendance(
                        recognized_student["name"]
                    )
                )

                # ------------------------------------------------
                # DISPLAY SUCCESS
                # ------------------------------------------------

                st.success(
                    "✅ Face recognized!"
                )

                st.write(
                    f"**Name:** {recognized_student['name']}"
                )

                st.write(
                    f"**Roll No:** {recognized_student['roll_no']}"
                )

                st.write(
                    f"**Department:** {recognized_student['department']}"
                )

                st.write(
                    "**Status:** PRESENT"
                )

                st.write(
                    f"**Date:** {current_date}"
                )

                st.write(
                    f"**Time:** {current_time}"
                )

                # ------------------------------------------------
                # ATTENDANCE MESSAGE
                # ------------------------------------------------

                if attendance_saved:

                    st.success(
                        "✅ Attendance marked successfully!"
                    )

                else:

                    st.info(
                        "ℹ️ Attendance already marked today."
                    )

            # ----------------------------------------------------
            # FACE FOUND BUT NOT RECOGNIZED
            # ----------------------------------------------------

            else:

                st.warning(
                    "⚠️ Face detected, but student was not recognized."
                )

                st.write("**Name:** —")
                st.write("**Roll No:** —")
                st.write("**Department:** —")
                st.write("**Status:** UNKNOWN")


# ============================================================
# SYSTEM INFORMATION
# ============================================================

st.divider()

st.subheader("📊 System Information")

col1, col2, col3 = st.columns(3)


# ------------------------------------------------------------
# FACE DATABASE
# ------------------------------------------------------------

with col1:

    if encodings_loaded:

        st.success(
            f"Face database: {len(known_names)} encodings"
        )

    else:

        st.error(
            "Face database unavailable"
        )


# ------------------------------------------------------------
# REGISTERED STUDENTS
# ------------------------------------------------------------

with col2:

    st.info(
        f"Registered students: {len(students)}"
    )


# ------------------------------------------------------------
# CAMERA STATUS
# ------------------------------------------------------------

with col3:

    st.info(
        "Browser camera: Ready"
    )