CREATE PROCEDURE CW2.insertintotrail 
@trail_name VARCHAR(255), 
@trail_summary VARCHAR(255),
@trail_description VARCHAR(255), 
@difficulty VARCHAR(25),
@location VARCHAR(255), 
@trail_length DECIMAL(4,2), 
@trail_elevation INT,
@route_type VARCHAR(20),
@trail_feature VARCHAR(100)
AS
BEGIN
    BEGIN TRANSACTION;

    BEGIN TRY
        INSERT INTO CW2.trail(
            trail_name, 
            trail_summary,
            trail_description, 
            difficulty,
            location, 
            trail_length, 
            trail_elevation,
            route_type
        )
        VALUES(
            @trail_name, 
            @trail_summary,
            @trail_description, 
            @difficulty,
            @location, 
            @trail_length, 
            @trail_elevation,
            @route_type
        )

        DECLARE @newtrailid INT = SCOPE_IDENTITY();

        INSERT INTO CW2.trail_feature(
            trail_id
        )
        VALUES(
            @newtrailid
        )

        DECLARE @newtrailfeatureid INT = SCOPE_IDENTITY();

        INSERT INTO CW2.feature(
            trail_feature_id,
            trail_feature
        )
        VALUES(
            @newtrailfeatureid,
            @trail_feature
        )


        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH;
END;

