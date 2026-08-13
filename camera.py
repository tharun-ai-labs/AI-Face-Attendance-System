import os
import numpy as np
import cv2
import face_recognition
import pickle

from attendance import mark_attendance
from PIL import Image, ImageTk
from students import get_student_details
from datetime import datetime


# ============================================================
# GLOBAL VARIABLES
# ============================================================

video = None

camera_label = None

running = False

name_label = None
status_label = None
roll_label = None
department_label = None

known_encodings = []
known_names = []


# ============================================================
# ATTENDANCE CONTROL
# ============================================================

# Students whose attendance has already been processed
# during the current day.

marked_names_today = set()

marked_date = None


# ============================================================
# BASE FOLDER
# ============================================================

BASE_FOLDER = os.path.dirname(
    os.path.abspath(__file__)
)


# ============================================================
# ENCODINGS FILE
# ============================================================

ENCODINGS_FILE = os.path.join(
    BASE_FOLDER,
    "encodings",
    "encodings.pkl"
)


# ============================================================
# LOAD FACE ENCODINGS
# ============================================================

def load_face_encodings():

    global known_encodings
    global known_names

    known_encodings = []
    known_names = []

    if not os.path.exists(ENCODINGS_FILE):

        print("ERROR: encodings.pkl not found!")

        return False

    try:

        with open(
            ENCODINGS_FILE,
            "rb"
        ) as f:

            data = pickle.load(f)

        if isinstance(data, tuple) and len(data) == 2:

            known_encodings = data[0]
            known_names = data[1]

        else:

            print(
                "ERROR: Invalid encodings.pkl format."
            )

            return False

        print(
            "Face encodings loaded successfully."
        )

        print(
            "Total registered faces:",
            len(known_names)
        )

        return True

    except Exception as e:

        print(
            "Error loading face encodings:",
            e
        )

        known_encodings = []
        known_names = []

        return False


# Load encodings when camera.py starts
load_face_encodings()


# ============================================================
# RESET STUDENT INFORMATION
# ============================================================

def reset_student_information():

    if name_label:

        name_label.config(
            text="Name : --------"
        )

    if roll_label:

        roll_label.config(
            text="Roll No : --------"
        )

    if department_label:

        department_label.config(
            text="Department : --------"
        )

    if status_label:

        status_label.config(
            text="Status : Waiting...",
            fg="#FB8C00"
        )


# ============================================================
# SHOW UNKNOWN STUDENT
# ============================================================

def show_unknown_student():

    if name_label:

        name_label.config(
            text="Name : Unknown"
        )

    if roll_label:

        roll_label.config(
            text="Roll No : --------"
        )

    if department_label:

        department_label.config(
            text="Department : --------"
        )

    if status_label:

        status_label.config(
            text="Status : Unknown ❌",
            fg="#E53935"
        )


# ============================================================
# UPDATE STUDENT INFORMATION
# ============================================================

def update_student_information(name):

    student = {
        "roll_no": "--------",
        "department": "--------"
    }

    try:

        result = get_student_details(name)

        if isinstance(result, dict):

            student = result

    except Exception as e:

        print(
            "Student details error:",
            e
        )

    # --------------------------------------------------------
    # NAME
    # --------------------------------------------------------

    if name_label:

        name_label.config(
            text=f"Name : {name}"
        )

    # --------------------------------------------------------
    # ROLL NUMBER
    # --------------------------------------------------------

    if roll_label:

        roll_label.config(
            text=(
                "Roll No : "
                + str(
                    student.get(
                        "roll_no",
                        "--------"
                    )
                )
            )
        )

    # --------------------------------------------------------
    # DEPARTMENT
    # --------------------------------------------------------

    if department_label:

        department_label.config(
            text=(
                "Department : "
                + str(
                    student.get(
                        "department",
                        "--------"
                    )
                )
            )
        )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    if status_label:

        status_label.config(
            text="Status : Present ✅",
            fg="#43A047"
        )


# ============================================================
# MARK ATTENDANCE ONCE PER DAY
# ============================================================

