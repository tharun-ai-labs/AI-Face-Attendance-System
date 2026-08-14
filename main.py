import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import subprocess
import sys
import pandas as pd

import camera

from students import (
    open_student_management,
    get_total_students
)


# ============================================================
# COLORS
# ============================================================

BG_COLOR = "#F4F7FB"
HEADER_COLOR = "#0D47A1"
CARD_COLOR = "#FFFFFF"

TEXT_COLOR = "#263238"
SECONDARY_TEXT = "#607D8B"

GREEN = "#43A047"
BLUE = "#2196F3"
PURPLE = "#8E44AD"
ORANGE = "#FB8C00"
RED = "#E53935"
GRAY = "#607D8B"


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title("AI Face Attendance System")

# Screen is 1366 x 768
root.geometry("1200x700")

root.minsize(1000, 620)
root.resizable(True, True)

root.configure(bg=BG_COLOR)


# ============================================================
# WINDOW CLOSE
# ============================================================

def close_application():

    try:
        camera.stop_camera()
    except Exception:
        pass

    root.destroy()


root.protocol(
    "WM_DELETE_WINDOW",
    close_application
)


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(
    root,
    bg=HEADER_COLOR,
    height=65
)

header.pack(fill="x")
header.pack_propagate(False)


tk.Label(
    header,
    text="🤖  AI FACE ATTENDANCE SYSTEM",
    font=("Arial", 20, "bold"),
    bg=HEADER_COLOR,
    fg="white"
).pack(
    side="left",
    padx=25,
    pady=15
)


# ============================================================
# DATE AND TIME
# ============================================================

datetime_frame = tk.Frame(
    header,
    bg=HEADER_COLOR
)

datetime_frame.pack(
    side="right",
    padx=20
)


date_label = tk.Label(
    datetime_frame,
    text="Date: --",
    font=("Arial", 9, "bold"),
    bg=HEADER_COLOR,
    fg="white"
)

date_label.pack(anchor="e")


time_label = tk.Label(
    datetime_frame,
    text="Time: --",
    font=("Arial", 9, "bold"),
    bg=HEADER_COLOR,
    fg="white"
)

time_label.pack(anchor="e")


def update_datetime():

    now = datetime.now()

    date_label.config(
        text="Date: " + now.strftime("%d-%m-%Y")
    )

    time_label.config(
        text="Time: " + now.strftime("%H:%M:%S")
    )

    root.after(
        1000,
        update_datetime
    )


update_datetime()


# ============================================================
# FOOTER
# ============================================================

footer = tk.Label(
    root,
    text=(
        "AI Face Attendance System  |  "
        "Face Recognition • Student Management • "
        "Attendance • Analytics"
    ),
    font=("Arial", 8),
    bg=HEADER_COLOR,
    fg="white",
    height=2
)

footer.pack(
    fill="x",
    side="bottom"
)


# ============================================================
# MAIN CONTAINER
# ============================================================

main_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=12,
    pady=10
)


# ============================================================
# LEFT SIDE
# ============================================================

left_frame = tk.Frame(
    main_frame,
    bg=BG_COLOR
)

left_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 8)
)


# ============================================================
# CAMERA CARD
# ============================================================

camera_card = tk.Frame(
    left_frame,
    bg="black",
    highlightbackground="#D6DEE8",
    highlightthickness=1
)

camera_card.pack(
    fill="both",
    expand=True
)


camera_title = tk.Label(
    camera_card,
    text="📷 LIVE CAMERA",
    font=("Arial", 13, "bold"),
    bg=HEADER_COLOR,
    fg="white",
    height=2
)

camera_title.pack(
    fill="x"
)


# ============================================================
# CAMERA LABEL
# ============================================================

camera.camera_label = tk.Label(
    camera_card,
    text="📷 Camera Preview\n\nPress START CAMERA",
    font=("Arial", 17, "bold"),
    bg="black",
    fg="white"
)

camera.camera_label.pack(
    fill="both",
    expand=True
)


# ============================================================
# CAMERA BUTTON FRAME
# ============================================================

camera_button_frame = tk.Frame(
    left_frame,
    bg=BG_COLOR,
    height=55
)

camera_button_frame.pack(
    fill="x",
    pady=(7, 0)
)

camera_button_frame.pack_propagate(False)


# ============================================================
# START CAMERA
# ============================================================

