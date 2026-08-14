import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
from datetime import datetime


# ============================================================
# COLORS
# ============================================================

BG_COLOR = "#F4F7FB"
HEADER_COLOR = "#0D47A1"
CARD_COLOR = "#FFFFFF"
TEXT_COLOR = "#263238"
SECONDARY_TEXT = "#607D8B"

GREEN = "#43A047"
ORANGE = "#FB8C00"
PURPLE = "#8E44AD"
BLUE = "#2196F3"
RED = "#E53935"
TEAL = "#00897B"
DARK = "#263238"


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title("AI Face Attendance System")
root.geometry("1200x780")
root.resizable(False, False)
root.configure(bg=BG_COLOR)


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(
    root,
    bg=HEADER_COLOR,
    height=75
)

header.pack(fill="x")
header.pack_propagate(False)


title_label = tk.Label(
    header,
    text="AI FACE ATTENDANCE SYSTEM",
    font=("Arial", 23, "bold"),
    bg=HEADER_COLOR,
    fg="white"
)

title_label.pack(pady=18)


# ============================================================
# SUBTITLE
# ============================================================

subtitle_label = tk.Label(
    header,
    text="Smart • Secure • Automated Attendance",
    font=("Arial", 9),
    bg=HEADER_COLOR,
    fg="#D6E4FF"
)

subtitle_label.place(
    relx=0.5,
    y=58,
    anchor="center"
)


# ============================================================
# STATISTICS FRAME
# ============================================================

statistics_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

statistics_frame.pack(
    fill="x",
    padx=25,
    pady=(12, 5)
)


for i in range(3):
    statistics_frame.grid_columnconfigure(
        i,
        weight=1
    )


# ============================================================
# STATISTICS CARD
# ============================================================

def create_stat_card(
    parent,
    title,
    value,
    icon,
    color,
    column
):

    card = tk.Frame(
        parent,
        bg=CARD_COLOR,
        highlightbackground="#D6DEE8",
        highlightthickness=1,
        height=78
    )

    card.grid(
        row=0,
        column=column,
        padx=6,
        sticky="ew"
    )

    card.grid_propagate(False)

    icon_label = tk.Label(
        card,
        text=icon,
        font=("Arial", 21),
        bg=CARD_COLOR,
        fg=color
    )

    icon_label.pack(
        side="left",
        padx=(15, 8)
    )

    text_frame = tk.Frame(
        card,
        bg=CARD_COLOR
    )

    text_frame.pack(
        side="left",
        pady=8
    )

    title_label = tk.Label(
        text_frame,
        text=title,
        font=("Arial", 9, "bold"),
        bg=CARD_COLOR,
        fg=SECONDARY_TEXT
    )

    title_label.pack(
        anchor="w"
    )

    value_label = tk.Label(
        text_frame,
        text=value,
        font=("Arial", 17, "bold"),
        bg=CARD_COLOR,
        fg=color
    )

    value_label.pack(
        anchor="w"
    )

    return value_label


# ============================================================
# STATISTICS VALUES
# ============================================================

total_students_label = create_stat_card(
    statistics_frame,
    "TOTAL STUDENTS",
    "0",
    "👥",
    PURPLE,
    0
)


present_today_label = create_stat_card(
    statistics_frame,
    "PRESENT TODAY",
    "0",
    "✅",
    GREEN,
    1
)


total_records_label = create_stat_card(
    statistics_frame,
    "TOTAL RECORDS",
    "0",
    "📋",
    BLUE,
    2
)


# ============================================================
# MAIN CONTENT
# ============================================================

main_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=10
)


main_frame.grid_columnconfigure(
    0,
    weight=7
)

main_frame.grid_columnconfigure(
    1,
    weight=3
)


# ============================================================
# CAMERA CARD
# ============================================================

camera_card = tk.Frame(
    main_frame,
    bg=CARD_COLOR,
    highlightbackground="#D6DEE8",
    highlightthickness=1
)

camera_card.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=(0, 12)
)


# ============================================================
# CAMERA TITLE
# ============================================================

camera_title_frame = tk.Frame(
    camera_card,
    bg=CARD_COLOR
)

