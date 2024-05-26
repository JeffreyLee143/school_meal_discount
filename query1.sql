use school_meal_discount;
CREATE TABLE `members`(
	`member_id` INT AUTO_INCREMENT PRIMARY KEY,
    `member_type` boolean DEFAULT FALSE,
    `member_registration_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `member_number` VARCHAR(45) ,
    `member_name` VARCHAR(45) ,
    `member_mail` VARCHAR(50) 
);

CREATE TABLE `shops`(
	`shop_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `shop_registration_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `shop_name` VARCHAR(45) ,
    `shop_run_time` VARCHAR(11)
);

CREATE TABLE `menu`(
	`shop_id` INT NOT NULL,
    `product_id` INT,
    `product_name` VARCHAR(45) NOT NULL,
    `product_price` DOUBLE NOT NULL,
    PRIMARY KEY(`shop_id`,`product_id`),
    FOREIGN KEY (`shop_id`) REFERENCES `shops`(`shop_id`) ON DELETE CASCADE
);

CREATE TABLE `order_histories`(
	`order_id` INT NOT NULL AUTO_INCREMENT,
    `shop_id` INT,
    `trade_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `product_name` VARCHAR(45) ,
    `total_cost` INT ,
    `order_status` boolean DEFAULT FALSE,
    PRIMARY KEY(`order_id`,`shop_id`),
    FOREIGN KEY (`shop_id`) REFERENCES `shops`(`shop_id`) ON DELETE CASCADE
);

CREATE TABLE `manager`(
	`manager_id` INT NOT NULL AUTO_INCREMENT,
    `manager_mail` VARCHAR(45) 
);

INSERT INTO `shops`(shop_number,shop_name,shop_mail)VALUE('123','456','789');
DROP TABLE `members`;
DROP TABLE `shops`;
DROP TABLE `menu`;
DROP TABLE `order_histories`;
DESCRIBE `members`;
DELETE FROM `members`;
DELETE FROM `order_histories`
WHERE order_id = 1 AND shop_id = 1;