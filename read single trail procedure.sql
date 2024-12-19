CREATE PROCEDURE CW2.readindividualtrail @trail_id INTEGER
AS 
SELECT * FROM 
CW2.trail as t
LEFT JOIN 
    CW2.trail_feature AS tf
    ON t.trail_id = tf.trail_id
LEFT JOIN 
    CW2.feature AS f
    ON tf.trail_feature_id = f.trail_feature_id
WHERE t.trail_id = @trail_id;