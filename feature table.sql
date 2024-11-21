CREATE TABLE CW2.feature(
    trail_feature_id INT IDENTITY(1,1) UNIQUE NOT NULL,
    trail_feature VARCHAR(100) NOT NULL,
    CONSTRAINT pk_feature PRIMARY KEY(trail_feature_id)
)