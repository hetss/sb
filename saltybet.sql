CREATE TABLE IF NOT EXISTS `fighter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(50) NOT NULL,
  `tier` char(1) NOT NULL,
  `stats` int(11) NOT NULL,
  `fights` int(11) NOT NULL DEFAULT '0',
  `wins` int(11) NOT NULL DEFAULT '0',
  `losses` int(11) NOT NULL DEFAULT '0',
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `active_match` (
  `id` int(11) NOT NULL DEFAULT '1',
  `fighter1` int(11) NOT NULL DEFAULT '1',
  `fighter2` int(11) NOT NULL DEFAULT '1',
  `tournament` tinyint(1) NOT NULL DEFAULT '0',
  `open` timestamp NULL DEFAULT NULL,
  `modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_fighter1` (`fighter1`),
  KEY `fk_fighter2` (`fighter2`),
  CONSTRAINT `fk_fighter1` FOREIGN KEY (`fighter1`) REFERENCES `fighter` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_fighter2` FOREIGN KEY (`fighter2`) REFERENCES `fighter` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `balance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `balance` int(11) NOT NULL,
  `tournament` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `balance2` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `balance` int(11) NOT NULL,
  `tournament` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

CREATE TABLE IF NOT EXISTS `event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fighter` int(11) NOT NULL,
  `description` text NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_fighter` (`fighter`),
  CONSTRAINT `fk_fighter` FOREIGN KEY (`fighter`) REFERENCES `fighter` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag` char(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tag` (`tag`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `fighter-tags` (
  `fighter` int(11) NOT NULL,
  `tag` int(11) NOT NULL,
  KEY `FK__tags` (`tag`),
  KEY `fighter` (`fighter`),
  CONSTRAINT `FK__tags` FOREIGN KEY (`tag`) REFERENCES `tags` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fighter` FOREIGN KEY (`fighter`) REFERENCES `fighter` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `match` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fighter1` int(11) NOT NULL DEFAULT '0',
  `fighter2` int(11) NOT NULL DEFAULT '0',
  `bet1` int(11) NOT NULL,
  `bet2` int(11) NOT NULL,
  `winner` int(11) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fighter1` (`fighter1`),
  KEY `fighter2` (`fighter2`),
  KEY `winner` (`winner`),
  CONSTRAINT `fighter1` FOREIGN KEY (`fighter1`) REFERENCES `fighter` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fighter2` FOREIGN KEY (`fighter2`) REFERENCES `fighter` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `winner` FOREIGN KEY (`winner`) REFERENCES `fighter` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;