camera_title_frame.pack(
    fill="x",
    padx=15,
    pady=(10, 5)
)


camera_title = tk.Label(
    camera_title_frame,
    text="📷  CAMERA PREVIEW",
    font=("Arial", 14, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

camera_title.pack(
    side="left"
)


# ============================================================
# CAMERA STATUS
# ============================================================

camera_status_label = tk.Label(
    camera_title_frame,
    text="● CAMERA OFF",
    font=("Arial", 9, "bold"),
    bg=CARD_COLOR,
    fg=RED
)

camera_status_label.pack(
    side="right"
)


# ============================================================
# CAMERA PREVIEW
# ============================================================

camera_frame = tk.Frame(
    camera_card,
    bg="#111111",
    width=700,
    height=365
)

camera_frame.pack(
    padx=15,
    pady=(5, 15)
)

camera_frame.pack_propagate(False)


camera_label = tk.Label(
    camera_frame,
    text="📷\n\nCamera Preview\n\nPress Start Camera",
    font=("Arial", 17, "bold"),
    bg="#111111",
    fg="white",
    justify="center"
)

camera_label.pack(
    fill="both",
    expand=True
)


# ============================================================
# STUDENT INFORMATION CARD
# ============================================================

student_card = tk.Frame(
    main_frame,
    bg=CARD_COLOR,
    highlightbackground="#D6DEE8",
    highlightthickness=1
)

student_card.grid(
    row=0,
    column=1,
    sticky="nsew",
    padx=(12, 0)
)


# ============================================================
# STUDENT HEADER
# ============================================================

student_header = tk.Label(
    student_card,
    text="👨‍🎓  STUDENT INFORMATION",
    font=("Arial", 14, "bold"),
    bg=HEADER_COLOR,
    fg="white",
    anchor="w",
    padx=15,
    pady=12
)

student_header.pack(
    fill="x"
)


# ============================================================
# ATTENDANCE COUNT
# ============================================================

attendance_count_label = tk.Label(
    student_card,
    text="Today's Attendance : 0",
    font=("Arial", 12, "bold"),
    bg="#EAF2FF",
    fg=HEADER_COLOR,
    padx=8,
    pady=9
)

attendance_count_label.pack(
    fill="x",
    padx=12,
    pady=(12, 10)
)


# ============================================================
# STUDENT DETAILS FRAME
# ============================================================

details_frame = tk.Frame(
    student_card,
    bg=CARD_COLOR
)

details_frame.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=5
)


# ============================================================
# NAME
# ============================================================

name_label = tk.Label(
    details_frame,
    text="Name : --------",
    font=("Arial", 13, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    anchor="w"
)

name_label.pack(
    fill="x",
    pady=6
)


# ============================================================
# ROLL NUMBER
# ============================================================

roll_label = tk.Label(
    details_frame,
    text="Roll No : --------",
    font=("Arial", 13),
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT,
    anchor="w"
)

roll_label.pack(
    fill="x",
    pady=6
)


# ============================================================
# DEPARTMENT
# ============================================================

department_label = tk.Label(
    details_frame,
    text="Department : --------",
    font=("Arial", 13),
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT,
    anchor="w"
)

department_label.pack(
    fill="x",
    pady=6
)


# ============================================================
# STATUS
# ============================================================

status_label = tk.Label(
    details_frame,
    text="Status : Waiting...",
    font=("Arial", 13, "bold"),
    bg=CARD_COLOR,
    fg=ORANGE,
    anchor="w"
)

status_label.pack(
    fill="x",
    pady=6
)


# ============================================================
# DATE
# ============================================================

date_label = tk.Label(
    details_frame,
    text="Date : --/--/----",
    font=("Arial", 13),
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT,
    anchor="w"
)

date_label.pack(
    fill="x",
    pady=6
)


# ============================================================
# TIME
# ============================================================

time_label = tk.Label(
    details_frame,
    text="Time : --:--:--",
    font=("Arial", 13),
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT,
    anchor="w"
)

time_label.pack(
    fill="x",
    pady=6
)


# ============================================================
# IMPORT CAMERA
# ============================================================

camera = None

try:

    import camera

    camera.camera_label = camera_label
    camera.name_label = name_label
    camera.status_label = status_label
    camera.roll_label = roll_label
    camera.department_label = department_label

except Exception as e:

    messagebox.showerror(
        "Camera Module Error",
        f"Unable to load camera.py\n\n{e}"
    )


# ============================================================
# BUTTON FRAME
# ============================================================

button_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

button_frame.pack(
    fill="x",
    padx=25,
    pady=(5, 5)
)


# ============================================================
# BUTTON GRID
# ============================================================

for i in range(7):

    button_frame.grid_columnconfigure(
        i,
        weight=1
    )


# ============================================================
# BUTTON FUNCTION
# ============================================================

def create_button(
    parent,
    text,
    bg,
    command,
    column
):

    button = tk.Button(
        parent,
        text=text,
        bg=bg,
        fg="white",
        activebackground=bg,
        activeforeground="white",
        font=("Arial", 9, "bold"),
        relief="flat",
        bd=0,
        cursor="hand2",
        height=2,
        command=command
    )

    button.grid(
        row=0,
        column=column,
        padx=4,
        sticky="ew"
    )

    return button


# ============================================================
# START CAMERA
# ============================================================

def start_camera():

    if camera is None:

        messagebox.showerror(
            "Camera Error",
            "camera.py could not be loaded."
        )

        return

    try:

        camera.start_camera()

        camera_status_label.config(
            text="● CAMERA ON",
            fg=GREEN
        )

        status_label.config(
            text="Status : Camera Running",
            fg=GREEN
        )

    except Exception as e:

        messagebox.showerror(
            "Camera Error",
            f"Unable to start camera.\n\n{e}"
        )


start_button = create_button(
    button_frame,
    "▶ Start",
    GREEN,
    start_camera,
    0
)


# ============================================================
# STOP CAMERA
# ============================================================

def stop_camera():

    if camera is None:
        return

    try:

        camera.stop_camera()

        camera_status_label.config(
            text="● CAMERA OFF",
            fg=RED
        )

        status_label.config(
            text="Status : Camera Stopped",
            fg=ORANGE
        )

    except Exception as e:

        messagebox.showerror(
            "Camera Error",
            f"Unable to stop camera.\n\n{e}"
        )


stop_button = create_button(
    button_frame,
    "⏹ Stop",
    ORANGE,
    stop_camera,
    1
)


# ============================================================
# REGISTER FACE
# ============================================================

def open_register_face():

    register_file = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
        ),
        "register_face.py"
    )

    if not os.path.exists(register_file):

        messagebox.showerror(
            "Error",
            "register_face.py not found!"
        )

        return

    try:

        subprocess.Popen(
            [
                sys.executable,
                register_file
            ]
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"Unable to open Register Face.\n\n{e}"
        )


