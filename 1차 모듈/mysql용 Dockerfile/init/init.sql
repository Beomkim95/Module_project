CREATE TABLE item(id INTEGER not null AUTO_INCREMENT PRIMARY KEY, p_name VARCHAR(20), p_price float, p_qty int, created_at DATE);

CREATE TABLE Member(id INTEGER not null AUTO_INCREMENT PRIMARY KEY, email VARCHAR(20), pwd VARCHAR(20),created_at DATE);

CREATE TABLE Order_(id INTEGER not null AUTO_INCREMENT PRIMARY KEY, member_id VARCHAR(20), item_id VARCHAR(20), order_qty int, order_price FLOAT, created_at DATE);