USE cis9440_final;

-- 1. Populate Dimensions
INSERT INTO Dim_Kiosk (kiosk_id, kiosk_name)
SELECT DISTINCT checkout_kiosk_id, checkout_kiosk FROM Staging_MetroBike WHERE checkout_kiosk_id IS NOT NULL
UNION SELECT DISTINCT return_kiosk_id, return_kiosk FROM Staging_MetroBike WHERE return_kiosk_id IS NOT NULL;

INSERT INTO Dim_Bike (bicycle_id, bike_type)
SELECT DISTINCT bicycle_id, bike_type FROM Staging_MetroBike WHERE bicycle_id IS NOT NULL;

INSERT INTO Dim_Membership (membership_type)
SELECT DISTINCT membership_type FROM Staging_MetroBike WHERE membership_type IS NOT NULL;

INSERT INTO Dim_Date (full_date, month, year)
SELECT DISTINCT checkout_date, month, year FROM Staging_MetroBike;

-- 2. Create Indexes for Performance
CREATE INDEX idx_checkout_kiosk ON Staging_MetroBike(checkout_kiosk_id);
CREATE INDEX idx_return_kiosk ON Staging_MetroBike(return_kiosk_id);
CREATE INDEX idx_bike ON Staging_MetroBike(bicycle_id);
CREATE INDEX idx_membership ON Staging_MetroBike(membership_type);
CREATE INDEX idx_date ON Staging_MetroBike(checkout_date);

-- 3. Populate Fact Table
INSERT INTO Fact_Trips (trip_id, trip_duration_minutes, checkout_datetime, checkout_kiosk_key, return_kiosk_key, bike_key, membership_key, date_key)
SELECT 
    s.trip_id, 
    s.trip_duration_minutes, 
    s.checkout_datetime,
    k_out.kiosk_key,
    k_in.kiosk_key,
    b.bike_key,
    m.membership_key,
    d.date_key
FROM Staging_MetroBike s
LEFT JOIN Dim_Kiosk k_out ON s.checkout_kiosk_id = k_out.kiosk_id
LEFT JOIN Dim_Kiosk k_in ON s.return_kiosk_id = k_in.kiosk_id
LEFT JOIN Dim_Bike b ON s.bicycle_id = b.bicycle_id
LEFT JOIN Dim_Membership m ON s.membership_type = m.membership_type
LEFT JOIN Dim_Date d ON s.checkout_date = d.full_date;