def start_camera():

    try:

        camera.start_camera()

        try:
            camera.status_label.config(
                text="Status : Camera Running",
                fg=GREEN
            )
        except Exception:
            pass

    except Exception as e:

        messagebox.showerror(
            "Camera Error",
            f"Unable to start camera.\n\n{e}"
        )


start_button = tk.Button(
    camera_button_frame,
    text="▶ START CAMERA",
    height=2,
    bg=GREEN,
    fg="white",
    activebackground="#2E7D32",
    activeforeground="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    cursor="hand2",
    command=start_camera
)

start_button.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 5)
)


# ============================================================
# STOP CAMERA
# ============================================================

def stop_camera():

    try:

        camera.stop_camera()

        try:
            camera.status_label.config(
                text="Status : Camera Stopped",
                fg=RED
            )
        except Exception:
            pass

        try:
            camera.camera_label.config(
                image="",
                text="📷 Camera Preview\n\nPress START CAMERA"
            )
            camera.camera_label.image = None
        except Exception:
            pass

    except Exception as e:

        messagebox.showerror(
            "Camera Error",
            f"Unable to stop camera.\n\n{e}"
        )


stop_button = tk.Button(
    camera_button_frame,
    text="■ STOP CAMERA",
    height=2,
    bg=RED,
    fg="white",
    activebackground="#B71C1C",
    activeforeground="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    cursor="hand2",
    command=stop_camera
)

stop_button.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(5, 0)
)


# ============================================================
# RIGHT OUTER FRAME
# ============================================================

right_outer_frame = tk.Frame(
    main_frame,
    bg=BG_COLOR,
    width=355
)

right_outer_frame.pack(
    side="right",
    fill="y",
    padx=(8, 0)
)

right_outer_frame.pack_propagate(False)


# ============================================================
# RIGHT CANVAS
# ============================================================

right_canvas = tk.Canvas(
    right_outer_frame,
    bg=BG_COLOR,
    highlightthickness=0,
    width=335
)

right_canvas.pack(
    side="left",
    fill="both",
    expand=True
)


# ============================================================
# RIGHT SCROLLBAR
# ============================================================

right_scrollbar = ttk.Scrollbar(
    right_outer_frame,
    orient="vertical",
    command=right_canvas.yview
)

right_scrollbar.pack(
    side="right",
    fill="y"
)

right_canvas.configure(
    yscrollcommand=right_scrollbar.set
)


# ============================================================
# RIGHT INNER FRAME
# ============================================================

right_frame = tk.Frame(
    right_canvas,
    bg=BG_COLOR
)

right_canvas_window = right_canvas.create_window(
    (0, 0),
    window=right_frame,
    anchor="nw"
)


# ============================================================
# UPDATE SCROLL REGION
# ============================================================

def update_right_scroll_region(event=None):

    right_canvas.configure(
        scrollregion=right_canvas.bbox("all")
    )


right_frame.bind(
    "<Configure>",
    update_right_scroll_region
)


# ============================================================
# RESIZE RIGHT FRAME
# ============================================================

def resize_right_frame(event):

    right_canvas.itemconfig(
        right_canvas_window,
        width=event.width
    )


right_canvas.bind(
    "<Configure>",
    resize_right_frame
)


# ============================================================
# MOUSE WHEEL
# ============================================================

def mouse_wheel(event):

    try:
        right_canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )
    except Exception:
        pass


right_canvas.bind_all(
    "<MouseWheel>",
    mouse_wheel
)


# ============================================================
# STUDENT INFORMATION CARD
# ============================================================

student_card = tk.Frame(
    right_frame,
    bg=CARD_COLOR,
    highlightbackground="#D6DEE8",
    highlightthickness=1
)

student_card.pack(
    fill="x",
    pady=(0, 7)
)


tk.Label(
    student_card,
    text="👨‍🎓 STUDENT INFORMATION",
    font=("Arial", 12, "bold"),
    bg=HEADER_COLOR,
    fg="white",
    height=2
).pack(
    fill="x"
)


# ============================================================
# STUDENT NAME
# ============================================================

