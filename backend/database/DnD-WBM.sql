-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: May 28, 2024 at 07:07 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `DnD-WBM`
--

-- Table structure for table `characters`
CREATE TABLE `characters` (
  `username` varchar(40) NOT NULL,
  `character_name` varchar(40) NOT NULL,
  `class` varchar(15) NOT NULL,
  `subclass` varchar(32) DEFAULT NULL,
  `background` varchar(20) NOT NULL,
  `race` varchar(16) NOT NULL,
  `alignment` varchar(16) NOT NULL,
  `xp` mediumint(6) NOT NULL,
  `hp` smallint(3) NOT NULL,
  `ac` smallint(3) NOT NULL,
  `strength` tinyint(2) NOT NULL,
  `dexterity` tinyint(2) NOT NULL,
  `constitution` tinyint(2) NOT NULL,
  `intelligence` tinyint(2) NOT NULL,
  `wisdom` tinyint(2) NOT NULL,
  `charisma` tinyint(2) NOT NULL,
  `proficiency_skills` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT 'Tratar como JSON, MariaDB utiliza longtext como referencia',
  `proficiency_n_language` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT 'Tratar como JSON, MariaDB utiliza longtext como referencia',
  `equipment` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT 'Tratar como JSON, MariaDB utiliza longtext como referencia',
  `lore` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT 'Tratar como JSON, MariaDB utiliza longtext como referencia',
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Table structure for table `users`
CREATE TABLE `users` (
  `username` varchar(40) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(24) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Estructura de tabla para la tabla `rooms`

CREATE TABLE `rooms` (
  `room_creator` varchar(20) NOT NULL,
  `room_name` varchar(20) NOT NULL,
  `ingame` int(11) NOT NULL,
  `maxplayers` int(11) NOT NULL,
  `code` varchar(4) NOT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
