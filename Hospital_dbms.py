import sqlite3
import random
from datetime import date, timedelta

conn = sqlite3.connect("hospital_management.db", timeout=30)
cursor = conn.cursor()

try:
    cursor.execute("PRAGMA foreign_keys = ON")

    # -------------------------
    # DROP & CREATE TABLES
    # -------------------------
    cursor.executescript("""
    DROP TABLE IF EXISTS Billing;
    DROP TABLE IF EXISTS Prescription;
    DROP TABLE IF EXISTS Appointment;
    DROP TABLE IF EXISTS Doctor;
    DROP TABLE IF EXISTS Department;
    DROP TABLE IF EXISTS Patient;

    CREATE TABLE Patient (
        PatientID INTEGER PRIMARY KEY,
        FirstName TEXT NOT NULL,
        MiddleName TEXT,
        LastName TEXT NOT NULL,
        Gender TEXT CHECK (Gender IN ('Male', 'Female')),
        DateOfBirth DATE NOT NULL,
        Address TEXT,
        PhoneNumber TEXT UNIQUE,
        Email TEXT UNIQUE
    );

    CREATE TABLE Department (
        DepartmentID INTEGER PRIMARY KEY,
        DepartmentName TEXT NOT NULL UNIQUE,
        Location TEXT
    );

    CREATE TABLE Doctor (
        DoctorID INTEGER PRIMARY KEY,
        FirstName TEXT NOT NULL,
        MiddleName TEXT,
        LastName TEXT NOT NULL,
        Specialization TEXT,
        PhoneNumber TEXT UNIQUE,
        Email TEXT UNIQUE,
        DepartmentID INTEGER,
        FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
    );

    CREATE TABLE Appointment (
        AppointmentID INTEGER PRIMARY KEY,
        PatientID INTEGER NOT NULL,
        DoctorID INTEGER NOT NULL,
        AppointmentDate DATE NOT NULL,
        AppointmentTime TEXT NOT NULL,
        Status TEXT,
        FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
        FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID)
    );

    CREATE TABLE Prescription (
        PrescriptionID INTEGER PRIMARY KEY,
        AppointmentID INTEGER NOT NULL,
        MedicationDetails TEXT,
        Dosage TEXT,
        Duration TEXT,
        FOREIGN KEY (AppointmentID) REFERENCES Appointment(AppointmentID)
    );

    CREATE TABLE Billing (
        BillID INTEGER PRIMARY KEY,
        PatientID INTEGER NOT NULL,
        Amount REAL,
        BillDate DATE,
        PaymentStatus TEXT,
        FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
    );
    """)

    # -------------------------
    # DATA POOLS
    # -------------------------
    first_names = ["Aarav","Aditi","Rahul","Sneha","Rohit","Neha","Ankit","Pooja","Karan","Riya"]
    middle_names = ["Kumar","Chandra","Prasad","Lal",""]
    last_names = ["Sharma","Verma","Singh","Gupta","Patel","Iyer","Reddy","Mehta"]

    departments = [
        (101,"Cardiology","Delhi"),
        (102,"Neurology","Mumbai"),
        (103,"Orthopedics","Chennai"),
        (104,"Pediatrics","Bengaluru"),
        (105,"Radiology","Hyderabad")
    ]

    specializations = ["Cardiologist","Neurologist","Orthopedic","Pediatrician","Radiologist"]

    # -------------------------
    # INSERT DEPARTMENTS
    # -------------------------
    cursor.executemany("INSERT INTO Department VALUES (?,?,?)", departments)

    # -------------------------
    # INSERT 100 PATIENTS
    # -------------------------
    for i in range(100):
        pid = 1000 + i
        cursor.execute("""
        INSERT INTO Patient VALUES (?,?,?,?,?,?,?,?,?)
        """, (
            pid,
            random.choice(first_names),
            random.choice(middle_names),
            random.choice(last_names),
            random.choice(["Male","Female"]),
            date(1980,1,1) + timedelta(days=random.randint(0,15000)),
            "India",
            "+91" + str(random.randint(6000000000,9999999999)),
            f"patient{pid}@gmail.com"
        ))

    # -------------------------
    # INSERT 20 DOCTORS
    # -------------------------
    for i in range(20):
        did = 200 + i
        cursor.execute("""
        INSERT INTO Doctor VALUES (?,?,?,?,?,?,?,?)
        """, (
            did,
            random.choice(first_names),
            random.choice(middle_names),
            random.choice(last_names),
            random.choice(specializations),
            "+91" + str(random.randint(6000000000,9999999999)),
            f"doctor{did}@hospital.in",
            random.choice(departments)[0]
        ))

    # -------------------------
    # INSERT 100 APPOINTMENTS
    # -------------------------
    for i in range(100):
        aid = 5000 + i
        cursor.execute("""
        INSERT INTO Appointment VALUES (?,?,?,?,?,?)
        """, (
            aid,
            1000 + i,
            200 + random.randint(0,19),
            date(2025,1,1) + timedelta(days=random.randint(0,180)),
            f"{random.randint(9,17):02d}:{random.choice([0,15,30,45]):02d}",
            random.choice(["Scheduled","Completed"])
        ))

    # -------------------------
    # INSERT 100 PRESCRIPTIONS
    # -------------------------
    for i in range(100):
        cursor.execute("""
        INSERT INTO Prescription VALUES (?,?,?,?,?)
        """, (
            8000 + i,
            5000 + i,
            random.choice(["Paracetamol","Ibuprofen","Amoxicillin"]),
            random.choice(["Once a day","Twice a day"]),
            random.choice(["5 days","7 days"])
        ))

    # -------------------------
    # INSERT 100 BILLS
    # -------------------------
    for i in range(100):
        cursor.execute("""
        INSERT INTO Billing VALUES (?,?,?,?,?)
        """, (
            7000 + i,
            1000 + i,
            random.randint(500,15000),
            date(2025,1,1) + timedelta(days=random.randint(0,180)),
            random.choice(["Paid","Pending"])
        ))

    conn.commit()
    print(" 100-patient hospital dataset created successfully.")

finally:
    conn.close()


import sqlite3
import pandas as pd

# Connect to the existing database
conn = sqlite3.connect("hospital_management.db")

tables = [
    "Patient",
    "Department",
    "Doctor",
    "Appointment",
    "Prescription",
    "Billing"
]

for table in tables:
    print(f"\n========== {table} TABLE (First 100 Records) ==========")
    df = pd.read_sql_query(f"SELECT * FROM {table} LIMIT 100", conn)
    display(df)

conn.close() 