register_button = create_button(
    button_frame,
    "➕ Register",
    PURPLE,
    open_register_face,
    2
)


# ============================================================
# VIEW ATTENDANCE
# ============================================================

def view_attendance():

    file_path = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
        ),
        "attendance",
        "attendance.xlsx"
    )

    if not os.path.exists(file_path):

        messagebox.showerror(
            "Error",
            "Attendance file not found!"
        )

        return

    try:

        df = pd.read_excel(
            file_path
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"Unable to read attendance file.\n\n{e}"
        )

        return


    attendance_window = tk.Toplevel(
        root
    )

    attendance_window.title(
        "Attendance Records"
    )

    attendance_window.geometry(
        "950x620"
    )

    attendance_window.resizable(
        False,
        False
    )

    attendance_window.configure(
        bg=BG_COLOR
    )


    attendance_header = tk.Frame(
        attendance_window,
        bg=HEADER_COLOR,
        height=70
    )

    attendance_header.pack(
        fill="x"
    )

    attendance_header.pack_propagate(
        False
    )


    tk.Label(
        attendance_header,
        text="📋 ATTENDANCE RECORDS",
        font=("Arial", 20, "bold"),
        bg=HEADER_COLOR,
        fg="white"
    ).pack(
        pady=18
    )


    total_label = tk.Label(
        attendance_window,
        text=f"Total Attendance Records : {len(df)}",
        font=("Arial", 12, "bold"),
        bg=BG_COLOR,
        fg=HEADER_COLOR
    )

    total_label.pack(
        pady=10
    )


    search_frame = tk.Frame(
        attendance_window,
        bg=BG_COLOR
    )

    search_frame.pack(
        pady=5
    )


    tk.Label(
        search_frame,
        text="🔍 Search Student :",
        font=("Arial", 11, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(
        side="left",
        padx=5
    )


    search_entry = tk.Entry(
        search_frame,
        width=30,
        font=("Arial", 11),
        relief="solid",
        bd=1
    )

    search_entry.pack(
        side="left",
        padx=5
    )


    table_frame = tk.Frame(
        attendance_window,
        bg="white"
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )


    columns = list(df.columns)


    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )


    style = ttk.Style()

    try:

        style.theme_use("clam")

    except Exception:

        pass


    style.configure(
        "Treeview",
        font=("Arial", 10),
        rowheight=30,
        background="white",
        fieldbackground="white"
    )


    style.configure(
        "Treeview.Heading",
        font=("Arial", 10, "bold")
    )


    for column in columns:

        tree.heading(
            column,
            text=column
        )

        tree.column(
            column,
            width=180,
            anchor="center"
        )


    for _, row in df.iterrows():

        tree.insert(
            "",
            "end",
            values=list(row)
        )


    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )

    tree.configure(
        yscrollcommand=scrollbar.set
    )


    tree.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )


    def search_student():

        search_text = (
            search_entry
            .get()
            .lower()
            .strip()
        )


        for item in tree.get_children():

            tree.delete(item)


        if search_text == "":

            filtered_df = df

        else:

            filtered_df = df[
                df.astype(str)
                .apply(
                    lambda row:
                    row.str.lower()
                    .str.contains(
                        search_text,
                        na=False
                    ).any(),
                    axis=1
                )
            ]


        for _, row in filtered_df.iterrows():

            tree.insert(
                "",
                "end",
                values=list(row)
            )


    tk.Button(
        search_frame,
        text="Search",
        width=10,
        bg=BLUE,
        fg="white",
        activebackground=BLUE,
        activeforeground="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
        command=search_student
    ).pack(
        side="left",
        padx=5
    )


    tk.Button(
        attendance_window,
        text="✖ Close",
        width=15,
        height=2,
        bg=RED,
        fg="white",
        activebackground=RED,
        activeforeground="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
        command=attendance_window.destroy
    ).pack(
        pady=15
    )


