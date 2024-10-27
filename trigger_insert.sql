DELIMITER |
CREATE TRIGGER copy_to_result
AFTER INSERT ON type_data
FOR EACH ROW
BEGIN
    INSERT INTO result (OTIME, equip_cd, mode, count_no, ok, quality_ng, cool_ng, press, quality, out_trigger, shot_type)
    VALUES (NEW.OTIME, NEW.equip_cd, NEW.mode, NEW.count_no, NEW.ok, NEW.quality_ng, NEW.cool_ng, NEW.press, NEW.quality, NEW.out_trigger, NEW.shot_type);
END |
DELIMITER ;