def mark_attendance_once(name):

    global marked_names_today
    global marked_date

    # --------------------------------------------------------
    # TODAY
    # --------------------------------------------------------

    today = datetime.now().date()

    # --------------------------------------------------------
    # RESET MEMORY WHEN NEW DAY STARTS
    # --------------------------------------------------------

    if marked_date != today:

        marked_names_today.clear()

        marked_date = today

    # --------------------------------------------------------
    # CLEAN NAME
    # --------------------------------------------------------

    clean_name = str(
        name
    ).strip()

    if not clean_name:

        return

    # --------------------------------------------------------
    # NORMALIZED NAME
    # --------------------------------------------------------

    name_key = clean_name.lower()

    # --------------------------------------------------------
    # ALREADY PROCESSED BY CAMERA
    # --------------------------------------------------------

    if name_key in marked_names_today:

        return

    # --------------------------------------------------------
    # REMEMBER IMMEDIATELY
    # --------------------------------------------------------

    marked_names_today.add(
        name_key
    )

    # --------------------------------------------------------
    # MARK ATTENDANCE
    # --------------------------------------------------------

    try:

        result = mark_attendance(
            clean_name
        )

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        if result is True:

            print(
                f"{clean_name} attendance marked successfully."
            )

        # ----------------------------------------------------
        # ALREADY EXISTS
        # ----------------------------------------------------

        elif result is False:

            print(
                f"{clean_name} already marked today."
            )

        # ----------------------------------------------------
        # OTHER RESULT
        # ----------------------------------------------------

        else:

            print(
                f"Attendance result for "
                f"{clean_name}: {result}"
            )

    except Exception as e:

        # If attendance failed,
        # allow retry.

        marked_names_today.discard(
            name_key
        )

        print(
            f"Attendance error for "
            f"{clean_name}: {e}"
        )


# ============================================================
# FIND BEST FACE MATCH
# ============================================================

def find_best_match(face_encoding):

    if len(known_encodings) == 0:

        return "Unknown"

    try:

        matches = face_recognition.compare_faces(
            known_encodings,
            face_encoding,
            tolerance=0.5
        )

        face_distances = face_recognition.face_distance(
            known_encodings,
            face_encoding
        )

        if len(face_distances) == 0:

            return "Unknown"

        best_match_index = np.argmin(
            face_distances
        )

        if matches[best_match_index]:

            return known_names[
                best_match_index
            ]

    except Exception as e:

        print(
            "Face matching error:",
            e
        )

    return "Unknown"


# ============================================================
# UPDATE CAMERA
# ============================================================

