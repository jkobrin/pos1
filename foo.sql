drop table if exists receipts_by_server;

CREATE TABLE receipts_by_server (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  person_id INT not null,
  dat date not null,
  cc1 float,
  cc2 float,
  cash1 float,
  cash2 float,
  INDEX rbs_person_id (person_id),
  INDEX rbs_dat (dat),
  FOREIGN KEY (person_id) REFERENCES person(id) ON DELETE CASCADE
)
ENGINE= MyISAM;

