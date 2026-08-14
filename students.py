import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import json
import shutil
import subprocess
import sys


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


# ============================================================
# FILE PATHS
# ============================================================

BASE_FOLDER = os.path.dirname(
    os.path.abspath(__file__)
)

STUDENT_FILE = os.path.join(
    BASE_FOLDER,
    "students.json"
)

IMAGES_FOLDER = os.path.join(
    BASE_FOLDER,
    "images"
)

ENCODE_FILE = os.path.join(
    BASE_FOLDER,
    "encode_face.py"
)


# ============================================================
# CREATE IMAGES FOLDER
# ============================================================

os.makedirs(
    IMAGES_FOLDER,
    exist_ok=True
)


# ============================================================
# PHOTO VARIABLE
# ============================================================

selected_photo = None


# ============================================================
# LOAD STUDENTS
# ============================================================

def load_students():

    if not os.path.exists(STUDENT_FILE):

        return []

    try:

        with open(
            STUDENT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, list):

            return data

        return []

    except json.JSONDecodeError as e:

        print(
            "students.json contains invalid JSON:",
            e
        )

        return []

    except Exception as e:

        print(
            "Unable to load students:",
            e
        )

        return []


# ============================================================
# SAVE STUDENTS
# ============================================================

def save_students(students):

    try:

        with open(
            STUDENT_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                students,
                file,
                indent=4,
                ensure_ascii=False
            )

        return True

    except Exception as e:

        messagebox.showerror(
            "Save Error",
            f"Unable to save student data.\n\n{e}"
        )

        return False


# ============================================================
# UPDATE FACE ENCODINGS
# ============================================================

def update_face_encodings():

    if not os.path.exists(ENCODE_FILE):

        print(
            "encode_face.py not found."
        )

        return False

    try:

        print(
            "Updating face encodings..."
        )

        result = subprocess.run(
            [
                sys.executable,
                ENCODE_FILE
            ],
            cwd=BASE_FOLDER,
            capture_output=True,
            text=True
        )

        if result.stdout:

            print(
                result.stdout
            )

        if result.stderr:

            print(
                result.stderr
            )

        if result.returncode == 0:

            print(
                "Face encodings updated successfully."
            )

            return True

        print(
            "Face encoding failed."
        )

        return False

    except Exception as e:

        print(
            "Face encoding error:",
            e
        )

        return False


# ============================================================
# CREATE SAFE PHOTO NAME
# ============================================================

def create_safe_filename(name):

    safe_name = "".join(
        character
        for character in name
        if character.isalnum()
        or character in (
            "_",
            "-"
        )
    )

    if not safe_name:

        safe_name = "student"

    return safe_name


# ============================================================
# ADD STUDENT
# ============================================================