def update_camera():

    global video
    global running

    # --------------------------------------------------------
    # CAMERA NOT RUNNING
    # --------------------------------------------------------

    if not running:

        return

    # --------------------------------------------------------
    # CAMERA OBJECT NOT AVAILABLE
    # --------------------------------------------------------

    if video is None:

        running = False

        return

    # --------------------------------------------------------
    # READ FRAME
    # --------------------------------------------------------

    ret, frame = video.read()

    if not ret:

        print(
            "Unable to read camera frame."
        )

        if camera_label and running:

            camera_label.after(
                100,
                update_camera
            )

        return

    # --------------------------------------------------------
    # MIRROR CAMERA
    # --------------------------------------------------------

    frame = cv2.flip(
        frame,
        1
    )

    # --------------------------------------------------------
    # CONVERT BGR TO RGB
    # --------------------------------------------------------

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    # --------------------------------------------------------
    # DETECT FACES
    # --------------------------------------------------------

    try:

        locations = face_recognition.face_locations(
            rgb
        )

        encodings = face_recognition.face_encodings(
            rgb,
            locations
        )

    except Exception as e:

        print(
            "Face detection error:",
            e
        )

        if running and camera_label:

            camera_label.after(
                100,
                update_camera
            )

        return

    # --------------------------------------------------------
    # NO FACE DETECTED
    # --------------------------------------------------------

    if len(locations) == 0:

        reset_student_information()

    # --------------------------------------------------------
    # PROCESS EACH FACE
    # --------------------------------------------------------

    for (
        top,
        right,
        bottom,
        left
    ), face_encoding in zip(
        locations,
        encodings
    ):

        # ----------------------------------------------------
        # DEFAULT
        # ----------------------------------------------------

        name = "Unknown"

        # ----------------------------------------------------
        # FIND MATCH
        # ----------------------------------------------------

        name = find_best_match(
            face_encoding
        )

        # ----------------------------------------------------
        # KNOWN STUDENT
        # ----------------------------------------------------

        if name != "Unknown":

            update_student_information(
                name
            )

            mark_attendance_once(
                name
            )

        # ----------------------------------------------------
        # UNKNOWN STUDENT
        # ----------------------------------------------------

        else:

            show_unknown_student()

        # ====================================================
        # FACE RECTANGLE COLOR
        # ====================================================

        if name != "Unknown":

            rectangle_color = (
                0,
                255,
                0
            )

        else:

            rectangle_color = (
                0,
                0,
                255
            )

        # ====================================================
        # FACE RECTANGLE
        # ====================================================

        cv2.rectangle(
            frame,
            (left, top),
            (right, bottom),
            rectangle_color,
            2
        )

        # ====================================================
        # NAME BACKGROUND
        # ====================================================

        label_top = max(
            bottom - 35,
            0
        )

        cv2.rectangle(
            frame,
            (
                left,
                label_top
            ),
            (
                right,
                bottom
            ),
            rectangle_color,
            cv2.FILLED
        )

        # ====================================================
        # DISPLAY NAME
        # ====================================================

        cv2.putText(
            frame,
            name,
            (
                left + 6,
                bottom - 10
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

    # ========================================================
    # CONVERT FRAME FOR TKINTER
    # ========================================================

    frame_rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    img = Image.fromarray(
        frame_rgb
    )

    # ========================================================
    # CAMERA DISPLAY SIZE
    # ========================================================

    img = img.resize(
        (640, 480),
        Image.Resampling.LANCZOS
    )

    photo = ImageTk.PhotoImage(
        img
    )

    # ========================================================
    # DISPLAY CAMERA
    # ========================================================

    if camera_label:

        camera_label.configure(
            image=photo,
            text=""
        )

        camera_label.image = photo

        # ----------------------------------------------------
        # CONTINUE CAMERA LOOP
        # ----------------------------------------------------

        if running:

            camera_label.after(
                30,
                update_camera
            )


# ============================================================
# START CAMERA
# ============================================================

def start_camera():

    global video
    global running
    global marked_names_today
    global marked_date

    # --------------------------------------------------------
    # ALREADY RUNNING
    # --------------------------------------------------------

    if running:

        print(
            "Camera is already running."
        )

        return

    # --------------------------------------------------------
    # RESET DAILY CONTROL
    # --------------------------------------------------------

    today = datetime.now().date()

    if marked_date != today:

        marked_names_today.clear()

        marked_date = today

    # --------------------------------------------------------
    # LOAD ENCODINGS AGAIN
    # --------------------------------------------------------

    if len(known_encodings) == 0:

        load_face_encodings()

    # --------------------------------------------------------
    # OPEN CAMERA
    # --------------------------------------------------------

    video = cv2.VideoCapture(
        0,
        cv2.CAP_DSHOW
    )

    # --------------------------------------------------------
    # CHECK CAMERA
    # --------------------------------------------------------

    if not video.isOpened():

        print(
            "ERROR: Camera could not be opened."
        )

        video.release()

        video = None

        if camera_label:

            camera_label.config(
                image="",
                text="❌ Camera Not Available",
                bg="black",
                fg="red",
                font=(
                    "Arial",
                    18,
                    "bold"
                )
            )

        if status_label:

            status_label.config(
                text="Status : Camera Error",
                fg="#E53935"
            )

        return

    # --------------------------------------------------------
    # CAMERA SETTINGS
    # --------------------------------------------------------

    video.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        640
    )

    video.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        480
    )

    # --------------------------------------------------------
    # START CAMERA
    # --------------------------------------------------------

    running = True

    reset_student_information()

    print(
        "Camera started successfully."
    )

    # --------------------------------------------------------
    # START CAMERA LOOP
    # --------------------------------------------------------

    update_camera()


# ============================================================
# STOP CAMERA
# ============================================================

def stop_camera():

    global video
    global running

    # --------------------------------------------------------
    # CAMERA ALREADY STOPPED
    # --------------------------------------------------------

    if not running and video is None:

        return

    # --------------------------------------------------------
    # STOP LOOP
    # --------------------------------------------------------

    running = False

    # --------------------------------------------------------
    # RELEASE CAMERA
    # --------------------------------------------------------

    if video is not None:

        try:

            video.release()

        except Exception:

            pass

        video = None

    # --------------------------------------------------------
    # RESET CAMERA DISPLAY
    # --------------------------------------------------------

    if camera_label:

        camera_label.config(
            image="",
            text="📷 Camera Preview\n\nPress START CAMERA",
            bg="black",
            fg="white",
            font=(
                "Arial",
                18,
                "bold"
            )
        )

        camera_label.image = None

    # --------------------------------------------------------
    # RESET STUDENT INFORMATION
    # --------------------------------------------------------

    reset_student_information()

    print(
        "Camera stopped."
    )