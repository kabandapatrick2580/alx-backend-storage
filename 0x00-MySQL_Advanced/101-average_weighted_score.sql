DELIMITER //

-- Create the stored procedure ComputeAverageWeightedScoreForUsers
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_id INT;
    DECLARE weighted_sum FLOAT;
    DECLARE total_weight FLOAT;
    
    -- Declare cursor for selecting user IDs
    DECLARE user_cursor CURSOR FOR
        SELECT id FROM users;
    
    -- Declare continue handler
    DECLARE CONTINUE HANDLER FOR NOT FOUND
        SET user_id = NULL;
    
    -- Open the cursor
    OPEN user_cursor;
    
    -- Loop through each user
    user_loop: LOOP
        -- Fetch the next user ID
        FETCH user_cursor INTO user_id;
        
        -- Exit loop if no more users
        IF user_id IS NULL THEN
            LEAVE user_loop;
        END IF;
        
        -- Reset variables
        SET weighted_sum = 0;
        SET total_weight = 0;
        
        -- Calculate the weighted sum of scores for the user
        SELECT SUM(c.score * p.weight) INTO weighted_sum
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id;
        
        -- Calculate the total weight of projects for the user
        SELECT SUM(p.weight) INTO total_weight
        FROM projects p
        JOIN corrections c ON c.project_id = p.id
        WHERE c.user_id = user_id;

        -- Calculate the average weighted score
        IF total_weight > 0 THEN
            UPDATE users
            SET average_score = weighted_sum / total_weight
            WHERE id = user_id;
        ELSE
            UPDATE users
            SET average_score = 0
            WHERE id = user_id;
        END IF;
    END LOOP;
    
    -- Close the cursor
    CLOSE user_cursor;
    
END;
//

DELIMITER ;
