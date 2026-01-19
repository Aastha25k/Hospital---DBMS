-- Hospital Management System Database Schema

-- =========================
-- Patient Table
-- =========================
CREATE TABLE Patient (
    PatientID INT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    MiddleName VARCHAR(50),
    LastName VARCHAR(50) NOT NULL,
    Gender VARCHAR(10) CHECK (Gender IN ('Male', 'Female')),
    DateOfBirth DATE NOT NULL,
    Address VARCHAR(100),
    PhoneNumber VARCHAR(15) UNIQUE,
    Email VARCHAR(100) UNIQUE
);

-- =========================
-- Department Table
-- =========================
CREATE TABLE Department (
    DepartmentID INT PRIMARY KEY,
    DepartmentName VARCHAR(100) NOT NULL UNIQUE,
    Location VARCHAR(50)
);

-- =========================
-- Doctor Table
-- =========================
CREATE TABLE Doctor (
    DoctorID INT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    MiddleName VARCHAR(50),
    LastName VARCHAR(50) NOT NULL,
    Specialization VARCHAR(100),
    PhoneNumber VARCHAR(15) UNIQUE,
    Email VARCHAR(100) UNIQUE,
    DepartmentID INT,
    FOREIGN KEY (DepartmentID)
        REFERENCES Department(DepartmentID)
);

-- =========================
-- Appointment Table
-- =========================
CREATE TABLE Appointment (
    AppointmentID INT PRIMARY KEY,
    PatientID INT NOT NULL,
    DoctorID INT NOT NULL,
    AppointmentDate DATE NOT NULL,
    AppointmentTime VARCHAR(10) NOT NULL,
    Status VARCHAR(20) DEFAULT 'Scheduled',
    FOREIGN KEY (PatientID)
        REFERENCES Patient(PatientID),
    FOREIGN KEY (DoctorID)
        REFERENCES Doctor(DoctorID)
);

-- =========================
-- Prescription Table
-- =========================
CREATE TABLE Prescription (
    PrescriptionID INT PRIMARY KEY,
    AppointmentID INT NOT NULL,
    MedicationDetails VARCHAR(100),
    Dosage VARCHAR(50),
    Duration VARCHAR(50),
    FOREIGN KEY (AppointmentID)
        REFERENCES Appointment(AppointmentID)
);

-- =========================
-- Billing Table
-- =========================
CREATE TABLE Billing (
    BillID INT PRIMARY KEY,
    PatientID INT NOT NULL,
    Amount FLOAT CHECK (Amount > 0),
    BillDate DATE NOT NULL,
    PaymentStatus VARCHAR(20) DEFAULT 'Pending',
    FOREIGN KEY (PatientID)
        REFERENCES Patient(PatientID)
);
