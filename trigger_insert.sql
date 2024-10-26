CREATE TRIGGER copy_to_result
AFTER INSERT ON type_data
FOR EACH ROW
BEGIN
    INSERT INTO result (equip_cd, otime, type_cd)
    VALUES (NEW.equip_cd, NEW.otime, NEW.type_cd);
END;