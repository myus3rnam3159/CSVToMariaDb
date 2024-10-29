DELIMITER |
CREATE TRIGGER update_result
AFTER INSERT ON toscast_data
FOR EACH ROW
BEGIN
    UPDATE result
    SET M_Name = NEW.M_Name,
    Shot_No = NEW.Shot_No,
    C1 = New.C1,
    C2 = New.C2,
    C3 = New.C3,
    C4 = New.C1,
    C5 = New.C2,
    C6 = New.C3,
    C7 = New.C7,
    otime = (SELECT result.otime FROM result ORDER BY ABS(otime - NEW.otime) ASC LIMIT 1)
    WHERE equip_cd = NEW.equip_cd;
END |
DELIMITER ;