def add_student(
    name,
    roll_no,
    department,
    photo_path=None
):

    name = str(name).strip()
    roll_no = str(roll_no).strip()
    department = str(department).strip()

    # --------------------------------------------------------
    # CHECK EMPTY FIELDS
    # --------------------------------------------------------

    if not name:

        messagebox.showwarning(
            "Missing Information",
            "Please enter student name."
        )

        return False

    if not roll_no:

        messagebox.showwarning(
            "Missing Information",
            "Please enter roll number."
        )

        return False

    if not department:

        messagebox.showwarning(
            "Missing Information",
            "Please enter department."
        )

        return False

    # --------------------------------------------------------
    # CHECK PHOTO
    # --------------------------------------------------------

    if not photo_path:

        messagebox.showwarning(
            "Photo Required",
            "Please select a student photo."
        )

        return False

    if not os.path.exists(photo_path):

        messagebox.showerror(
            "Photo Error",
            "Selected photo does not exist."
        )

        return False

    # --------------------------------------------------------
    # LOAD STUDENTS
    # --------------------------------------------------------

    students = load_students()

    # --------------------------------------------------------
    # CHECK DUPLICATE ROLL NUMBER
    # --------------------------------------------------------

    for student in students:

        existing_roll = str(
            student.get(
                "roll_no",
                ""
            )
        ).strip()

        if existing_roll.lower() == roll_no.lower():

            messagebox.showwarning(
                "Duplicate Student",
                "This Roll Number already exists."
            )

            return False

    # --------------------------------------------------------
    # CHECK DUPLICATE NAME
    # --------------------------------------------------------

    for student in students:

        existing_name = str(
            student.get(
                "name",
                ""
            )
        ).strip()

        if existing_name.lower() == name.lower():

            messagebox.showwarning(
                "Duplicate Student",
                "This student name already exists."
            )

            return False

    # --------------------------------------------------------
    # CHECK PHOTO EXTENSION
    # --------------------------------------------------------

    original_extension = os.path.splitext(
        photo_path
    )[1].lower()

    allowed_extensions = [
        ".jpg",
        ".jpeg",
        ".png"
    ]

    if original_extension not in allowed_extensions:

        messagebox.showwarning(
            "Invalid Photo",
            "Please select JPG, JPEG or PNG image."
        )

        return False

    # ========================================================
    # COPY PHOTO
    # ========================================================

    try:

        safe_name = create_safe_filename(
            name
        )

        destination_filename = (
            safe_name
            + original_extension
        )

        destination_path = os.path.join(
            IMAGES_FOLDER,
            destination_filename
        )

        counter = 1

        while os.path.exists(destination_path):

            destination_filename = (
                safe_name
                + "_"
                + str(counter)
                + original_extension
            )

            destination_path = os.path.join(
                IMAGES_FOLDER,
                destination_filename
            )

            counter += 1

        shutil.copy2(
            photo_path,
            destination_path
        )

        print(
            "Photo saved:",
            destination_path
        )

    except Exception as e:

        messagebox.showerror(
            "Photo Error",
            f"Unable to copy student photo.\n\n{e}"
        )

        return False

    # ========================================================
    # CREATE STUDENT RECORD
    # ========================================================

    new_student = {
        "name": name,
        "roll_no": roll_no,
        "department": department,
        "photo": destination_filename
    }

    students.append(
        new_student
    )

    # ========================================================
    # SAVE STUDENT
    # ========================================================

    if not save_students(students):

        # Remove copied photo if saving failed

        try:

            if os.path.exists(
                destination_path
            ):

                os.remove(
                    destination_path
                )

        except Exception:

            pass

        return False

    # ========================================================
    # UPDATE FACE ENCODINGS
    # ========================================================

    encode_success = update_face_encodings()

    # ========================================================
    # SUCCESS MESSAGE
    # ========================================================

    if encode_success:

        messagebox.showinfo(
            "Student Added Successfully",
            f"{name} added successfully!\n\n"
            f"Roll No: {roll_no}\n"
            f"Department: {department}\n\n"
            f"✓ Photo saved successfully.\n"
            f"✓ Face encoding updated successfully.\n\n"
            f"{name} is now ready for attendance."
        )

    else:

        messagebox.showwarning(
            "Student Added",
            f"{name} was added successfully.\n\n"
            f"✓ Photo saved successfully.\n"
            f"⚠ Face encoding could not be updated.\n\n"
            f"Please run encode_face.py manually."
        )

    return True


# ============================================================
# DELETE STUDENT
# ============================================================

def delete_student(roll_no):

    roll_no = str(
        roll_no
    ).strip()

    students = load_students()

    student_to_delete = None

    # --------------------------------------------------------
    # FIND STUDENT
    # --------------------------------------------------------

    for student in students:

        existing_roll = str(
            student.get(
                "roll_no",
                ""
            )
        ).strip()

        if existing_roll == roll_no:

            student_to_delete = student

            break

    if student_to_delete is None:

        return False

    # --------------------------------------------------------
    # REMOVE STUDENT FROM JSON
    # --------------------------------------------------------

    updated_students = []

    for student in students:

        existing_roll = str(
            student.get(
                "roll_no",
                ""
            )
        ).strip()

        if existing_roll != roll_no:

            updated_students.append(
                student
            )

    # --------------------------------------------------------
    # SAVE UPDATED STUDENTS
    # --------------------------------------------------------

    if not save_students(
        updated_students
    ):

        return False

    # --------------------------------------------------------
    # REMOVE PHOTO
    # --------------------------------------------------------

    photo_name = str(
        student_to_delete.get(
            "photo",
            ""
        )
    ).strip()

    if photo_name:

        photo_path = os.path.join(
            IMAGES_FOLDER,
            photo_name
        )

        if os.path.exists(photo_path):

            try:

                os.remove(
                    photo_path
                )

                print(
                    "Photo deleted:",
                    photo_path
                )

            except Exception as e:

                print(
                    "Unable to delete photo:",
                    e
                )

    # --------------------------------------------------------
    # UPDATE ENCODINGS
    # --------------------------------------------------------

    encode_success = update_face_encodings()

    if not encode_success:

        print(
            "Warning: Face encodings were not updated."
        )

    return True


