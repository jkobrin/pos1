drop table if exists tip_slips_printed;

CREATE TABLE tip_slips_printed(
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  created TIMESTAMP DEFAULT NOW()
) ENGINE = MyISAM;
