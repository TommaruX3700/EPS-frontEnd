CREATE TABLE pallet (
    pallet_code VARCHAR(255) PRIMARY KEY,
    description VARCHAR(255),
    location VARCHAR(255)
);

CREATE TABLE pacchi (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pallet_code VARCHAR(255),
    content VARCHAR(255),
    weight DECIMAL(10, 2),
    FOREIGN KEY (pallet_code) REFERENCES pallet(pallet_code) ON DELETE SET NULL
);

-- inserting tests
INSERT INTO pallet (pallet_code, description, location)
VALUES ('P001', 'Electronics', 'Warehouse 1'),
       ('P002', 'Furniture', 'Warehouse 2');

INSERT INTO pacchi (pallet_code, content, weight)
VALUES ('P001', 'Laptop', 2.5),
       ('P001', 'Tablet', 1.2),
       ('P002', 'Chair', 7.0);

-- re-link packs tests
UPDATE pacchi
SET pallet_code = 'P002'
WHERE id = 1;
