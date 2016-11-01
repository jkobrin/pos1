drop table reopened;

CREATE TABLE reopened (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  reqhost VARCHAR(16) NOT NULL,
  created TIMESTAMP DEFAULT NOW(),
  closedby INT,
  order_group_id INT 
)ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
