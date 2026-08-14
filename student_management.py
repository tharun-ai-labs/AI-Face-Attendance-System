import tkinter as tk
from tkinter import ttk, messagebox

from students import (
    add_student,
    update_student,
    delete_student,
    get_all_students
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
RED = "#E53935"
ORANGE = "#FB8C00"


# ============================================================
# OPEN STUDENT MANAGEMENT
# ============================================================

def open_student_management():

    window = tk.Toplevel()

    window.title(
        "Student Management"
    )

    window.geometry(
        "1100x700"
    )

    window.resizable(
        False,
        False
    )

    window.configure(
        bg=BG_COLOR
    )


    # ========================================================
    # HEADER
    # ========================================================

    header = tk.Frame(
        window,
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
        text="👨‍🎓  STUDENT MANAGEMENT",
        font=("Arial", 22, "bold"),
        bg=HEADER_COLOR,
        fg="white"
    ).pack(
        pady=20
    )


    # ========================================================
    # MAIN FRAME
    # ========================================================

    main_frame = tk.Frame(
        window,
        bg=BG_COLOR
    )

    main_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=15
    )


    main_frame.grid_columnconfigure(
        0,
        weight=3
    )

    main_frame.grid_columnconfigure(
        1,
        weight=7
    )


    # ========================================================
    # FORM CARD
    # ========================================================

    form_card = tk.Frame(
        main_frame,
        bg=CARD_COLOR,
        highlightbackground="#D6DEE8",
        highlightthickness=1
    )

    form_card.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=(0, 10)
    )


    # ========================================================
    # FORM HEADER
    # ========================================================

    tk.Label(
        form_card,
        text="Student Details",
        font=("Arial", 15, "bold"),
        bg=HEADER_COLOR,
        fg="white",
        anchor="w",
        padx=15,
        pady=12
    ).pack(
        fill="x"
    )


    # ========================================================
    # FORM FRAME
    # ========================================================

    fields_frame = tk.Frame(
        form_card,
        bg=CARD_COLOR
    )

    fields_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )


    # ========================================================
    # VARIABLES
    # ========================================================

    name_var = tk.StringVar()
    roll_var = tk.StringVar()
    department_var = tk.StringVar()
    email_var = tk.StringVar()
    phone_var = tk.StringVar()


    # ========================================================
    # FIELD FUNCTION
    # ========================================================

    def create_field(
        parent,
        label_text,
        variable,
        row
    ):

        tk.Label(
            parent,
            text=label_text,
            font=("Arial", 10, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).grid(
            row=row,
            column=0,
            sticky="w",
            pady=(8, 4)
        )

        entry = tk.Entry(
            parent,
            textvariable=variable,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )

        entry.grid(
            row=row + 1,
            column=0,
            sticky="ew",
            pady=(0, 8)
        )

        return entry


    fields_frame.grid_columnconfigure(
        0,
        weight=1
    )


    # ========================================================
    # CREATE FIELDS
    # ========================================================

    name_entry = create_field(
        fields_frame,
        "Student Name",
        name_var,
        0
    )

    roll_entry = create_field(
        fields_frame,
        "Roll Number",
        roll_var,
        2
    )

    department_entry = create_field(
        fields_frame,
        "Department",
        department_var,
        4
    )

    email_entry = create_field(
        fields_frame,
        "Email",
        email_var,
        6
    )

    phone_entry = create_field(
        fields_frame,
        "Phone",
        phone_var,
        8
    )


    # ========================================================
    # CLEAR FORM
    # ========================================================

    def clear_form():

        name_var.set("")
        roll_var.set("")
        department_var.set("")
        email_var.set("")
        phone_var.set("")

        tree.selection_remove(
            tree.selection()
        )


    # ========================================================
    # ADD STUDENT
    # ========================================================

    def add_student_action():

        name = name_var.get().strip()
        roll = roll_var.get().strip()
        department = department_var.get().strip()
        email = email_var.get().strip()
        phone = phone_var.get().strip()


        if not name:

            messagebox.showwarning(
                "Missing Information",
                "Please enter student name.",
                parent=window
            )

            return


        if not roll:

            messagebox.showwarning(
                "Missing Information",
                "Please enter roll number.",
                parent=window
            )

            return


        success, message = add_student(
            name,
            roll,
            department,
            email,
            phone
        )


        if success:

            messagebox.showinfo(
                "Success",
                message,
                parent=window
            )

            clear_form()

            load_table()

        else:

            messagebox.showerror(
                "Error",
                message,
                parent=window
            )


    # ========================================================
    # UPDATE STUDENT
    # ========================================================

    def update_student_action():

        name = name_var.get().strip()
        roll = roll_var.get().strip()
        department = department_var.get().strip()
        email = email_var.get().strip()
        phone = phone_var.get().strip()


        if not roll:

            messagebox.showwarning(
                "Missing Information",
                "Please select a student first.",
                parent=window
            )

            return


        success, message = update_student(
            roll,
            name,
            department,
            email,
            phone
        )


        if success:

            messagebox.showinfo(
                "Success",
                message,
                parent=window
            )

            clear_form()

            load_table()

        else:

            messagebox.showerror(
                "Error",
                message,
                parent=window
            )


    # ========================================================
    # DELETE STUDENT
    # ========================================================

    def delete_student_action():

        roll = roll_var.get().strip()


        if not roll:

            messagebox.showwarning(
                "Select Student",
                "Please select a student first.",
                parent=window
            )

            return


        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete student with Roll No: {roll}?",
            parent=window
        )


        if not confirm:

            return


        success, message = delete_student(
            roll
        )


        if success:

            messagebox.showinfo(
                "Success",
                message,
                parent=window
            )

            clear_form()

            load_table()

        else:

            messagebox.showerror(
                "Error",
                message,
                parent=window
            )


    # ========================================================
    # BUTTON FRAME
    # ========================================================

    button_frame = tk.Frame(
        fields_frame,
        bg=CARD_COLOR
    )

    button_frame.grid(
        row=10,
        column=0,
        sticky="ew",
        pady=15
    )


    button_frame.grid_columnconfigure(
        0,
        weight=1
    )

    button_frame.grid_columnconfigure(
        1,
        weight=1
    )


    tk.Button(
        button_frame,
        text="➕ Add Student",
        bg=GREEN,
        fg="white",
        activebackground=GREEN,
        activeforeground="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
        command=add_student_action
    ).grid(
        row=0,
        column=0,
        padx=3,
        pady=3,
        sticky="ew"
    )


    tk.Button(
        button_frame,
        text="✏️ Update",
        bg=BLUE,
        fg="white",
        activebackground=BLUE,
        activeforeground="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
        command=update_student_action
    ).grid(
        row=0,
        column=1,
        padx=3,
        pady=3,
        sticky="ew"
    )


    tk.Button(
        button_frame,
        text="🗑️ Delete",
        bg=RED,
        fg="white",
        activebackground=RED,
        activeforeground="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
        command=delete_student_action
    ).grid(
        row=1,
        column=0,
        padx=3,
        pady=3,
        sticky="ew"
    )


    tk.Button(
        button_frame,
        text="🔄 Clear",
        bg=ORANGE,
        fg="white",
        activebackground=ORANGE,
        activeforeground="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
        command=clear_form
    ).grid(
        row=1,
        column=1,
        padx=3,
        pady=3,
        sticky="ew"
    )


    # ========================================================
    # TABLE CARD
    # ========================================================

    table_card = tk.Frame(
        main_frame,
        bg=CARD_COLOR,
        highlightbackground="#D6DEE8",
        highlightthickness=1
    )

    table_card.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=(10, 0)
    )


    # ========================================================
    # TABLE HEADER
    # ========================================================

    tk.Label(
        table_card,
        text="Registered Students",
        font=("Arial", 15, "bold"),
        bg=HEADER_COLOR,
        fg="white",
        anchor="w",
        padx=15,
        pady=12
    ).pack(
        fill="x"
    )


    # ========================================================
    # SEARCH
    # ========================================================

    search_frame = tk.Frame(
        table_card,
        bg=CARD_COLOR
    )

    search_frame.pack(
        fill="x",
        padx=15,
        pady=12
    )


    tk.Label(
        search_frame,
        text="🔍 Search:",
        font=("Arial", 10, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).pack(
        side="left"
    )


    search_var = tk.StringVar()


    search_entry = tk.Entry(
        search_frame,
        textvariable=search_var,
        font=("Arial", 10),
        relief="solid",
        bd=1
    )

    search_entry.pack(
        side="left",
        fill="x",
        expand=True,
        padx=8
    )


    # ========================================================
    # TABLE
    # ========================================================

    table_frame = tk.Frame(
        table_card,
        bg=CARD_COLOR
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=(0, 15)
    )


    columns = (
        "Roll No",
        "Name",
        "Department",
        "Email",
        "Phone"
    )


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
        font=("Arial", 9),
        rowheight=30,
        background="white",
        fieldbackground="white"
    )


    style.configure(
        "Treeview.Heading",
        font=("Arial", 9, "bold")
    )


    widths = {
        "Roll No": 100,
        "Name": 150,
        "Department": 130,
        "Email": 180,
        "Phone": 120
    }


    for column in columns:

        tree.heading(
            column,
            text=column
        )

        tree.column(
            column,
            width=widths[column],
            anchor="center"
        )


    tree.pack(
        side="left",
        fill="both",
        expand=True
    )


    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )

    tree.configure(
        yscrollcommand=scrollbar.set
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )


    # ========================================================
    # LOAD TABLE
    # ========================================================

    def load_table():

        for item in tree.get_children():

            tree.delete(item)


        students = get_all_students()


        search_text = (
            search_var.get()
            .strip()
            .lower()
        )


        for roll, student in students.items():

            name = student.get(
                "name",
                ""
            )

            department = student.get(
                "department",
                ""
            )

            email = student.get(
                "email",
                ""
            )

            phone = student.get(
                "phone",
                ""
            )


            searchable = (
                f"{roll} "
                f"{name} "
                f"{department} "
                f"{email} "
                f"{phone}"
            ).lower()


            if search_text and search_text not in searchable:

                continue


            tree.insert(
                "",
                "end",
                values=(
                    roll,
                    name,
                    department,
                    email,
                    phone
                )
            )


    # ========================================================
    # SEARCH EVENT
    # ========================================================

    search_var.trace_add(
        "write",
        lambda *args: load_table()
    )


    # ========================================================
    # SELECT STUDENT
    # ========================================================

    def select_student(event):

        selected = tree.selection()

        if not selected:

            return


        values = tree.item(
            selected[0],
            "values"
        )


        if len(values) < 5:

            return


        roll_var.set(values[0])
        name_var.set(values[1])
        department_var.set(values[2])
        email_var.set(values[3])
        phone_var.set(values[4])


    tree.bind(
        "<<TreeviewSelect>>",
        select_student
    )


    # ========================================================
    # CLOSE BUTTON
    # ========================================================

    tk.Button(
        window,
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
        command=window.destroy
    ).pack(
        pady=(0, 15)
    )


    # ========================================================
    # INITIAL LOAD
    # ========================================================

    load_table()


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()

    open_student_management()

    root.mainloop()