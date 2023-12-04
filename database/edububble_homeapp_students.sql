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
-- Table structure for table `homeapp_students`
--

DROP TABLE IF EXISTS `homeapp_students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `homeapp_students` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `student_id` varchar(250) NOT NULL,
  `section` varchar(250) DEFAULT NULL,
  `classname_id` bigint DEFAULT NULL,
  `username_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `student_id` (`student_id`),
  KEY `homeapp_students_username_id_56e51e4d_fk_homeapp_user_id` (`username_id`),
  KEY `homeapp_students_classname_id_591ecdc2_fk_homeapp_classname_id` (`classname_id`),
  CONSTRAINT `homeapp_students_classname_id_591ecdc2_fk_homeapp_classname_id` FOREIGN KEY (`classname_id`) REFERENCES `homeapp_classname` (`id`),
  CONSTRAINT `homeapp_students_username_id_56e51e4d_fk_homeapp_user_id` FOREIGN KEY (`username_id`) REFERENCES `homeapp_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `homeapp_students`
--

LOCK TABLES `homeapp_students` WRITE;
/*!40000 ALTER TABLE `homeapp_students` DISABLE KEYS */;
INSERT INTO `homeapp_students` VALUES (1,'563164','EXA',1,2);
/*!40000 ALTER TABLE `homeapp_students` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-04 21:44:41
