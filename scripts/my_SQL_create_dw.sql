CREATE DATABASE IF NOT EXISTS cis9440;
USE cis9440;


-- 1. Create the Staging Table (Temporary holding area)
CREATE TABLE Staging_MetroBike (
    trip_id BIGINT,
    membership_type VARCHAR(100),
    bicycle_id VARCHAR(50),
    bike_type VARCHAR(50),
    checkout_datetime DATETIME,
    checkout_date DATE,
    checkout_time VARCHAR(20),
    checkout_kiosk_id VARCHAR(50),
    checkout_kiosk VARCHAR(255),
    return_kiosk_id VARCHAR(50),
    return_kiosk VARCHAR(255),
    trip_duration_minutes INT,
    month VARCHAR(20),
    year INT
);

-- 2. Create Dimension Tables
CREATE TABLE Dim_Kiosk (
    kiosk_key INT AUTO_INCREMENT PRIMARY KEY,   -- Surrogate Key
    kiosk_id VARCHAR(50),                       -- Natural Key
    kiosk_name VARCHAR(255)
);

CREATE TABLE Dim_Bike (
    bike_key INT AUTO_INCREMENT PRIMARY KEY,
    bicycle_id VARCHAR(50),
    bike_type VARCHAR(50)
);

CREATE TABLE Dim_Membership (
    membership_key INT AUTO_INCREMENT PRIMARY KEY,
    membership_type VARCHAR(100)
);

CREATE TABLE Dim_Date (
    date_key INT AUTO_INCREMENT PRIMARY KEY,
    full_date DATE,
    month VARCHAR(20),
    year INT
);

-- 3. Create Fact Table
CREATE TABLE Fact_Trips (
    trip_key INT AUTO_INCREMENT PRIMARY KEY,
    trip_id BIGINT,
    trip_duration_minutes INT,
    checkout_datetime DATETIME,
    
    -- Foreign Keys
    checkout_kiosk_key INT,
    return_kiosk_key INT,
    bike_key INT,
    membership_key INT,
    date_key INT,

    -- Links to Dimensions
    FOREIGN KEY (checkout_kiosk_key) REFERENCES Dim_Kiosk(kiosk_key),
    FOREIGN KEY (return_kiosk_key) REFERENCES Dim_Kiosk(kiosk_key),
    FOREIGN KEY (bike_key) REFERENCES Dim_Bike(bike_key),
    FOREIGN KEY (membership_key) REFERENCES Dim_Membership(membership_key),
    FOREIGN KEY (date_key) REFERENCES Dim_Date(date_key)
);

