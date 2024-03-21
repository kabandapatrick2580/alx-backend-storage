DELIMITER //

-- Create a trigger to reset the valid_email attribute only when the email has been changed
CREATE TRIGGER reset_valid_email_after_email_update
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    -- Check if the email has been changed
    IF OLD.email != NEW.email THEN
        SET NEW.valid_email = 0; -- Reset valid_email attribute
    END IF;
END;
//

DELIMITER ;
