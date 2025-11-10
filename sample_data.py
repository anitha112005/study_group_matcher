from models import init_db, load_sample_students

if __name__ == "__main__":
    DB_PATH = "students.db"
    init_db(DB_PATH)
    load_sample_students(DB_PATH, overwrite=True)
    print("Sample data loaded into students.db")
