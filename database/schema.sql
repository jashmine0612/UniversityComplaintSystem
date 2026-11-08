
CREATE DATABASE IF NOT EXISTS university_complaints;

USE university_complaints;


-- 1. Departments table
CREATE TABLE IF NOT EXISTS departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);


-- 2. Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    department_id INT NULL,
    is_active BOOLEAN DEFAULT TRUE,

    FOREIGN KEY (department_id)
        REFERENCES departments(id)
);


-- 3. Complaints table
CREATE TABLE IF NOT EXISTS complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    complaint_code VARCHAR(30) NOT NULL UNIQUE,

    roll_number VARCHAR(30) NOT NULL,
    description TEXT NOT NULL,
    image_path VARCHAR(255) NULL,
    location VARCHAR(255) NOT NULL,

    category VARCHAR(100) NULL,
    priority VARCHAR(20) DEFAULT 'MEDIUM',

    department_id INT NULL,
    assigned_officer_id INT NULL,

    status VARCHAR(50) DEFAULT 'PENDING',
    verification_token_hash VARCHAR(255) NOT NULL,

    resolution_remarks TEXT NULL,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deadline DATETIME NULL,
    resolved_at DATETIME NULL,
    closed_at DATETIME NULL,

    closure_reason VARCHAR(50) NULL
);


-- 4. Complaint history table
CREATE TABLE IF NOT EXISTS complaint_history (
    id INT AUTO_INCREMENT PRIMARY KEY,

    complaint_id INT NOT NULL,
    old_status VARCHAR(50) NULL,
    new_status VARCHAR(50) NOT NULL,
    remarks TEXT NULL,

    changed_by INT NULL,
    changed_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (complaint_id)
        REFERENCES complaints(id),

    FOREIGN KEY (changed_by)
        REFERENCES users(id)
);
