CREATE PROCEDURE CW2.updatetrail
    @trail_id INT,
    @newtrailname VARCHAR(255) = NULL,
    @newtrailsummary VARCHAR(255) = NULL,
    @newtraildescription VARCHAR(255) = NULL,
    @newdifficulty VARCHAR(25) = NULL,
    @newlocation VARCHAR(255) = NULL,
    @newtraillength DECIMAL(4, 2) = NULL,
    @newtrailelevation INT = NULL,
    @newroutetype VARCHAR(20) = NULL,
    @newfeature VARCHAR(100) = NULL
AS
BEGIN
    BEGIN TRANSACTION;

    BEGIN TRY
        UPDATE CW2.trail
        SET trail_name = COALESCE(@newtrailname, trail_name),
            trail_summary = COALESCE(@newtrailsummary, trail_summary),
            trail_description = COALESCE(@newtraildescription, trail_description),
            difficulty = COALESCE(@newdifficulty, difficulty),
            location = COALESCE(@newlocation, location),
            trail_length = COALESCE(@newtraillength, trail_length),
            trail_elevation = COALESCE(@newtrailelevation, trail_elevation),
            route_type = COALESCE(@newroutetype, route_type)
        WHERE trail_id = @Trail_id;

        UPDATE CW2.feature
        SET trail_feature = COALESCE(@newfeature, trail_feature)
        WHERE trail_feature_id IN (
            SELECT trail_feature_id
            FROM CW2.trail_feature
            WHERE trail_id = @trail_id
        )

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH;
END;