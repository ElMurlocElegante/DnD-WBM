-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 06-06-2024 a las 05:22:09
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `DnD-WBM`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `characters`
--

CREATE TABLE `characters` (
  `username` varchar(40) NOT NULL,
  `character_name` varchar(40) NOT NULL,
  `class` varchar(9) NOT NULL,
  `subclass` varchar(16) DEFAULT NULL,
  `background` varchar(20) NOT NULL,
  `race` varchar(16) NOT NULL,
  `alignment` varchar(16) NOT NULL,
  `xp` mediumint(6) NOT NULL,
  `hp` smallint(3) NOT NULL,
  `strength` tinyint(2) NOT NULL,
  `dexterity` tinyint(2) NOT NULL,
  `constitution` tinyint(2) NOT NULL,
  `intelligence` tinyint(2) NOT NULL,
  `wisdom` tinyint(2) NOT NULL,
  `charisma` tinyint(2) NOT NULL,
  `proficiency_skills` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT 'Tratar como JSON, MariaDB utiliza longtext como referencia',
  `proficiency_n_languange` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT 'Tratar como JSON, MariaDB utiliza longtext como referencia',
  `equipment` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT 'Tratar como JSON, MariaDB utiliza longtext como referencia',
  `lore` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT 'Tratar como JSON, MariaDB utiliza longtext como referencia',
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` smallint(5) UNSIGNED NOT NULL,
  `username` varchar(40) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` char(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`) VALUES
(1, 'DMatias', 'dejeanmatias@gmail.com', '314159'),
(2, 'martinam', '', 'martina'),
(3, 'manolo', 'mdejean@fi.uba.ar', '123456'),
(6, 'juan', 'dejean@AA', '123456'),
(7, 'mateo', 'matiasdejeangonzalez@gmail.com', '123456'),
(8, 'diego', 'd2g6cnba@gmail.com', '123qwe'),
(9, 'tobias', 'jdsahjas@gmail.com', '123456');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `characters`
--
ALTER TABLE `characters`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `characters`
--
ALTER TABLE `characters`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` smallint(5) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
