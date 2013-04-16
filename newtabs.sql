/*REM DROP TABLE IF EXISTS `bevinventory`;*/
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
/*
CREATE TABLE `bevinventory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item_name` varchar(32) NOT NULL,
  `created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `units` int(4) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1008 DEFAULT CHARSET=latin1;
*/

DROP TABLE IF EXISTS winelist;
CREATE TABLE winelist (
  id int NOT NULL AUTO_INCREMENT,
  category varchar(32),
  bin varchar(4),
  listorder int,
  byline varchar(128),
  name varchar(64),
  qtprice int,
  frontprice float,
  mynotes varchar(256),
  grapes varchar(64),
  supplier varchar(64),
  notes varchar(512),
  listprice int,
  active boolean default true,
  units_in_stock int(4) DEFAULT '0',
  inventory_date date default 0,
  PRIMARY KEY (`id`)
)ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
