


drop table if exists employee_tax_info;

CREATE TABLE employee_tax_info (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  person_id INT (4),
  married boolean not null,
  allowances INT not null default 1,
  nominal_scale float not null default 0,
  created TIMESTAMP DEFAULT NOW(),
  updated TIMESTAMP DEFAULT 0,
  FOREIGN KEY (person_id) REFERENCES person(id) ON DELETE CASCADE,
  UNIQUE KEY(person_id)
) ENGINE = MyISAM;

