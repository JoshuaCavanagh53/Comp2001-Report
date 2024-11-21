CREATE TABLE CW2.trail_feature(
    trail_id INT NOT NULL,
    trail_feature_id INT IDENTITY(1,1) NOT NULL,
    CONSTRAINT pk_trail_feature PRIMARY KEY(trail_id, trail_feature_id),
    CONSTRAINT fk_trail FOREIGN KEY(trail_id) REFERENCES CW2.trail (trail_id),
    CONSTRAINT fk_feature FOREIGN KEY(trail_feature_id) REFERENCES CW2.feature (trail_feature_id)
)