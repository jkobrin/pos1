drop table if exists server_receipts;

CREATE TABLE server_receipts(
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  dat date not null,
  person_id INT not null,
  cctotal float default null,
  cctips float default null,
  cash_drop float default null,
  starting_cash float default null,
  cash_left_in_bank float default null,
  created TIMESTAMP DEFAULT NOW(),
  INDEX person_idx_receipts (person_id),
  FOREIGN KEY (person_id) REFERENCES person(id) ON DELETE CASCADE
) ENGINE = MyISAM;
