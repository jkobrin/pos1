
drop table order_group;

CREATE TABLE order_group (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  table_id VARCHAR(3) NOT NULL,
  is_open boolean NOT NULL DEFAULT TRUE,
  created TIMESTAMP DEFAULT NOW()
);


CREATE TABLE order_item (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  order_group_id INT NOT NULL,
  item_name VARCHAR(32) NOT NULL,
  price FLOAT NOT NULL,
  item_cancelled BOOLEAN NOT NULL DEFAULT FALSE,
  created TIMESTAMP DEFAULT NOW(),
  updated TIMESTAMP DEFAULT 0,
  INDEX order_idx (order_group_id),
  FOREIGN KEY (order_group_id) REFERENCES order_group(id) ON DELETE CASCADE
);


