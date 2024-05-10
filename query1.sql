use school_meal_discount;
CREATE TABLE `members`(
	`member_id` VARCHAR(45) NOT NULL PRIMARY KEY,
    `member_type` boolean DEFAULT FALSE,
    `member_registration_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `member_name` VARCHAR(45) 
);

CREATE TABLE `shops`(
	`shop_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `shop_registration_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `shop_name` VARCHAR(45) ,
    `shop_run_time` VARCHAR(11),
    `shop_menu_url` VARCHAR(70)
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

INSERT INTO `shops`(shop_id,shop_name,shop_run_time,shop_menu_url)VALUE('1','早安美廣','07:00~16:00','https://i.postimg.cc/mZjPk5QG/2024-05-09-203153.jpg');
INSERT INTO `shops`(shop_id,shop_name,shop_run_time,shop_menu_url)VALUE('2','傳香飯糰','07:00~19:30','https://i.postimg.cc/mDQ1dQjb/2024-05-03-225704.jpg');
INSERT INTO `shops`(shop_id,shop_name,shop_run_time,shop_menu_url)VALUE('3','八方雲集','11:00~19:30','https://i.postimg.cc/3xSqRGgJ/2024-05-03-225723.jpg');
INSERT INTO `shops`(shop_id,shop_name,shop_run_time,shop_menu_url)VALUE('4','宜廷小吃','11:00~19:30','https://i.postimg.cc/RZxLnJmS/19d872c0-4906-42b2-a283-ae6882ee8443.jpg');
INSERT INTO `shops`(shop_id,shop_name,shop_run_time,shop_menu_url)VALUE('5','琪美食堂','11:00~19:30','https://i.postimg.cc/Pf6nQZrM/0dabfdda-0f3d-430d-b974-d6c1c746c1e8.jpg');
INSERT INTO `shops`(shop_id,shop_name,shop_run_time,shop_menu_url)VALUE('6','美廣鮮果吧','11:00~19:30','https://i.postimg.cc/SKTcrkjR/2024-05-03-224705.jpg');
INSERT INTO `shops`(shop_id,shop_name,shop_run_time)VALUE('7','自助餐','11:00~19:30');

INSERT INTO `shops`(shop_id,shop_name,shop_run_time)VALUE('7', '宜廷小吃', '11:00~19:30');
ALTER TABLE shops ADD shop_menu_url VARCHAR(70);
DROP TABLE `members`;
DROP TABLE `shops`;
DROP TABLE `menu`;
DROP TABLE `order_histories`;
DESCRIBE `members`;
DELETE FROM `members`;
DELETE FROM `order_histories`
WHERE order_id = 1 AND shop_id = 1;

DELETE FROM `shops`
WHERE shop_id < 8;