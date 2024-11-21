CREATE PROCEDURE CW2.deletetrail @trail_id INT
AS
BEGIN
    BEGIN TRANSACTION;

    BEGIN TRY
        DELETE FROM CW2.feature
            WHERE trail_feature_id IN (
                SELECT trail_feature_id
                FROM CW2.trail_feature
                WHERE trail_id = @trail_id
            );
        DELETE FROM CW2.trail WHERE trail_id = @trail_id;
        DELETE FROM CW2.trail_feature WHERE trail_id = @trail_id;
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH;
END;