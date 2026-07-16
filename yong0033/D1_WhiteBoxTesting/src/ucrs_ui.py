# src/ucrs_ui.py
# pylint: disable=protected-access
"""
URCS: University Course Registration System (console UI)
"""

from src import user_input
from src import urcs_logic
from src.allocation import Seat


class UCRSUI:
    """
    Manages the UI screens of URCS and transitions between them.
    """

    def __init__(self, data_manager):
        self._current_screen = self._main_menu
        self._dm = data_manager

    def get_current_screen(self):
        screen_map = {
            self._main_menu: "MAIN MENU",
            self._enrol: "ENROL IN COURSE",
            self._drop: "DROP COURSE",
            self._search_student: "SEARCH STUDENT",
            self._register_student: "REGISTER STUDENT",
            self._search_course: "SEARCH COURSE",
            self._quit: "QUIT",
        }
        return screen_map.get(self._current_screen, "MAIN MENU")

    def run_current_screen(self):
        self._current_screen = self._current_screen()

    # ---------- screens ----------

    def _main_menu(self):
        print("""
            ---------------------------------------
            | URCS: Course Registration Terminal |
            ---------------------------------------

            1. Enrol in Course
            2. Drop Course
            3. Search Student
            4. Register Student
            5. Search Course
            6. Save & Quit
            """)
        choice = user_input.read_integer_range("Enter your choice: ", 1, 6)

        if choice == 1:
            return self._enrol
        elif choice == 2:
            return self._drop
        elif choice == 3:
            return self._search_student
        elif choice == 4:
            return self._register_student
        elif choice == 5:
            return self._search_course
        elif choice == 6:
            return self._quit
        else:
            return self._main_menu

    # --- helpers ---

    def _find_student_by_id(self, student_id):
        for student_rec in self._dm._student_data:
            if student_rec.get("student_id") == student_id:
                return student_rec
        return None

    def _find_student_by_name(self, name):
        name_lower = str(name).lower()
        results = []
        for student_rec in self._dm._student_data:
            if str(student_rec.get("name", "")).lower() == name_lower:
                results.append(student_rec)
        return results

    def _find_course_by_id(self, course_id):
        for course in self._dm._course_data:
            if course._id == course_id:
                return course
        return None

    def _find_course_by_code(self, code):
        code_lower = str(code).lower()
        for course in self._dm._course_data:
            if str(course._code).lower() == code_lower:
                return course
        return None

    # --- enrol ---

    def _enrol(self):
        print("""
            --------------------------
            | URCS: Enrol in Course |
            --------------------------
        """)
        # student
        mode = user_input.read_integer_range("Find student by (1) ID or (2) Name? ", 1, 2)
        student = None
        if mode == 1:
            student_id = user_input.read_integer("Enter Student ID: ")
            student = self._find_student_by_id(student_id)
        else:
            student_name = user_input.read_string("Enter Student Name: ")
            matched_students = self._find_student_by_name(student_name)
            if not matched_students:
                print("!!! NO SUCH STUDENT.")
                return self._main_menu
            if len(matched_students) > 1:
                print("Multiple students found with that name:")
                for student_rec in matched_students:
                    print(f"  - ID {student_rec['student_id']}: {student_rec['name']}")
                student_id = user_input.read_integer("Enter Student ID: ")
                student = self._find_student_by_id(student_id)
            else:
                student = matched_students[0]

        if student is None:
            print("!!! NO SUCH STUDENT. CANCELLING.")
            return self._main_menu

        # course
        mode = user_input.read_integer_range("Find course by (1) ID or (2) Code? ", 1, 2)
        course = None
        if mode == 1:
            course_id = user_input.read_integer("Enter Course ID: ")
            course = self._find_course_by_id(course_id)
        else:
            course_code = user_input.read_string("Enter Course Code: ")
            course = self._find_course_by_code(course_code)

        if course is None:
            print("!!! NO SUCH COURSE. CANCELLING.")
            return self._main_menu

        print(f"Selected: {course._code} - {course._title} ({course._credits} credits)")
        print(f"Capacity: {len(course._enrolled)}/{course._capacity}")

        current_credits = student.get("current_credits", 0)
        completed_courses = student.get("completed_courses", [])
        student_slots = student.get("timeslots", [])
        required_prereqs = course._prerequisites
        course_slots = course._timeslots

        seat_helper = Seat(course)
        seat_available = (seat_helper.is_full() is False)

        waitlist_pref_opt_in = None
        if seat_available is False:
            print("No seats available.")
            wl = user_input.read_bool("Join waitlist? (y/n): ")
            waitlist_pref_opt_in = bool(wl)

        outcome, reason = urcs_logic.decide_enrolment_and_allocation(
            current_credits=current_credits,
            course_credits=course._credits,
            completed_courses=completed_courses,
            required_prereqs=required_prereqs,
            student_slots=student_slots,
            course_slots=course_slots,
            seat_available=seat_available,
            waitlist_pref_opt_in=waitlist_pref_opt_in,
            prereq_override=False,
        )

        if outcome == "Allocated Approved":
            if student.get("student_id") not in course._enrolled:
                course._enrolled.append(student.get("student_id"))
            student["current_credits"] = current_credits + int(course._credits)
            print(f"SUCCESS: {student['name']} enrolled in {course._code} ({reason}).")
        elif outcome == "Waitlisted":
            if student.get("student_id") not in course._waitlist:
                course._waitlist.append(student.get("student_id"))
            print(f"WAITLISTED: {student['name']} added to waitlist for {course._code} ({reason}).")
        else:
            print(f"REJECTED: {student['name']} not enrolled in {course._code} (reason: {reason}).")

        return self._main_menu

    # --- drop ---

    def _drop(self):
        print("""
            -----------------------
            | URCS: Drop Course   |
            -----------------------
        """)
        student_id = user_input.read_integer("Enter Student ID: ")
        student = self._find_student_by_id(student_id)
        if student is None:
            print("!!! NO SUCH STUDENT.")
            return self._main_menu

        mode = user_input.read_integer_range("Find course by (1) ID or (2) Code? ", 1, 2)
        course = None
        if mode == 1:
            course_id = user_input.read_integer("Enter Course ID: ")
            course = self._find_course_by_id(course_id)
        else:
            course_code = user_input.read_string("Enter Course Code: ")
            course = self._find_course_by_code(course_code)

        if course is None:
            print("!!! NO SUCH COURSE.")
            return self._main_menu

        sid_val = student.get("student_id")
        if sid_val in course._enrolled:
            course._enrolled.remove(sid_val)
            new_credits = int(student.get("current_credits", 0)) - int(course._credits)
            if new_credits < 0:
                new_credits = 0
            student["current_credits"] = new_credits
            if course._waitlist:
                promoted_student_id = course._waitlist.pop(0)
                if promoted_student_id not in course._enrolled:
                    course._enrolled.append(promoted_student_id)
            print(f"Dropped: {student['name']} from {course._code}.")
        elif sid_val in course._waitlist:
            course._waitlist.remove(sid_val)
            print(f"Removed: {student['name']} from {course._code} waitlist.")
        else:
            print("Student is neither enrolled nor on the waitlist for this course.")

        return self._main_menu

    # --- search student ---

    def _search_student(self):
        print("""
            -----------------------
            | URCS: Find Student  |
            -----------------------

            1. Search by ID
            2. Search by Name
            3. Back
        """)
        choice = user_input.read_integer_range("Enter your choice: ", 1, 3)

        if choice == 1:
            student_id = user_input.read_integer("Student ID: ")
            student = self._find_student_by_id(student_id)
            if student is None:
                print("NO STUDENT FOUND.")
            else:
                self._print_student(student)
        elif choice == 2:
            name = user_input.read_string("Student Name: ")
            matched_students = self._find_student_by_name(name)
            if not matched_students:
                print("NO STUDENTS FOUND.")
            else:
                for student in matched_students:
                    self._print_student(student)
        return self._main_menu

    def _print_student(self, student):
        print(f"Student {student.get('student_id')}: {student.get('name')}")
        print(f"  Current credits: {student.get('current_credits', 0)}")
        completed = student.get("completed_courses", [])
        print(f"  Completed: {', '.join(completed) if completed else 'none'}")
        slots = student.get("timeslots", [])
        print(f"  Timeslots: {', '.join(slots) if slots else 'n/a'}")

    # --- register student ---

    def _register_student(self):
        print("""
            ------------------------------
            | URCS: Register New Student |
            ------------------------------
        """)
        name = user_input.read_string("Student name: ")
        new_student = self._dm.register_student(
            name=name,
            current_credits=0,
            completed_courses=[],
            timeslots=[],
            holds=False
        )
        print(f"Registered student ID {new_student['student_id']}: {new_student['name']}")
        return self._main_menu

    # --- search course ---

    def _search_course(self):
        print("""
            ----------------------
            | URCS: Find Course  |
            ----------------------

            1. Search by ID
            2. Search by Code
            3. List All
            4. Back
        """)
        choice = user_input.read_integer_range("Enter your choice: ", 1, 4)

        if choice == 1:
            course_id = user_input.read_integer("Course ID: ")
            course_obj = self._find_course_by_id(course_id)
            if course_obj is None:
                print("NO COURSE FOUND.")
            else:
                self._print_course(course_obj)
        elif choice == 2:
            code = user_input.read_string("Course Code: ")
            course_obj = self._find_course_by_code(code)
            if course_obj is None:
                print("NO COURSE FOUND.")
            else:
                self._print_course(course_obj)
        elif choice == 3:
            for course_obj in self._dm._course_data:
                self._print_course(course_obj)
        return self._main_menu

    def _print_course(self, course):
        print(f"{course._code} - {course._title}")
        print(f"  ID: {course._id}, Credits: {course._credits}, Mode: {course._mode}")
        print(f"  Capacity: {len(course._enrolled)}/{course._capacity}")
        if course._prerequisites:
            print(f"  Prereqs: {', '.join(course._prerequisites)}")
        else:
            print("  Prereqs: none")
        if course._timeslots:
            print(f"  Timeslots: {', '.join(sorted(course._timeslots))}")
        else:
            print("  Timeslots: n/a")
        if course._waitlist:
            print(f"  Waitlist: {len(course._waitlist)} student(s)")

    # --- quit ---

    def _quit(self):
        print("Saving data...")
        try:
            self._dm.save_students()
            self._dm.save_courses()
            print("Saved. Bye!")
        except Exception:
            print("ERROR SAVING DATA (files unchanged).")
        return self._quit