camera.name_label = tk.Label(
    student_card,
    text="Name : --------",
    font=("Arial", 10, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    anchor="w"
)

camera.name_label.pack(
    fill="x",
    padx=15,
    pady=(8, 3)
)


# ============================================================
# ROLL NUMBER
# ============================================================

camera.roll_label = tk.Label(
    student_card,
    text="Roll No : --------",
    font=("Arial", 10),
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    anchor="w"
)

camera.roll_label.pack(
    fill="x",
    padx=15,
    pady=3
)


# ============================================================
# DEPARTMENT
# ============================================================

camera.department_label = tk.Label(
    student_card,
    text="Department : --------",
    font=("Arial", 10),
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    anchor="w"
)

camera.department_label.pack(
    fill="x",
    padx=15,
    pady=3
)


# ============================================================
# STATUS
# ============================================================

camera.status_label = tk.Label(
    student_card,
    text="Status : Waiting...",
    font=("Arial", 10, "bold"),
    bg=CARD_COLOR,
    fg=ORANGE,
    anchor="w"
)

camera.status_label.pack(
    fill="x",
    padx=15,
    pady=(3, 8)
)


# ============================================================
# STATISTICS CARD
# ============================================================

stats_card = tk.Frame(
    right_frame,
    bg=CARD_COLOR,
    highlightbackground="#D6DEE8",
    highlightthickness=1
)

stats_card.pack(
    fill="x",
    pady=5
)


tk.Label(
    stats_card,
    text="📊 SYSTEM STATISTICS",
    font=("Arial", 12, "bold"),
    bg=PURPLE,
    fg="white",
    height=2
).pack(
    fill="x"
)


total_students_label = tk.Label(
    stats_card,
    text="0",
    font=("Arial", 23, "bold"),
    bg=CARD_COLOR,
    fg=BLUE
)

total_students_label.pack(
    pady=(6, 0)
)


tk.Label(
    stats_card,
    text="Total Registered Students",
    font=("Arial", 9),
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT
).pack(
    pady=(0, 7)
)


# ============================================================
# UPDATE TOTAL STUDENTS
# ============================================================

def update_total_students():

    try:

        total = get_total_students()

        total_students_label.config(
            text=str(total)
        )

    except Exception as e:

        print(
            "Student count error:",
            e
        )

        total_students_label.config(
            text="0"
        )

    root.after(
        3000,
        update_total_students
    )


update_total_students()


# ============================================================
# ATTENDANCE DASHBOARD
# ============================================================

def open_attendance_dashboard():

    dashboard = tk.Toplevel(root)

    dashboard.title(
        "Attendance Dashboard"
    )

    dashboard.geometry(
        "1000x650"
    )

    dashboard.minsize(
        850,
        550
    )

    dashboard.resizable(
        True,
        True
    )

    dashboard.configure(
        bg=BG_COLOR
    )

    # ========================================================
    # DASHBOARD HEADER
    # ========================================================

    dashboard_header = tk.Frame(
        dashboard,
        bg=HEADER_COLOR,
        height=65
    )

    dashboard_header.pack(
        fill="x"
    )

    dashboard_header.pack_propagate(
        False
    )

    tk.Label(
        dashboard_header,
        text="📊 ATTENDANCE DASHBOARD",
        font=("Arial", 20, "bold"),
        bg=HEADER_COLOR,
        fg="white"
    ).pack(
        side="left",
        padx=25,
        pady=16
    )

    # ========================================================
    # STATISTICS FRAME
    # ========================================================

    dashboard_stats = tk.Frame(
        dashboard,
        bg=BG_COLOR
    )

    dashboard_stats.pack(
        fill="x",
        padx=15,
        pady=10
    )

    # ========================================================
    # TOTAL CARD
    # ========================================================

    total_card = tk.Frame(
        dashboard_stats,
        bg=CARD_COLOR,
        highlightbackground="#D6DEE8",
        highlightthickness=1
    )

    total_card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=4
    )

    total_value = tk.Label(
        total_card,
        text="0",
        font=("Arial", 24, "bold"),
        bg=CARD_COLOR,
        fg=BLUE
    )

    total_value.pack(
        pady=(8, 0)
    )

    tk.Label(
        total_card,
        text="Total Students",
        font=("Arial", 9, "bold"),
        bg=CARD_COLOR,
        fg=SECONDARY_TEXT
    ).pack(
        pady=(0, 8)
    )

    # ========================================================
    # PRESENT CARD
    # ========================================================

    present_card = tk.Frame(
        dashboard_stats,
        bg=CARD_COLOR,
        highlightbackground="#D6DEE8",
        highlightthickness=1
    )

    present_card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=4
    )

    present_value = tk.Label(
        present_card,
        text="0",
        font=("Arial", 24, "bold"),
        bg=CARD_COLOR,
        fg=GREEN
    )

    present_value.pack(
        pady=(8, 0)
    )

    tk.Label(
        present_card,
        text="Present Today",
        font=("Arial", 9, "bold"),
        bg=CARD_COLOR,
        fg=SECONDARY_TEXT
    ).pack(
        pady=(0, 8)
    )

    # ========================================================
    # ABSENT CARD
    # ========================================================

    absent_card = tk.Frame(
        dashboard_stats,
        bg=CARD_COLOR,
        highlightbackground="#D6DEE8",
        highlightthickness=1
    )

    absent_card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=4
    )

    absent_value = tk.Label(
        absent_card,
        text="0",
        font=("Arial", 24, "bold"),
        bg=CARD_COLOR,
        fg=RED
    )

    absent_value.pack(
        pady=(8, 0)
    )

    tk.Label(
        absent_card,
        text="Absent Today",
        font=("Arial", 9, "bold"),
        bg=CARD_COLOR,
        fg=SECONDARY_TEXT
    ).pack(
        pady=(0, 8)
    )

    # ========================================================
    # PERCENTAGE CARD
    # ========================================================

    percentage_card = tk.Frame(
        dashboard_stats,
        bg=CARD_COLOR,
        highlightbackground="#D6DEE8",
        highlightthickness=1
    )

    percentage_card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=4
    )

    percentage_value = tk.Label(
        percentage_card,
        text="0%",
        font=("Arial", 24, "bold"),
        bg=CARD_COLOR,
        fg=PURPLE
    )

    percentage_value.pack(
        pady=(8, 0)
    )

    tk.Label(
        percentage_card,
        text="Attendance",
        font=("Arial", 9, "bold"),
        bg=CARD_COLOR,
        fg=SECONDARY_TEXT
    ).pack(
        pady=(0, 8)
    )

    # ========================================================
    # TABLE CARD
    # ========================================================

    table_card = tk.Frame(
        dashboard,
        bg=CARD_COLOR,
        highlightbackground="#D6DEE8",
        highlightthickness=1
    )

    table_card.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=4
    )

    tk.Label(
        table_card,
        text="📋 TODAY'S ATTENDANCE",
        font=("Arial", 13, "bold"),
        bg=CARD_COLOR,
        fg=HEADER_COLOR
    ).pack(
        anchor="w",
        padx=12,
        pady=6
    )

    table_frame = tk.Frame(
        table_card,
        bg="white"
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=12,
        pady=4
    )

    # ========================================================
    # TREEVIEW
    # ========================================================

    columns = (
        "name",
        "date",
        "time"
    )

    attendance_tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    attendance_tree.heading(
        "name",
        text="Student Name"
    )

    attendance_tree.heading(
        "date",
        text="Date"
    )

    attendance_tree.heading(
        "time",
        text="Time"
    )

    attendance_tree.column(
        "name",
        width=300,
        anchor="center"
    )

    attendance_tree.column(
        "date",
        width=200,
        anchor="center"
    )

    attendance_tree.column(
        "time",
        width=200,
        anchor="center"
    )

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=attendance_tree.yview
    )

    attendance_tree.configure(
        yscrollcommand=scrollbar.set
    )

    attendance_tree.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # ========================================================
    # LOAD DASHBOARD DATA
    # ========================================================

    def load_dashboard():

        for item in attendance_tree.get_children():

            attendance_tree.delete(item)

        base_folder = os.path.dirname(
            os.path.abspath(__file__)
        )

        attendance_file = os.path.join(
            base_folder,
            "attendance",
            "attendance.xlsx"
        )

        # ----------------------------------------------------
        # TOTAL STUDENTS
        # ----------------------------------------------------

        try:

            total = get_total_students()

        except Exception as e:

            print(
                "Unable to get student count:",
                e
            )

            total = 0

        total_value.config(
            text=str(total)
        )

        # ----------------------------------------------------
        # FILE DOES NOT EXIST
        # ----------------------------------------------------

        if not os.path.exists(
            attendance_file
        ):

            present_value.config(
                text="0"
            )

            absent_value.config(
                text=str(total)
            )

            percentage_value.config(
                text="0%"
            )

            return

        # ----------------------------------------------------
        # READ EXCEL FILE
        # ----------------------------------------------------

        try:

            df = pd.read_excel(
                attendance_file
            )

        except Exception as e:

            messagebox.showerror(
                "Attendance Error",
                f"Unable to read attendance file.\n\n{e}"
            )

            return

        # ----------------------------------------------------
        # REQUIRED COLUMNS
        # ----------------------------------------------------

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

        # ====================================================
        # NORMALIZE DATE
        # ====================================================

        def normalize_date(value):

            if pd.isna(value):
                return ""

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

            value = value.replace(
                ",",
                ""
            )

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

            # Pandas date conversion
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

        # ----------------------------------------------------
        # NORMALIZE COLUMNS
        # ----------------------------------------------------

        df["Date"] = df[
            "Date"
        ].apply(
            normalize_date
        )

        df["Name"] = (
            df["Name"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        df["Time"] = (
            df["Time"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        # ====================================================
        # TODAY
        # ====================================================

        today = datetime.now().strftime(
            "%d-%m-%Y"
        )

        today_df = df[
            df["Date"] == today
        ].copy()

        today_df = today_df[
            today_df["Name"] != ""
        ]

        # One attendance per student
        today_df = today_df.drop_duplicates(
            subset=["Name"],
            keep="first"
        )

        # ====================================================
        # CALCULATE STATISTICS
        # ====================================================

        present = len(
            today_df
        )

        absent = max(
            total - present,
            0
        )

        if total > 0:

            percentage = (
                present / total
            ) * 100

        else:

            percentage = 0

        # ====================================================
        # UPDATE STATISTICS
        # ====================================================

        present_value.config(
            text=str(present)
        )

        absent_value.config(
            text=str(absent)
        )

        percentage_value.config(
            text=f"{percentage:.1f}%"
        )

        # ====================================================
        # INSERT ATTENDANCE DATA
        # ====================================================

        for _, row in today_df.iterrows():

            attendance_tree.insert(
                "",
                "end",
                values=(
                    row["Name"],
                    row["Date"],
                    row["Time"]
                )
            )

    # ========================================================
    # DASHBOARD BUTTON FRAME
    # ========================================================

    dashboard_button_frame = tk.Frame(
        dashboard,
        bg=BG_COLOR
    )

    dashboard_button_frame.pack(
        fill="x",
        pady=7
    )

    # ========================================================
    # REFRESH BUTTON
    # ========================================================

    tk.Button(
        dashboard_button_frame,
        text="🔄 Refresh",
        width=14,
        height=2,
        bg=GREEN,
        fg="white",
        activebackground=GREEN,
        activeforeground="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
        command=load_dashboard
    ).pack(
        side="left",
        padx=10
    )

    # ========================================================
    # CLOSE BUTTON
    # ========================================================

    tk.Button(
        dashboard_button_frame,
        text="✖ Close",
        width=14,
        height=2,
        bg=RED,
        fg="white",
        activebackground=RED,
        activeforeground="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
        command=dashboard.destroy
    ).pack(
        side="right",
        padx=10
    )

    # Load data immediately
    load_dashboard()


# ============================================================
# ANALYTICS
# ============================================================

def open_analytics():

    try:

        analytics_file = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)
            ),
            "analytics.py"
        )

        if not os.path.exists(
            analytics_file
        ):

            messagebox.showerror(
                "Analytics Error",
                "analytics.py was not found."
            )

            return

        subprocess.Popen(
            [
                sys.executable,
                analytics_file
            ],
            cwd=os.path.dirname(
                os.path.abspath(__file__)
            )
        )

    except Exception as e:

        messagebox.showerror(
            "Analytics Error",
            f"Unable to open Analytics.\n\n{e}"
        )


# ============================================================
# MANAGEMENT CARD
# ============================================================

management_card = tk.Frame(
    right_frame,
    bg=CARD_COLOR,
    highlightbackground="#D6DEE8",
    highlightthickness=1
)

management_card.pack(
    fill="x",
    pady=(7, 5)
)


# ============================================================
# MANAGEMENT HEADER
# ============================================================

tk.Label(
    management_card,
    text="⚙ MANAGEMENT",
    font=("Arial", 12, "bold"),
    bg=ORANGE,
    fg="white",
    height=2
).pack(
    fill="x"
)


# ============================================================
# STUDENT MANAGEMENT
# ============================================================

def open_students():

    try:

        open_student_management()

    except TypeError:

        try:

            open_student_management(
                root
            )

        except Exception as e:

            messagebox.showerror(
                "Student Management Error",
                str(e)
            )

    except Exception as e:

        messagebox.showerror(
            "Student Management Error",
            str(e)
        )


tk.Button(
    management_card,
    text="👨‍🎓 Student Management",
    height=2,
    bg=BLUE,
    fg="white",
    activebackground=BLUE,
    activeforeground="white",
    font=("Arial", 9, "bold"),
    relief="flat",
    cursor="hand2",
    command=open_students
).pack(
    fill="x",
    padx=10,
    pady=(7, 3)
)


# ============================================================
# ATTENDANCE DASHBOARD BUTTON
# ============================================================

tk.Button(
    management_card,
    text="📊 Attendance Dashboard",
    height=2,
    bg=GREEN,
    fg="white",
    activebackground=GREEN,
    activeforeground="white",
    font=("Arial", 9, "bold"),
    relief="flat",
    cursor="hand2",
    command=open_attendance_dashboard
).pack(
    fill="x",
    padx=10,
    pady=3
)


# ============================================================
# ANALYTICS BUTTON
# ============================================================

tk.Button(
    management_card,
    text="📈 Attendance Analytics",
    height=2,
    bg=PURPLE,
    fg="white",
    activebackground=PURPLE,
    activeforeground="white",
    font=("Arial", 9, "bold"),
    relief="flat",
    cursor="hand2",
    command=open_analytics
).pack(
    fill="x",
    padx=10,
    pady=3
)


# ============================================================
# OPEN ATTENDANCE FOLDER
# ============================================================

def open_attendance_folder():

    attendance_folder = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
        ),
        "attendance"
    )

    os.makedirs(
        attendance_folder,
        exist_ok=True
    )

    try:

        if sys.platform == "win32":

            os.startfile(
                attendance_folder
            )

        elif sys.platform == "darwin":

            subprocess.Popen(
                [
                    "open",
                    attendance_folder
                ]
            )

        else:

            subprocess.Popen(
                [
                    "xdg-open",
                    attendance_folder
                ]
            )

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"Unable to open attendance folder.\n\n{e}"
        )


