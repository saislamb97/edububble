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
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('7rbm1253iqni1u3oynk3ftua91vs0y7f','.eJxVjDEOAiEQRe9CbQg4wriW9p6BDMMgqwaSZbcy3t2QbKHtf-_9twq0rSVsXZYwJ3VRVh1-t0j8lDpAelC9N82trssc9VD0Tru-tSSv6-7-HRTqZdSQ_Tm7I6IQg6WJPSc0mPMpRkBjyLpMABNbyGIdCydGRIjOAztRny_71ziS:1rB7fe:J5gew573c2ssbrv59rVWO-EJwgdAW_2RzOD-9RGeuwE','2023-12-21 06:15:38.862692'),('9ksko3r16pf9som1v4he10h42tyq6zra','.eJxVjDEOAiEQRe9CbQg4wriW9p6BDMMgqwaSZbcy3t2QbKHtf-_9twq0rSVsXZYwJ3VRVh1-t0j8lDpAelC9N82trssc9VD0Tru-tSSv6-7-HRTqZdSQ_Tm7I6IQg6WJPSc0mPMpRkBjyLpMABNbyGIdCydGRIjOAztRny_71ziS:1rI2z8:CzZBu1UIT1J3GHfnj03XsNjEA9Op259rVjqdo74ABR4','2024-01-09 08:40:22.612236'),('p48ae0lw063onu2m8fhiibrb2p35hawk','.eJxVjDEOAiEQRe9CbQg4wriW9p6BDMMgqwaSZbcy3t2QbKHtf-_9twq0rSVsXZYwJ3VRVh1-t0j8lDpAelC9N82trssc9VD0Tru-tSSv6-7-HRTqZdSQ_Tm7I6IQg6WJPSc0mPMpRkBjyLpMABNbyGIdCydGRIjOAztRny_71ziS:1rFmaB:FVRh4p5sDGyun869ayjXKCREMimachQinkMn8gIbMoU','2024-01-03 02:45:15.588702'),('sp2937rwm3chl8ydz8un02k2jh9dwbhz','.eJxVjDEOAiEQRe9CbQg4wriW9p6BDMMgqwaSZbcy3t2QbKHtf-_9twq0rSVsXZYwJ3VRVh1-t0j8lDpAelC9N82trssc9VD0Tru-tSSv6-7-HRTqZdSQ_Tm7I6IQg6WJPSc0mPMpRkBjyLpMABNbyGIdCydGRIjOAztRny_71ziS:1rIK5P:je0iSmq6wYqiGTbhJFH-z8TTkGkiPyzrd9CgelnehsU','2024-01-10 02:55:59.947102'),('ucapgt5cdj6sxixz09tdlh36cgxpupau','.eJxVjDEOAiEQRe9CbQg4wriW9p6BDMMgqwaSZbcy3t2QbKHtf-_9twq0rSVsXZYwJ3VRVh1-t0j8lDpAelC9N82trssc9VD0Tru-tSSv6-7-HRTqZdSQ_Tm7I6IQg6WJPSc0mPMpRkBjyLpMABNbyGIdCydGRIjOAztRny_71ziS:1rHzKy:piCeRnP_s5wKx26iazVSAOIGPQbRri5CJniB26pbZwA','2024-01-09 04:46:40.743302');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-27 11:31:56
