import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
RED = "#E53935"
ORANGE = "#FB8C00"


# ============================================================
# FILE PATH
# ============================================================

BASE_FOLDER = os.path.dirname(
    os.path.abspath(__file__)
)

ATTENDANCE_FILE = os.path.join(
    BASE_FOLDER,
    "attendance",
    "attendance.xlsx"
)


# ============================================================
# LOAD ATTENDANCE DATA
# ============================================================

def load_attendance():

    if not os.path.exists(ATTENDANCE_FILE):

        messagebox.showerror(
            "Attendance File",
            "attendance.xlsx was not found."
        )

        return None

    try:

        df = pd.read_excel(
            ATTENDANCE_FILE
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"Unable to read attendance file.\n\n{e}"
        )

        return None

    required_columns = [
        "Name",
        "Date",
        "Time"
    ]

    for column in required_columns:

        if column not in df.columns:

            messagebox.showerror(
                "Invalid File",
                "Attendance file must contain:\n"
                "Name, Date and Time columns."
            )

            return None

    return df


# ============================================================
# DATE CONVERSION
# ============================================================

def convert_dates(df):

    df = df.copy()

    df["Date_Converted"] = pd.to_datetime(
        df["Date"],
        format="mixed",
        dayfirst=True,
        errors="coerce"
    )

    return df


# ============================================================
# ANALYTICS WINDOW
# ============================================================

