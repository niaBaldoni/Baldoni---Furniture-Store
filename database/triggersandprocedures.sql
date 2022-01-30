DROP TRIGGER IF EXISTS `baldonifurniturestore`.`fur_tra_BEFORE_INSERT`;
fur_tra_BEFORE_INSERT
DELIMITER $$
USE `baldonifurniturestore`$$
CREATE DEFINER = CURRENT_USER TRIGGER `baldonifurniturestore`.`fur_tra_BEFORE_INSERT` BEFORE INSERT ON `fur_tra` FOR EACH ROW
BEGIN
	SET @StoreId = (SELECT Transactions.Store_Id FROM Transactions WHERE Transactions.Transaction_Id = NEW.Transaction_Id);
    SET @avail = (SELECT Fur_Sto.Quantity FROM Fur_Sto WHERE Fur_Sto.Store_Id = @StoreId AND Fur_Sto.Furniture_Id = NEW.Furniture_Id);
    IF (@avail >= NEW.Quantity) THEN
		UPDATE Fur_Sto SET Quantity = (Quantity - NEW.Quantity) WHERE Fur_Sto.Store_Id = @StoreId;
	ELSE
		SIGNAL SQLSTATE '45000' SET message_text = 'Not enough requested furniture in this store';
	END IF;
END$$
DELIMITER ;

DROP TRIGGER IF EXISTS `baldonifurniturestore`.`fur_tra_AFTER_INSERT`;
fur_tra_AFTER_INSERT
DELIMITER $$
USE `baldonifurniturestore`$$
CREATE DEFINER = CURRENT_USER TRIGGER `baldonifurniturestore`.`fur_tra_AFTER_INSERT` AFTER INSERT ON `fur_tra` FOR EACH ROW
BEGIN
	DECLARE IssueTime DATETIME;
    SET @IssueTime = (SELECT Transactions.Transaction_Date FROM Transactions WHERE Transactions.Transaction_Id = NEW.Transaction_Id);
    UPDATE Transactions INNER JOIN Prices ON Prices.Furniture_Id = NEW.Furniture_Id
    SET Transactions.Total = Transactions.Total + (((Prices.Price / 100) * Prices.Discount) * NEW.Quantity)
    WHERE Transactions.Transaction_Id = NEW.Transaction_Id AND Prices.Furniture_Id = NEW.Furniture_Id AND @IssueTime BETWEEN Prices.Start_Date AND Prices.End_Date;
END$$
DELIMITER ;
