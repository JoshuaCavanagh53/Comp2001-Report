CREATE TABLE CW2.trail(
    trail_id INT IDENTITY(1,1) UNIQUE NOT NULL,
    trail_name VARCHAR(255) NOT NULL,
    trail_summary VARCHAR(255) NOT NULL,
    trail_description VARCHAR(255) NOT NULL,
    difficulty VARCHAR(25) NOT NULL,
    location VARCHAR(255) NOT NULL,
    trail_length DECIMAL(4,2) NOT NULL,
    trail_elevation INT NOT NULL,
    route_type VARCHAR(20) NOT NULL
    CONSTRAINT pk_trail PRIMARY KEY(trail_id)
)