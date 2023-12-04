-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: edububble
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `homeapp_textbookstatus`
--

DROP TABLE IF EXISTS `homeapp_textbookstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `homeapp_textbookstatus` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `collected` tinyint(1) NOT NULL,
  `returned` tinyint(1) NOT NULL,
  `student_id` bigint NOT NULL,
  `textbook_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `homeapp_textbookstat_student_id_020b62fe_fk_homeapp_s` (`student_id`),
  KEY `homeapp_textbookstat_textbook_id_81b5d78b_fk_homeapp_t` (`textbook_id`),
  CONSTRAINT `homeapp_textbookstat_student_id_020b62fe_fk_homeapp_s` FOREIGN KEY (`student_id`) REFERENCES `homeapp_students` (`id`),
  CONSTRAINT `homeapp_textbookstat_textbook_id_81b5d78b_fk_homeapp_t` FOREIGN KEY (`textbook_id`) REFERENCES `homeapp_textbooks` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `homeapp_textbookstatus`
--

LOCK TABLES `homeapp_textbookstatus` WRITE;
/*!40000 ALTER TABLE `homeapp_textbookstatus` DISABLE KEYS */;
INSERT INTO `homeapp_textbookstatus` VALUES (1,1,0,1,1);
/*!40000 ALTER TABLE `homeapp_textbookstatus` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-04 22:11:12
