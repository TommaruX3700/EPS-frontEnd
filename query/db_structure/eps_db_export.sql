-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Creato il: Mag 30, 2024 alle 16:41
-- Versione del server: 10.4.32-MariaDB
-- Versione PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `eps`
--

DELIMITER $$
--
-- Procedure
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `procedura1` (`param1` INT, `param2` CHAR(3), OUT `param3` INT)   BEGIN
        DECLARE finito INT default 0;
        DECLARE a INT;
        DECLARE b CHAR(50);
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Struttura della tabella `pacchi`
--

CREATE TABLE `pacchi` (
  `id` int(11) NOT NULL,
  `ID_PACCO` int(255) NOT NULL,
  `CODICE_PALLET` int(255) DEFAULT NULL,
  `NUM_SPEDIZIONE` int(255) DEFAULT NULL,
  `CODICE_CLIENTE` int(255) DEFAULT NULL,
  `PESO_NETTO` varchar(255) DEFAULT NULL,
  `PESO_LORDO` varchar(255) DEFAULT NULL,
  `BASE_MAGGIORE` int(255) DEFAULT NULL,
  `BASE_MINORE` int(255) DEFAULT NULL,
  `ALTEZZA` int(255) DEFAULT NULL,
  `FLAG_PALLETTIZZABILE` char(255) DEFAULT NULL,
  `FLAG_SOVRAPPONIBILE` char(255) DEFAULT NULL,
  `FLAG_RUOTABILE` char(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `pacchi`
--

INSERT INTO `pacchi` (`id`, `ID_PACCO`, `CODICE_PALLET`, `NUM_SPEDIZIONE`, `CODICE_CLIENTE`, `PESO_NETTO`, `PESO_LORDO`, `BASE_MAGGIORE`, `BASE_MINORE`, `ALTEZZA`, `FLAG_PALLETTIZZABILE`, `FLAG_SOVRAPPONIBILE`, `FLAG_RUOTABILE`) VALUES
(1, 1532, 10, 1212, 454, '12', '55', 15, 82, 22, 'N', '', ''),
(2, 5425, 10, 1235, 444, '13', '54', 52, 65, 33, '', 'N', ''),
(3, 5454, NULL, 4456, 666, '15', '54', 56, 23, 55, 'N', '', ''),
(4, 65, NULL, 747, 127, '76', '33', 97, 7, 173, ' \'', ' \'', ' \''),
(5, 92, NULL, 672, 120, '98', '98', 67, 94, 131, ' \'', ' \'', ' \''),
(6, 42, NULL, 174, 926, '98', '53', 48, 143, 185, ' \'', ' \'', ' \''),
(7, 47, NULL, 292, 151, '73', '42', 177, 65, 101, ' \'', ' \'', ' \''),
(8, 67, NULL, 102, 23, '56', '100', 199, 18, 67, ' \'', ' \'', ' \''),
(9, 16, NULL, 229, 828, '18', '87', 195, 180, 110, ' \'', ' \'', ' \''),
(10, 43, NULL, 865, 690, '94', '11', 1, 98, 104, ' \'', ' \'', ' \''),
(11, 99, NULL, 68, 123, '51', '63', 58, 6, 59, '', 'N', 'N'),
(12, 23, NULL, 545, 482, '8', '41', 89, 81, 122, 'N', 'N', ''),
(13, 54, NULL, 17, 298, '9', '27', 187, 35, 30, '', '', 'N'),
(15, 90, NULL, 344, 270, '32', '27', 113, 6, 142, 'N', '', ''),
(16, 80, NULL, 37, 784, '61', '14', 95, 15, 20, '', 'N', 'N'),
(17, 30, NULL, 485, 205, '45', '40', 17, 78, 150, '', '', 'N'),
(18, 39, NULL, 882, 1, '82', '50', 172, 136, 18, 'N', '', 'N'),
(19, 17, NULL, 569, 944, '22', '69', 26, 154, 190, 'N', '', ''),
(20, 49, NULL, 968, 960, '52', '7', 171, 166, 14, '', 'N', ''),
(21, 51, NULL, 301, 678, '45', '96', 70, 168, 21, 'N', '', 'N'),
(22, 63, 10, 326, 168, '31', '16', 42, 17, 176, 'N', 'N', ''),
(23, 4, NULL, 35, 279, '97', '80', 29, 16, 19, 'N', '', ''),
(24, 5, NULL, 580, 39, '37', '40', 72, 142, 199, '', '', 'N'),
(25, 68, NULL, 173, 941, '34', '36', 131, 74, 116, 'N', 'N', ''),
(28, 38, NULL, 544, 772, '32', '29', 39, 77, 122, 'N', '', 'N'),
(30, 74, NULL, 445, 463, '58', '85', 197, 164, 152, 'N', 'N', 'N'),
(31, 60, NULL, 982, 120, '58', '72', 66, 156, 61, 'N', 'N', 'N'),
(32, 73, NULL, 33, 630, '10', '93', 124, 137, 145, '', 'N', ''),
(33, 35, NULL, 458, 616, '11', '42', 126, 190, 170, '', 'N', 'N'),
(34, 32, NULL, 505, 459, '84', '6', 183, 16, 129, '', 'N', ''),
(35, 31, NULL, 545, 439, '41', '91', 152, 58, 175, 'N', 'N', ''),
(36, 77, NULL, 985, 653, '4', '42', 192, 150, 77, '', 'N', ''),
(38, 84, NULL, 374, 913, '48', '2', 145, 19, 23, 'N', 'N', ''),
(39, 85, NULL, 133, 201, '94', '10', 184, 70, 189, 'N', '', 'N'),
(40, 72, NULL, 538, 139, '68', '19', 84, 133, 124, '', 'N', ''),
(41, 46, NULL, 16, 677, '70', '96', 153, 107, 119, 'N', '', 'N'),
(43, 78, NULL, 385, 770, '40', '23', 96, 147, 156, 'N', '', ''),
(45, 62, NULL, 852, 968, '83', '56', 30, 107, 138, '', 'N', 'N'),
(46, 44, NULL, 433, 394, '37', '88', 87, 55, 51, '', 'N', 'N'),
(47, 9, NULL, 530, 419, '28', '82', 145, 75, 146, 'N', 'N', 'N'),
(48, 98, NULL, 456, 626, '85', '69', 40, 12, 39, 'N', 'N', ''),
(49, 6, NULL, 742, 741, '82', '7', 19, 144, 151, 'N', '', 'N'),
(50, 88, NULL, 175, 93, '9', '73', 125, 113, 111, '', '', 'N'),
(51, 40, NULL, 283, 971, '13', '61', 124, 83, 119, 'N', 'N', 'N'),
(52, 27, NULL, 660, 232, '99', '21', 19, 187, 191, 'N', '', 'N'),
(53, 100, NULL, 593, 470, '59', '63', 80, 95, 139, 'N', '', 'N'),
(54, 36, NULL, 682, 598, '36', '68', 121, 93, 133, '', 'N', ''),
(55, 61, NULL, 747, 278, '65', '94', 43, 160, 11, 'N', 'N', ''),
(56, 10, NULL, 189, 165, '28', '84', 176, 37, 72, '', 'N', ''),
(57, 76, NULL, 894, 58, '6', '53', 75, 127, 90, '', 'N', 'N'),
(58, 81, NULL, 522, 117, '11', '66', 127, 57, 194, 'N', '', 'N'),
(59, 52, NULL, 318, 834, '22', '96', 3, 200, 22, 'N', '', ''),
(60, 37, NULL, 710, 167, '21', '50', 56, 81, 97, '', 'N', ''),
(61, 57, NULL, 506, 420, '75', '74', 12, 107, 67, '', 'N', 'N');

-- --------------------------------------------------------

--
-- Struttura della tabella `pallet`
--

CREATE TABLE `pallet` (
  `CODICE_PALLET` int(255) NOT NULL,
  `DIM_X_PALLET` int(255) DEFAULT NULL,
  `DIM_Y_PALLET` int(255) DEFAULT NULL,
  `DIM_Z_PALLET` int(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `pallet`
--

INSERT INTO `pallet` (`CODICE_PALLET`, `DIM_X_PALLET`, `DIM_Y_PALLET`, `DIM_Z_PALLET`) VALUES
(10, 1000, 500, 200),
(15, 600, 500, 200),
(125, NULL, NULL, NULL);

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `pacchi`
--
ALTER TABLE `pacchi`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ID_PACCO` (`ID_PACCO`),
  ADD KEY `CODICE_PALLET` (`CODICE_PALLET`);

--
-- Indici per le tabelle `pallet`
--
ALTER TABLE `pallet`
  ADD PRIMARY KEY (`CODICE_PALLET`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `pacchi`
--
ALTER TABLE `pacchi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=62;

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `pacchi`
--
ALTER TABLE `pacchi`
  ADD CONSTRAINT `pacchi_ibfk_1` FOREIGN KEY (`CODICE_PALLET`) REFERENCES `pallet` (`CODICE_PALLET`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