# ============================================================
# GET TOTAL STUDENTS
# ============================================================

def get_total_students():

    students = load_students()

    return len(students)


# ============================================================
# GET STUDENT DETAILS
# ============================================================

def get_student_details(name):

    requested_name = str(
        name
    ).strip().lower()

    students = load_students()

    for student in students:

        existing_name = str(
            student.get(
                "name",
                ""
            )
        ).strip().lower()

        if existing_name == requested_name:

            return student

    return None


# ============================================================
# STUDENT MANAGEMENT WINDOW
# ============================================================

def open_student_management():

    global selected_photo

    selected_photo = None

    students_window = tk.Toplevel()

    students_window.title(
        "Student Management"
    )

    students_window.geometry(
        "1100x750"
    )

    students_window.resizable(
        False,
        False
    )

    students_window.configure(
        bg=BG_COLOR
    )

    # ========================================================
    # HEADER
    # ========================================================

    header = tk.Frame(
        students_window,
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
        text="👨‍🎓  STUDENT MANAGEMENT SYSTEM",
        font=(
            "Arial",
            22,
            "bold"
        ),
        bg=HEADER_COLOR,
        fg="white"
    ).pack(
        pady=20
    )

    # ========================================================
    # ADD STUDENT CARD
    # ========================================================

    form_card = tk.Frame(
        students_window,
        bg=CARD_COLOR,
        highlightbackground="#D6DEE8",
        highlightthickness=1
    )

    form_card.pack(
        fill="x",
        padx=25,
        pady=15
    )

    tk.Label(
        form_card,
        text="ADD NEW STUDENT",
        font=(
            "Arial",
            14,
            "bold"
        ),
        bg=CARD_COLOR,
        fg=HEADER_COLOR
    ).grid(
        row=0,
        column=0,
        columnspan=7,
        pady=(
            12,
            10
        )
    )

    # ========================================================
    # NAME
    # ========================================================

    tk.Label(
        form_card,
        text="Name",
        font=(
            "Arial",
            10,
            "bold"
        ),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).grid(
        row=1,
        column=0,
        padx=8,
        pady=5
    )

    name_entry = tk.Entry(
        form_card,
        width=18,
        font=(
            "Arial",
            10
        )
    )

    name_entry.grid(
        row=1,
        column=1,
        padx=8,
        pady=5
    )

    # ========================================================
    # ROLL NUMBER
    # ========================================================

    tk.Label(
        form_card,
        text="Roll No",
        font=(
            "Arial",
            10,
            "bold"
        ),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).grid(
        row=1,
        column=2,
        padx=8,
        pady=5
    )

    roll_entry = tk.Entry(
        form_card,
        width=16,
        font=(
            "Arial",
            10
        )
    )

    roll_entry.grid(
        row=1,
        column=3,
        padx=8,
        pady=5
    )

    # ========================================================
    # DEPARTMENT
    # ========================================================

    tk.Label(
        form_card,
        text="Department",
        font=(
            "Arial",
            10,
            "bold"
        ),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).grid(
        row=1,
        column=4,
        padx=8,
        pady=5
    )

    department_entry = tk.Entry(
        form_card,
        width=16,
        font=(
            "Arial",
            10
        )
    )

    department_entry.grid(
        row=1,
        column=5,
        padx=8,
        pady=5
    )

    # ========================================================
    # PHOTO LABEL
    # ========================================================

    photo_label = tk.Label(
        form_card,
        text="No photo selected",
        font=(
            "Arial",
            9
        ),
        bg=CARD_COLOR,
        fg=SECONDARY_TEXT,
        width=22
    )

    photo_label.grid(
        row=2,
        column=0,
        columnspan=4,
        padx=8,
        pady=8
    )

    # ========================================================
    # SELECT PHOTO
    # ========================================================

    def select_photo():

        global selected_photo

        file_path = filedialog.askopenfilename(

            parent=students_window,

            title="Select Student Photo",

            filetypes=[
                (
                    "Image Files",
                    "*.jpg *.jpeg *.png"
                ),
                (
                    "JPG Files",
                    "*.jpg"
                ),
                (
                    "JPEG Files",
                    "*.jpeg"
                ),
                (
                    "PNG Files",
                    "*.png"
                )
            ]
        )

        if not file_path:

            return

        selected_photo = file_path

        photo_label.config(
            text=os.path.basename(
                file_path
            ),
            fg=GREEN
        )

        print(
            "Selected photo:",
            selected_photo
        )

    tk.Button(
        form_card,
        text="📷 Select Photo",
        bg=PURPLE,
        fg="white",
        activebackground=PURPLE,
        activeforeground="white",
        font=(
            "Arial",
            10,
            "bold"
        ),
        relief="flat",
        cursor="hand2",
        command=select_photo
    ).grid(
        row=2,
        column=4,
        columnspan=2,
        padx=8,
        pady=8
    )

    # ========================================================
    # TABLE CARD
    # ========================================================

    table_card = tk.Frame(
        students_window,
        bg=CARD_COLOR,
        highlightbackground="#D6DEE8",
        highlightthickness=1
    )

    table_card.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=5
    )

    tk.Label(
        table_card,
        text="STUDENT LIST",
        font=(
            "Arial",
            14,
            "bold"
        ),
        bg=CARD_COLOR,
        fg=HEADER_COLOR
    ).pack(
        anchor="w",
        padx=15,
        pady=10
    )

    # ========================================================
    # SEARCH FRAME
    # ========================================================

    search_frame = tk.Frame(
        table_card,
        bg=CARD_COLOR
    )

    search_frame.pack(
        fill="x",
        padx=15,
        pady=5
    )

    tk.Label(
        search_frame,
        text="🔍 Search:",
        font=(
            "Arial",
            10,
            "bold"
        ),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).pack(
        side="left"
    )

    search_entry = tk.Entry(
        search_frame,
        width=30,
        font=(
            "Arial",
            10
        )
    )

    search_entry.pack(
        side="left",
        padx=8
    )

    # ========================================================
    # TABLE FRAME
    # ========================================================

    table_frame = tk.Frame(
        table_card,
        bg="white"
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=8
    )

    # ========================================================
    # TABLE
    # ========================================================

    columns = (
        "name",
        "roll_no",
        "department"
    )

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    tree.heading(
        "name",
        text="Student Name"
    )

    tree.heading(
        "roll_no",
        text="Roll Number"
    )

    tree.heading(
        "department",
        text="Department"
    )

    tree.column(
        "name",
        width=300,
        anchor="center"
    )

    tree.column(
        "roll_no",
        width=250,
        anchor="center"
    )

    tree.column(
        "department",
        width=300,
        anchor="center"
    )

    # ========================================================
    # TREEVIEW STYLE
    # ========================================================

    style = ttk.Style()

    try:

        style.theme_use(
            "clam"
        )

    except Exception:

        pass

    style.configure(
        "Treeview",
        font=(
            "Arial",
            10
        ),
        rowheight=32,
        background="white",
        fieldbackground="white"
    )

    style.configure(
        "Treeview.Heading",
        font=(
            "Arial",
            10,
            "bold"
        )
    )

    # ========================================================
    # SCROLLBAR
    # ========================================================

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

    # ========================================================
    # REFRESH TABLE
    # ========================================================

    def refresh_table():

        for item in tree.get_children():

            tree.delete(item)

        search_text = (
            search_entry
            .get()
            .strip()
            .lower()
        )

        students = load_students()

        for student in students:

            name = str(
                student.get(
                    "name",
                    ""
                )
            ).strip()

            roll_no = str(
                student.get(
                    "roll_no",
                    ""
                )
            ).strip()

            department = str(
                student.get(
                    "department",
                    ""
                )
            ).strip()

            searchable_text = (
                name
                + " "
                + roll_no
                + " "
                + department
            ).lower()

            if (
                search_text
                and
                search_text not in searchable_text
            ):

                continue

            tree.insert(
                "",
                "end",
                values=(
                    name,
                    roll_no,
                    department
                )
            )

    # ========================================================
    # ADD STUDENT FROM FORM
    # ========================================================

    def add_student_from_form():

        global selected_photo

        success = add_student(

            name_entry.get(),

            roll_entry.get(),

            department_entry.get(),

            selected_photo
        )

        if success:

            name_entry.delete(
                0,
                tk.END
            )

            roll_entry.delete(
                0,
                tk.END
            )

            department_entry.delete(
                0,
                tk.END
            )

            selected_photo = None

            photo_label.config(
                text="No photo selected",
                fg=SECONDARY_TEXT
            )

            refresh_table()

            name_entry.focus()

    # ========================================================
    # ADD BUTTON
    # ========================================================

    tk.Button(
        form_card,
        text="➕ Add Student",
        bg=GREEN,
        fg="white",
        activebackground=GREEN,
        activeforeground="white",
        font=(
            "Arial",
            10,
            "bold"
        ),
        relief="flat",
        cursor="hand2",
        command=add_student_from_form
    ).grid(
        row=3,
        column=0,
        columnspan=7,
        pady=(
            8,
            12
        )
    )

    # ========================================================
    # SEARCH BUTTON
    # ========================================================

    tk.Button(
        search_frame,
        text="Search",
        width=10,
        bg=BLUE,
        fg="white",
        activebackground=BLUE,
        activeforeground="white",
        font=(
            "Arial",
            10,
            "bold"
        ),
        relief="flat",
        cursor="hand2",
        command=refresh_table
    ).pack(
        side="left",
        padx=5
    )

    # ========================================================
    # SHOW ALL
    # ========================================================

    def show_all():

        search_entry.delete(
            0,
            tk.END
        )

        refresh_table()

    tk.Button(
        search_frame,
        text="Show All",
        width=10,
        bg=PURPLE,
        fg="white",
        activebackground=PURPLE,
        activeforeground="white",
        font=(
            "Arial",
            10,
            "bold"
        ),
        relief="flat",
        cursor="hand2",
        command=show_all
    ).pack(
        side="left",
        padx=5
    )

    # ========================================================
    # DELETE SELECTED STUDENT
    # ========================================================

    def delete_selected_student():

        selected = tree.selection()

        if not selected:

            messagebox.showwarning(
                "Select Student",
                "Please select a student first.",
                parent=students_window
            )

            return

        item = tree.item(
            selected[0]
        )

        values = item.get(
            "values",
            []
        )

        if len(values) < 2:

            return

        name = str(
            values[0]
        )

        roll_no = str(
            values[1]
        )

        confirm = messagebox.askyesno(
            "Delete Student",
            f"Are you sure you want to delete:\n\n"
            f"Name: {name}\n"
            f"Roll No: {roll_no}\n\n"
            f"The student's photo will also be deleted.",
            parent=students_window
        )

        if not confirm:

            return

        if delete_student(
            roll_no
        ):

            messagebox.showinfo(
                "Deleted",
                f"{name} deleted successfully.",
                parent=students_window
            )

            refresh_table()

        else:

            messagebox.showerror(
                "Error",
                "Unable to delete student.",
                parent=students_window
            )

    # ========================================================
    # DELETE BUTTON
    # ========================================================

    tk.Button(
        search_frame,
        text="🗑 Delete",
        width=10,
        bg=RED,
        fg="white",
        activebackground=RED,
        activeforeground="white",
        font=(
            "Arial",
            10,
            "bold"
        ),
        relief="flat",
        cursor="hand2",
        command=delete_selected_student
    ).pack(
        side="left",
        padx=5
    )

    # ========================================================
    # CLOSE BUTTON
    # ========================================================

    tk.Button(
        students_window,
        text="✖ Close",
        width=15,
        height=2,
        bg=ORANGE,
        fg="white",
        activebackground=ORANGE,
        activeforeground="white",
        font=(
            "Arial",
            10,
            "bold"
        ),
        relief="flat",
        cursor="hand2",
        command=students_window.destroy
    ).pack(
        pady=12
    )

    # ========================================================
    # ENTER KEY SEARCH
    # ========================================================

    search_entry.bind(
        "<Return>",
        lambda event: refresh_table()
    )

    # ========================================================
    # INITIAL TABLE LOAD
    # ========================================================

    refresh_table()

    name_entry.focus()


# ============================================================
# COMMAND-LINE TEST
# ============================================================

if __name__ == "__main__":

    print(
        "========================================"
    )

    print(
        " Student Management System"
    )

    print(
        "========================================"
    )

    print(
        f"Total Students: {get_total_students()}"
    )

    root = tk.Tk()

    root.withdraw()

    open_student_management()

    root.mainloop()