tk.Button(
    management_card,
    text="📂 Open Attendance Folder",
    height=2,
    bg=GRAY,
    fg="white",
    activebackground=GRAY,
    activeforeground="white",
    font=("Arial", 9, "bold"),
    relief="flat",
    cursor="hand2",
    command=open_attendance_folder
).pack(
    fill="x",
    padx=10,
    pady=3
)


# ============================================================
# EXIT APPLICATION
# ============================================================

def exit_application():

    result = messagebox.askyesno(
        "Exit Application",
        "Are you sure you want to exit the AI Face Attendance System?"
    )

    if not result:
        return

    try:
        camera.stop_camera()
    except Exception:
        pass

    root.destroy()


exit_button = tk.Button(
    management_card,
    text="✖  EXIT APPLICATION",
    height=2,
    bg=RED,
    fg="white",
    activebackground="#B71C1C",
    activeforeground="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    cursor="hand2",
    command=exit_application
)

exit_button.pack(
    fill="x",
    padx=10,
    pady=(3, 9)
)


# ============================================================
# SYSTEM INFORMATION CARD
# ============================================================

info_card = tk.Frame(
    right_frame,
    bg=CARD_COLOR,
    highlightbackground="#D6DEE8",
    highlightthickness=1
)

info_card.pack(
    fill="x",
    pady=5
)