view_button = create_button(
    button_frame,
    "📄 Attendance",
    BLUE,
    view_attendance,
    3
)


# ============================================================
# OPEN ANALYTICS
# ============================================================

def open_analytics():

    analytics_file = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
        ),
        "analytics.py"
    )

    if not os.path.exists(analytics_file):

        messagebox.showerror(
            "Error",
            "analytics.py not found!"
        )

        return

    try:

        subprocess.Popen(
            [
                sys.executable,
                analytics_file
            ]
        )

    except Exception as e:

        messagebox.showerror(
            "Analytics Error",
            f"Unable to open Analytics.\n\n{e}"
        )


analytics_button = create_button(
    button_frame,
    "📊 Analytics",
    TEAL,
    open_analytics,
    4
)


# ============================================================
# STUDENT MANAGEMENT
# ============================================================

def open_students():

    students_file = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
        ),
        "students.py"
    )

    if not os.path.exists(students_file):

        messagebox.showerror(
            "Student Management",
            "students.py not found!"
        )

        return

    try:

        subprocess.Popen(
            [
                sys.executable,
                students_file
            ]
        )

    except Exception as e:

        messagebox.showerror(
            "Student Management Error",
            f"Unable to open students.py.\n\n{e}"
        )


students_button = create_button(
    button_frame,
    "👨‍🎓 Students",
    DARK,
    open_students,
    5
)


# ============================================================
# REFRESH BUTTON
# ============================================================

def manual_refresh():

    update_statistics()

    status_label.config(
        text="Status : Dashboard Refreshed",
        fg=BLUE
    )


refresh_button = create_button(
    button_frame,
    "🔄 Refresh",
    BLUE,
    manual_refresh,
    6
)


# ============================================================
# EXIT BUTTON
# ============================================================

