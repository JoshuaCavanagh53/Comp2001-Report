CREATE TABLE CW2.trail (
    trail_id INT IDENTITY(1,1) PRIMARY KEY, 
    trail_name VARCHAR(255) NOT NULL,       
    trail_summary VARCHAR(255),             
    trail_description TEXT,                 
    difficulty VARCHAR(25),                 
    location VARCHAR(255),                  
    trail_length DECIMAL(4, 2),             
    trail_elevation INT,                    
    route_type VARCHAR(20)                  
);

CREATE TABLE CW2.trail_feature (
    trail_feature_id INT IDENTITY(1,1) PRIMARY KEY, 
    trail_id INT NOT NULL,                           
    FOREIGN KEY (trail_id) REFERENCES CW2.trail(trail_id)  
);


CREATE TABLE CW2.feature (
    trail_feature_id INT NOT NULL, 
    trail_feature VARCHAR(100),    
    PRIMARY KEY (trail_feature_id),
    FOREIGN KEY (trail_feature_id) REFERENCES CW2.trail_feature(trail_feature_id) 
);