tk.Label(
    info_card,
    text="💡 SYSTEM",
    font=("Arial", 11, "bold"),
    bg=HEADER_COLOR,
    fg="white",
    height=2
).pack(
    fill="x"
)


tk.Label(
    info_card,
    text=(
        "Start the camera to recognize students.\n"
        "Attendance is automatically saved."
    ),
    font=("Arial", 9),
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT,
    justify="left"
).pack(
    padx=12,
    pady=8
)


# ============================================================
# INITIAL STUDENT INFORMATION
# ============================================================

try:

    camera.reset_student_information()

except Exception as e:

    print(
        "Unable to reset student information:",
        e
    )


# ============================================================
# INITIAL CAMERA STATUS
# ============================================================

try:

    camera.status_label.config(
        text="Status : Waiting...",
        fg=ORANGE
    )

except Exception:

    pass


# ============================================================
# INITIAL SCROLL REGION
# ============================================================

root.update_idletasks()

right_canvas.configure(
    scrollregion=right_canvas.bbox("all")
)


# ============================================================
# START APPLICATION
# ============================================================

print("=" * 50)
print("        AI FACE ATTENDANCE SYSTEM")
print("=" * 50)

print("Dashboard starting...")


try:

    print(
        "Registered faces:",
        len(camera.known_names)
    )

except Exception:

    print(
        "Registered faces: Unable to determine"
    )


print("=" * 50)


# ============================================================
# MAIN LOOP
# ============================================================

root.mainloop()