def exit_application():

    try:

        if camera is not None:

            camera.stop_camera()

    except Exception:

        pass

    root.destroy()


# ============================================================
# FOOTER BUTTON
# ============================================================

exit_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

exit_frame.pack(
    fill="x",
    padx=25,
    pady=(0, 8)
)


tk.Button(
    exit_frame,
    text="❌ Exit Application",
    width=20,
    height=1,
    bg=RED,
    fg="white",
    activebackground=RED,
    activeforeground="white",
    font=("Arial", 9, "bold"),
    relief="flat",
    cursor="hand2",
    command=exit_application
).pack(
    side="right"
)


# ============================================================
# UPDATE DATE AND TIME
# ============================================================

def update_time():

    now = datetime.now()

    date_label.config(
        text="Date : " +
        now.strftime("%d-%m-%Y")
    )

    time_label.config(
        text="Time : " +
        now.strftime("%H:%M:%S")
    )

    root.after(
        1000,
        update_time
    )


# ============================================================
# GET TOTAL STUDENTS
# ============================================================

def get_total_students():

    try:

        from students import students

        if isinstance(
            students,
            dict
        ):

            return len(students)

    except Exception:

        pass

    return 0


# ============================================================
# CONVERT ATTENDANCE DATES
# ============================================================

def convert_attendance_dates(
    date_series
):

    converted_dates = pd.Series(
        pd.NaT,
        index=date_series.index,
        dtype="datetime64[ns]"
    )


    numeric_values = pd.to_numeric(
        date_series,
        errors="coerce"
    )


    numeric_mask = (
        numeric_values.notna()
    )


    if numeric_mask.any():

        converted_dates.loc[
            numeric_mask
        ] = pd.to_datetime(
            numeric_values.loc[
                numeric_mask
            ],
            unit="D",
            origin="1899-12-30",
            errors="coerce"
        )


    text_mask = (
        ~numeric_mask
    )


    if text_mask.any():

        text_values = (
            date_series
            .loc[text_mask]
            .astype(str)
            .str.strip()
        )


        converted_text = pd.to_datetime(
            text_values,
            format="%Y-%m-%d",
            errors="coerce"
        )


        remaining_mask = (
            converted_text.isna()
        )


        if remaining_mask.any():

            converted_text.loc[
                remaining_mask
            ] = pd.to_datetime(
                text_values.loc[
                    remaining_mask
                ],
                format="%d-%m-%Y",
                errors="coerce"
            )


        remaining_mask = (
            converted_text.isna()
        )


        if remaining_mask.any():

            converted_text.loc[
                remaining_mask
            ] = pd.to_datetime(
                text_values.loc[
                    remaining_mask
                ],
                format="%d/%m/%Y",
                errors="coerce"
            )


        converted_dates.loc[
            text_mask
        ] = converted_text


    return converted_dates


# ============================================================
# UPDATE STATISTICS
# ============================================================

def update_statistics():

    file_name = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
        ),
        "attendance",
        "attendance.xlsx"
    )


    total_students = get_total_students()


    total_students_label.config(
        text=str(total_students)
    )


    present_today = 0
    total_records = 0


    if os.path.exists(file_name):

        try:

            df = pd.read_excel(
                file_name
            )


            total_records = len(df)


            if (
                "Date" in df.columns
                and not df.empty
            ):

                dates = convert_attendance_dates(
                    df["Date"]
                )


                today = datetime.now().date()


                today_attendance = df[
                    dates.dt.date == today
                ]


                present_today = len(
                    today_attendance
                )


        except Exception as e:

            print(
                "Statistics error:",
                e
            )


    present_today_label.config(
        text=str(present_today)
    )


    total_records_label.config(
        text=str(total_records)
    )


    attendance_count_label.config(
        text=
        f"Today's Attendance : "
        f"{present_today}"
    )


    root.after(
        5000,
        update_statistics
    )


# ============================================================
# WINDOW CLOSE
# ============================================================

root.protocol(
    "WM_DELETE_WINDOW",
    exit_application
)


# ============================================================
# START DATE/TIME
# ============================================================

update_time()


# ============================================================
# START STATISTICS
# ============================================================

update_statistics()


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()