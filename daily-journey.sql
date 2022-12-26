-- --------------------------------------------------------
-- Host:                         localhost
-- Server version:               5.7.33 - MySQL Community Server (GPL)
-- Server OS:                    Win64
-- HeidiSQL Version:             11.2.0.6213
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for daily-journey
DROP DATABASE IF EXISTS `daily-journey`;
CREATE DATABASE IF NOT EXISTS `daily-journey` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `daily-journey`;

-- Dumping structure for table daily-journey.beverages
DROP TABLE IF EXISTS `beverages`;
CREATE TABLE IF NOT EXISTS `beverages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL DEFAULT '',
  `notes` varchar(255) DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `FK_beverages_userid` (`user_id`),
  CONSTRAINT `FK_beverages_userid` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for table daily-journey.beverages: ~0 rows (approximately)
/*!40000 ALTER TABLE `beverages` DISABLE KEYS */;
/*!40000 ALTER TABLE `beverages` ENABLE KEYS */;

-- Dumping structure for table daily-journey.daily_beverages
DROP TABLE IF EXISTS `daily_beverages`;
CREATE TABLE IF NOT EXISTS `daily_beverages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `journey_id` int(11) NOT NULL,
  `beverage_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_dailybeverages_userid` (`user_id`),
  KEY `FK_dailybeverages_journey_id` (`journey_id`),
  KEY `FK_dailybeverages_beverageid` (`beverage_id`),
  CONSTRAINT `FK_dailybeverages_beverageid` FOREIGN KEY (`beverage_id`) REFERENCES `beverages` (`id`),
  CONSTRAINT `FK_dailybeverages_journey_id` FOREIGN KEY (`journey_id`) REFERENCES `journeys` (`id`),
  CONSTRAINT `FK_dailybeverages_userid` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for table daily-journey.daily_beverages: ~0 rows (approximately)
/*!40000 ALTER TABLE `daily_beverages` DISABLE KEYS */;
/*!40000 ALTER TABLE `daily_beverages` ENABLE KEYS */;

-- Dumping structure for table daily-journey.daily_food
DROP TABLE IF EXISTS `daily_food`;
CREATE TABLE IF NOT EXISTS `daily_food` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `journey_id` int(11) NOT NULL,
  `food_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_dailyfood_userid` (`user_id`),
  KEY `FK_dailyfood_journeyid` (`journey_id`),
  KEY `FK_fdailyfood_foodid` (`food_id`),
  CONSTRAINT `FK_dailyfood_journeyid` FOREIGN KEY (`journey_id`) REFERENCES `journeys` (`id`),
  CONSTRAINT `FK_dailyfood_userid` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `FK_fdailyfood_foodid` FOREIGN KEY (`food_id`) REFERENCES `food` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for table daily-journey.daily_food: ~0 rows (approximately)
/*!40000 ALTER TABLE `daily_food` DISABLE KEYS */;
/*!40000 ALTER TABLE `daily_food` ENABLE KEYS */;

-- Dumping structure for table daily-journey.expenses
DROP TABLE IF EXISTS `expenses`;
CREATE TABLE IF NOT EXISTS `expenses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `journey_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `notes` varchar(255) DEFAULT '',
  `amount` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_expeenses_userid` (`user_id`),
  KEY `FK_expenses_journeyid` (`journey_id`),
  CONSTRAINT `FK_expeenses_userid` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `FK_expenses_journeyid` FOREIGN KEY (`journey_id`) REFERENCES `journeys` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for table daily-journey.expenses: ~0 rows (approximately)
/*!40000 ALTER TABLE `expenses` DISABLE KEYS */;
/*!40000 ALTER TABLE `expenses` ENABLE KEYS */;

-- Dumping structure for table daily-journey.food
DROP TABLE IF EXISTS `food`;
CREATE TABLE IF NOT EXISTS `food` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `notes` varchar(255) DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `FK_food_userid` (`user_id`),
  CONSTRAINT `FK_food_userid` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for table daily-journey.food: ~0 rows (approximately)
/*!40000 ALTER TABLE `food` DISABLE KEYS */;
/*!40000 ALTER TABLE `food` ENABLE KEYS */;

-- Dumping structure for table daily-journey.importances
DROP TABLE IF EXISTS `importances`;
CREATE TABLE IF NOT EXISTS `importances` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `journey_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `notes` varchar(255) DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `FK_importances_userid` (`user_id`),
  KEY `FK_importances` (`journey_id`),
  CONSTRAINT `FK_importances` FOREIGN KEY (`journey_id`) REFERENCES `journeys` (`id`),
  CONSTRAINT `FK_importances_userid` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for table daily-journey.importances: ~0 rows (approximately)
/*!40000 ALTER TABLE `importances` DISABLE KEYS */;
/*!40000 ALTER TABLE `importances` ENABLE KEYS */;

-- Dumping structure for table daily-journey.journeys
DROP TABLE IF EXISTS `journeys`;
CREATE TABLE IF NOT EXISTS `journeys` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `mood_id` int(11) NOT NULL,
  `weather_id` int(11) NOT NULL,
  `person_id` int(11) NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_journeys_userid` (`user_id`),
  KEY `FK_journeys_moodid` (`mood_id`),
  KEY `FK_journeys_personid` (`person_id`),
  KEY `FK_journeys_weathers` (`weather_id`),
  CONSTRAINT `FK_journeys_moodid` FOREIGN KEY (`mood_id`) REFERENCES `moods` (`id`),
  CONSTRAINT `FK_journeys_personid` FOREIGN KEY (`person_id`) REFERENCES `people` (`id`),
  CONSTRAINT `FK_journeys_userid` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `FK_journeys_weathers` FOREIGN KEY (`weather_id`) REFERENCES `weathers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for table daily-journey.journeys: ~0 rows (approximately)
/*!40000 ALTER TABLE `journeys` DISABLE KEYS */;
/*!40000 ALTER TABLE `journeys` ENABLE KEYS */;

-- Dumping structure for table daily-journey.moods
DROP TABLE IF EXISTS `moods`;
CREATE TABLE IF NOT EXISTS `moods` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `notes` varchar(255) DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `FK_moods_userid` (`user_id`),
  CONSTRAINT `FK_moods_userid` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for table daily-journey.moods: ~0 rows (approximately)
/*!40000 ALTER TABLE `moods` DISABLE KEYS */;
/*!40000 ALTER TABLE `moods` ENABLE KEYS */;

-- Dumping structure for table daily-journey.people
DROP TABLE IF EXISTS `people`;
CREATE TABLE IF NOT EXISTS `people` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `notes` varchar(255) DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `FK_people_userid` (`user_id`),
  CONSTRAINT `FK_people_userid` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for table daily-journey.people: ~0 rows (approximately)
/*!40000 ALTER TABLE `people` DISABLE KEYS */;
/*!40000 ALTER TABLE `people` ENABLE KEYS */;

-- Dumping structure for table daily-journey.users
DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for table daily-journey.users: ~0 rows (approximately)
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
/*!40000 ALTER TABLE `users` ENABLE KEYS */;

-- Dumping structure for table daily-journey.weathers
DROP TABLE IF EXISTS `weathers`;
CREATE TABLE IF NOT EXISTS `weathers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `notes` varchar(255) DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `FK_weathers_userid` (`user_id`),
  CONSTRAINT `FK_weathers_userid` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for table daily-journey.weathers: ~0 rows (approximately)
/*!40000 ALTER TABLE `weathers` DISABLE KEYS */;
/*!40000 ALTER TABLE `weathers` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
