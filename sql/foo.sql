
drop table if exists order_group;

CREATE TABLE order_group (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  table_id VARCHAR(3) NOT NULL,
  is_open boolean NOT NULL DEFAULT TRUE,
  closedby smallint,
  created TIMESTAMP DEFAULT NOW(),
  updated TIMESTAMP DEFAULT 0,
  FOREIGN KEY (closedby) REFERENCES person(id) ON DELETE CASCADE
) ENGINE=MyISAM;