def open_analytics():

    df = load_attendance()

    if df is None:
        return

    df = convert_dates(df)

    # ========================================================
    # WINDOW
    # ========================================================

    analytics_window = tk.Toplevel()

    analytics_window.title(
        "Attendance Analytics"
    )

    analytics_window.geometry(
        "1150x760"
    )

    analytics_window.resizable(
        False,
        False
    )

    analytics_window.configure(
        bg=BG_COLOR
    )

    # ========================================================
    # HEADER
    # ========================================================

    header = tk.Frame(
        analytics_window,
        bg=HEADER_COLOR,
        height=75
    )

    header.pack(
        fill="x"
    )

    header.pack_propagate(
        False
    )

    tk.Label(
        header,
        text="📊  ATTENDANCE ANALYTICS",
        font=("Arial", 22, "bold"),
        bg=HEADER_COLOR,
        fg="white"
    ).pack(
        pady=20
    )

    # ========================================================
    # STATISTICS FRAME
    # ========================================================

    statistics_frame = tk.Frame(
        analytics_window,
        bg=BG_COLOR
    )

    statistics_frame.pack(
        fill="x",
        padx=20,
        pady=12
    )

    for i in range(4):

        statistics_frame.grid_columnconfigure(
            i,
            weight=1
        )

    # ========================================================
    # STAT CARD FUNCTION
    # ========================================================

    def create_card(
        title,
        value,
        icon,
        color,
        column
    ):

        card = tk.Frame(
            statistics_frame,
            bg=CARD_COLOR,
            highlightbackground="#D6DEE8",
            highlightthickness=1,
            height=80
        )

        card.grid(
            row=0,
            column=column,
            padx=6,
            sticky="ew"
        )

        card.grid_propagate(
            False
        )

        tk.Label(
            card,
            text=icon,
            font=("Arial", 21),
            bg=CARD_COLOR,
            fg=color
        ).pack(
            side="left",
            padx=(12, 7)
        )

        text_frame = tk.Frame(
            card,
            bg=CARD_COLOR
        )

        text_frame.pack(
            side="left",
            pady=10
        )

        tk.Label(
            text_frame,
            text=title,
            font=("Arial", 8, "bold"),
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT
        ).pack(
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

    # ========================================================
    # STATISTICS
    # ========================================================

    total_records = len(df)

    total_students = (
        df["Name"]
        .dropna()
        .astype(str)
        .str.strip()
        .nunique()
    )

    unique_dates = (
        df["Date_Converted"]
        .dropna()
        .dt.date
        .nunique()
    )

    today = pd.Timestamp.today().date()

    present_today = (
        df[
            df["Date_Converted"]
            .dt.date == today
        ]["Name"]
        .dropna()
        .astype(str)
        .str.strip()
        .nunique()
    )

    create_card(
        "TOTAL RECORDS",
        str(total_records),
        "📋",
        BLUE,
        0
    )

    create_card(
        "STUDENTS",
        str(total_students),
        "👥",
        PURPLE,
        1
    )

    create_card(
        "ATTENDANCE DAYS",
        str(unique_dates),
        "📅",
        GREEN,
        2
    )

    create_card(
        "PRESENT TODAY",
        str(present_today),
        "✅",
        ORANGE,
        3
    )

    # ========================================================
    # FILTER FRAME
    # ========================================================

    filter_frame = tk.Frame(
        analytics_window,
        bg=BG_COLOR
    )

    filter_frame.pack(
        fill="x",
        padx=25,
        pady=5
    )

    tk.Label(
        filter_frame,
        text="🔍 Student:",
        font=("Arial", 11, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(
        side="left",
        padx=5
    )

    search_entry = tk.Entry(
        filter_frame,
        width=24,
        font=("Arial", 11),
        relief="solid",
        bd=1
    )

    search_entry.pack(
        side="left",
        padx=5
    )

    # ========================================================
    # TABLE FRAME
    # ========================================================

    table_frame = tk.Frame(
        analytics_window,
        bg=CARD_COLOR,
        highlightbackground="#D6DEE8",
        highlightthickness=1
    )

    table_frame.pack(
        fill="x",
        padx=25,
        pady=8
    )

    columns = [
        "Name",
        "Attendance Days",
        "Total Records",
        "Attendance %"
    ]

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=7
    )

    # ========================================================
    # TREEVIEW STYLE
    # ========================================================

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

    # ========================================================
    # TABLE HEADINGS
    # ========================================================

    tree.heading(
        "Name",
        text="Student Name"
    )

    tree.heading(
        "Attendance Days",
        text="Attendance Days"
    )

    tree.heading(
        "Total Records",
        text="Total Records"
    )

    tree.heading(
        "Attendance %",
        text="Attendance %"
    )

    tree.column(
        "Name",
        width=280,
        anchor="center"
    )

    tree.column(
        "Attendance Days",
        width=200,
        anchor="center"
    )

    tree.column(
        "Total Records",
        width=200,
        anchor="center"
    )

    tree.column(
        "Attendance %",
        width=200,
        anchor="center"
    )

    tree.pack(
        side="left",
        fill="both",
        expand=True
    )

    # ========================================================
    # TABLE SCROLLBAR
    # ========================================================

    table_scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )

    tree.configure(
        yscrollcommand=table_scrollbar.set
    )

    table_scrollbar.pack(
        side="right",
        fill="y"
    )

    # ========================================================
    # CHART FRAME
    # ========================================================

    chart_frame = tk.Frame(
        analytics_window,
        bg=CARD_COLOR,
        highlightbackground="#D6DEE8",
        highlightthickness=1
    )

    chart_frame.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=8
    )

    # ========================================================
    # FILTER DATA
    # ========================================================

    def get_filtered_data():

        search_text = (
            search_entry
            .get()
            .strip()
            .lower()
        )

        if search_text == "":
            return df.copy()

        filtered_df = df[
            df["Name"]
            .astype(str)
            .str.lower()
            .str.contains(
                search_text,
                na=False
            )
        ]

        return filtered_df

    # ========================================================
    # UPDATE TABLE
    # ========================================================

    def update_table():

        filtered_df = get_filtered_data()

        for item in tree.get_children():

            tree.delete(item)

        if filtered_df.empty:

            return

        all_days = (
            df["Date_Converted"]
            .dropna()
            .dt.date
            .nunique()
        )

        grouped = (
            filtered_df
            .groupby("Name")
        )

        for name, student_data in grouped:

            name = str(
                name
            ).strip()

            attendance_days = (
                student_data["Date_Converted"]
                .dropna()
                .dt.date
                .nunique()
            )

            total_student_records = len(
                student_data
            )

            if all_days > 0:

                percentage = (
                    attendance_days /
                    all_days
                ) * 100

            else:

                percentage = 0

            tree.insert(
                "",
                "end",
                values=(
                    name,
                    attendance_days,
                    total_student_records,
                    f"{percentage:.1f}%"
                )
            )

    # ========================================================
    # CLEAR CHART
    # ========================================================

    def clear_chart():

        for widget in chart_frame.winfo_children():

            widget.destroy()

    # ========================================================
    # SHOW STUDENT CHART
    # ========================================================

    def show_student_chart():

        clear_chart()

        chart_data = (
            get_filtered_data()
            .groupby("Name")
            .size()
            .sort_values(
                ascending=False
            )
        )

        if chart_data.empty:

            tk.Label(
                chart_frame,
                text="No attendance data available.",
                font=("Arial", 14, "bold"),
                bg=CARD_COLOR,
                fg=SECONDARY_TEXT
            ).pack(
                expand=True
            )

            return

        chart_data = chart_data.head(10)

        figure = plt.Figure(
            figsize=(9, 3.1),
            dpi=100
        )

        ax = figure.add_subplot(111)

        ax.bar(
            chart_data.index.astype(str),
            chart_data.values
        )

        ax.set_title(
            "Attendance by Student",
            fontsize=14,
            fontweight="bold"
        )

        ax.set_xlabel(
            "Student"
        )

        ax.set_ylabel(
            "Attendance Records"
        )

        ax.tick_params(
            axis="x",
            rotation=30
        )

        ax.grid(
            axis="y",
            alpha=0.25
        )

        figure.tight_layout()

        canvas = FigureCanvasTkAgg(
            figure,
            master=chart_frame
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    # ========================================================
    # SHOW DAILY CHART
    # ========================================================

    def show_daily_chart():

        clear_chart()

        daily_data = (
            df.dropna(
                subset=["Date_Converted"]
            )
            .groupby(
                df["Date_Converted"].dt.date
            )
            .size()
            .sort_index()
        )

        if daily_data.empty:

            tk.Label(
                chart_frame,
                text="No date information available.",
                font=("Arial", 14, "bold"),
                bg=CARD_COLOR,
                fg=SECONDARY_TEXT
            ).pack(
                expand=True
            )

            return

        daily_data = daily_data.tail(15)

        figure = plt.Figure(
            figsize=(9, 3.1),
            dpi=100
        )

        ax = figure.add_subplot(111)

        ax.plot(
            [
                str(date)
                for date in daily_data.index
            ],
            daily_data.values,
            marker="o"
        )

        ax.set_title(
            "Daily Attendance",
            fontsize=14,
            fontweight="bold"
        )

        ax.set_xlabel(
            "Date"
        )

        ax.set_ylabel(
            "Attendance"
        )

        ax.tick_params(
            axis="x",
            rotation=35
        )

        ax.grid(
            alpha=0.25
        )

        figure.tight_layout()

        canvas = FigureCanvasTkAgg(
            figure,
            master=chart_frame
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    # ========================================================
    # SHOW ATTENDANCE PERCENTAGE CHART
    # ========================================================

    def show_percentage_chart():

        clear_chart()

        all_days = (
            df["Date_Converted"]
            .dropna()
            .dt.date
            .nunique()
        )

        if all_days == 0:

            tk.Label(
                chart_frame,
                text="No attendance dates available.",
                font=("Arial", 14, "bold"),
                bg=CARD_COLOR,
                fg=SECONDARY_TEXT
            ).pack(
                expand=True
            )

            return

        percentage_data = (
            df.groupby("Name")[
                "Date_Converted"
            ]
            .apply(
                lambda x:
                x.dropna()
                .dt.date
                .nunique()
                / all_days * 100
            )
            .sort_values(
                ascending=False
            )
            .head(10)
        )

        if percentage_data.empty:

            tk.Label(
                chart_frame,
                text="No student data available.",
                font=("Arial", 14, "bold"),
                bg=CARD_COLOR,
                fg=SECONDARY_TEXT
            ).pack(
                expand=True
            )

            return

        figure = plt.Figure(
            figsize=(9, 3.1),
            dpi=100
        )

        ax = figure.add_subplot(111)

        ax.barh(
            percentage_data.index.astype(str),
            percentage_data.values
        )

        ax.set_title(
            "Student Attendance Percentage",
            fontsize=14,
            fontweight="bold"
        )

        ax.set_xlabel(
            "Attendance Percentage (%)"
        )

        ax.set_xlim(
            0,
            100
        )

        ax.grid(
            axis="x",
            alpha=0.25
        )

        figure.tight_layout()

        canvas = FigureCanvasTkAgg(
            figure,
            master=chart_frame
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    # ========================================================
    # SEARCH BUTTON
    # ========================================================

    tk.Button(
        filter_frame,
        text="🔍 Search",
        width=11,
        bg=BLUE,
        fg="white",
        activebackground=BLUE,
        activeforeground="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
        command=update_table
    ).pack(
        side="left",
        padx=4
    )

    # ========================================================
    # SHOW ALL BUTTON
    # ========================================================

    def show_all():

        search_entry.delete(
            0,
            tk.END
        )

        update_table()

        show_student_chart()

    tk.Button(
        filter_frame,
        text="Show All",
        width=11,
        bg=GREEN,
        fg="white",
        activebackground=GREEN,
        activeforeground="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
        command=show_all
    ).pack(
        side="left",
        padx=4
    )

    # ========================================================
    # STUDENT CHART BUTTON
    # ========================================================

    tk.Button(
        filter_frame,
        text="📊 Student Chart",
        width=15,
        bg=PURPLE,
        fg="white",
        activebackground=PURPLE,
        activeforeground="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
        command=show_student_chart
    ).pack(
        side="left",
        padx=4
    )

    # ========================================================
    # DAILY CHART BUTTON
    # ========================================================

    tk.Button(
        filter_frame,
        text="📈 Daily Chart",
        width=13,
        bg=ORANGE,
        fg="white",
        activebackground=ORANGE,
        activeforeground="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
        command=show_daily_chart
    ).pack(
        side="left",
        padx=4
    )

    # ========================================================
    # PERCENTAGE BUTTON
    # ========================================================

    tk.Button(
        filter_frame,
        text="🏆 Percentage",
        width=13,
        bg=BLUE,
        fg="white",
        activebackground=BLUE,
        activeforeground="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
        command=show_percentage_chart
    ).pack(
        side="left",
        padx=4
    )

    # ========================================================
    # REFRESH BUTTON
    # ========================================================

    def refresh_analytics():

        nonlocal df

        new_df = load_attendance()

        if new_df is None:
            return

        df = convert_dates(
            new_df
        )

        update_table()
        show_student_chart()

    tk.Button(
        filter_frame,
        text="🔄 Refresh",
        width=11,
        bg=GREEN,
        fg="white",
        activebackground=GREEN,
        activeforeground="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
        command=refresh_analytics
    ).pack(
        side="left",
        padx=4
    )

    # ========================================================
    # CLOSE BUTTON
    # ========================================================

    tk.Button(
        analytics_window,
        text="✖  Close",
        width=15,
        height=2,
        bg=RED,
        fg="white",
        activebackground=RED,
        activeforeground="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
        command=analytics_window.destroy
    ).pack(
        pady=10
    )

    # ========================================================
    # LOAD TABLE
    # ========================================================

    update_table()

    # ========================================================
    # SHOW STUDENT CHART AUTOMATICALLY
    # ========================================================

    show_student_chart()


# ============================================================
# TEST ANALYTICS DIRECTLY
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()

    open_analytics()

    root.mainloop()