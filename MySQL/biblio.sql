-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Erstellungszeit: 30. Apr 2020 um 17:30
-- Server-Version: 10.4.11-MariaDB
-- PHP-Version: 7.4.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `biblio`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `ausleihe`
--

CREATE TABLE `ausleihe` (
  `id` int(11) NOT NULL,
  `medium_id` int(11) NOT NULL,
  `leser_id` int(11) NOT NULL,
  `dat_ausleihe` date NOT NULL,
  `dat_letzte_verlaeng` date NOT NULL,
  `dat_rueckgabe` date NOT NULL,
  `kz_beanstandet` char(1) NOT NULL DEFAULT '',
  `kz_zurueckgegeben` char(1) NOT NULL DEFAULT '',
  `ts_last_update` datetime DEFAULT NULL,
  `ts_created` datetime DEFAULT NULL,
  `ts_upd_internal` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `kategorie`
--

CREATE TABLE `kategorie` (
  `id` smallint(6) NOT NULL,
  `kategorie_bez` varchar(30) DEFAULT NULL,
  `ts_last_update` datetime DEFAULT NULL,
  `ts_created` datetime DEFAULT NULL,
  `ts_upd_internal` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Daten für Tabelle `kategorie`
--

INSERT INTO `kategorie` (`id`, `kategorie_bez`, `ts_last_update`, `ts_created`, `ts_upd_internal`) VALUES
(1, 'Sachbuch', '2020-03-31 12:03:13', '2020-03-31 12:03:13', '2020-03-31 10:03:13'),
(2, 'Belletristik', '2020-03-31 12:03:30', '2020-03-31 12:03:30', '2020-03-31 10:03:30'),
(3, 'Audio CD: Klassische Musik', '2020-04-30 13:59:01', '2020-04-30 13:59:01', '2020-04-30 11:59:01'),
(4, 'Audio: sonstige Musik', '2020-04-30 14:00:03', '2020-04-30 14:00:03', '2020-04-30 12:00:03'),
(5, 'Hörbuch', '2020-04-30 14:00:49', '2020-04-30 14:00:49', '2020-04-30 12:00:49'),
(6, 'Sachfilm, Dokumentation', '2020-04-30 14:01:53', '2020-04-30 14:01:53', '2020-04-30 12:01:53'),
(7, 'Unterhaltungsfilm', '2020-04-30 14:02:14', '2020-04-30 14:02:14', '2020-04-30 12:02:14');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `leser`
--

CREATE TABLE `leser` (
  `id` int(11) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `vorname` varchar(50) DEFAULT NULL,
  `anrede` varchar(20) DEFAULT NULL,
  `titel` varchar(30) DEFAULT NULL,
  `adr_ort` varchar(50) DEFAULT NULL,
  `adr_plz` varchar(20) DEFAULT NULL,
  `adr_str` varchar(50) DEFAULT NULL,
  `adr_zusatz` varchar(50) DEFAULT NULL,
  `adr_land` varchar(50) DEFAULT NULL,
  `mailadresse` varchar(100) DEFAULT NULL,
  `kz_aktiv` char(1) NOT NULL DEFAULT '',
  `kz_gesperrt` char(1) NOT NULL DEFAULT '',
  `ts_last_update` datetime DEFAULT NULL,
  `ts_created` datetime DEFAULT NULL,
  `ts_upd_internal` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `medientyp`
--

CREATE TABLE `medientyp` (
  `id` smallint(6) NOT NULL,
  `medientyp_bez` varchar(30) DEFAULT NULL,
  `ts_last_update` datetime DEFAULT NULL,
  `ts_created` datetime DEFAULT NULL,
  `ts_upd_internal` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Daten für Tabelle `medientyp`
--

INSERT INTO `medientyp` (`id`, `medientyp_bez`, `ts_last_update`, `ts_created`, `ts_upd_internal`) VALUES
(1, 'Buch', '2020-03-31 11:52:25', '2020-03-31 11:52:25', '2020-03-31 09:52:25'),
(2, 'E-Book', '2020-03-31 11:52:59', '2020-03-31 11:52:59', '2020-03-31 09:52:59'),
(3, 'Audio CD', '2020-03-31 11:53:18', '2020-03-31 11:53:18', '2020-03-31 09:53:18'),
(4, 'Video DVD', '2020-03-31 11:53:35', '2020-03-31 11:53:35', '2020-03-31 09:53:35');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `medium`
--

CREATE TABLE `medium` (
  `id` int(11) NOT NULL,
  `titel` varchar(255) DEFAULT NULL,
  `verfasser` varchar(255) DEFAULT NULL,
  `medientyp` smallint(6) DEFAULT NULL,
  `kategorie` smallint(6) DEFAULT NULL,
  `signatur` varchar(10) DEFAULT NULL,
  `erscheinungsdatum` date DEFAULT NULL,
  `auflage` smallint(6) DEFAULT NULL,
  `verlag` varchar(255) DEFAULT NULL,
  `einstandspreis` decimal(7,2) DEFAULT NULL,
  `anschaffungsdatum` date DEFAULT NULL,
  `inhalt` text DEFAULT NULL,
  `anmerkung` text DEFAULT NULL,
  `ts_last_update` datetime DEFAULT NULL,
  `ts_created` datetime DEFAULT NULL,
  `ts_upd_internal` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Daten für Tabelle `medium`
--

INSERT INTO `medium` (`id`, `titel`, `verfasser`, `medientyp`, `kategorie`, `signatur`, `erscheinungsdatum`, `auflage`, `verlag`, `einstandspreis`, `anschaffungsdatum`, `inhalt`, `anmerkung`, `ts_last_update`, `ts_created`, `ts_upd_internal`) VALUES
(1, 'Four Lions', 'Morris, Chris', 3, 8, 'asd-ff', '1998-01-31', 1, 'Capelight', '9.95', '2001-02-18', 'www', 'qqq', '2020-04-30 13:48:08', '2020-03-30 23:51:45', '2020-04-30 11:48:08'),
(2, 'Python - Der Grundkurs', 'Kofler, Michael', 1, 1, 'Edv Py3', '2019-11-01', 1, 'Rheinwerk Computing', '14.90', '2019-11-01', 'kompakte Einführung', 'übersichtliche, brauchbare Einführung', '2020-04-14 22:25:26', '2020-04-06 22:41:50', '2020-04-30 12:08:59'),
(3, 'Krieg und Frieden', 'Tolstoy, Lew', 1, 2, 'aaa-bbb', '1899-09-12', 34, '', '35.00', '2020-02-08', '', 'das Buch ist ziemlich lang', '2020-04-30 14:30:46', '2020-03-31 11:24:42', '2020-04-30 12:30:46'),
(7, 'test', NULL, 1, 2, 'sssss', NULL, NULL, NULL, '0.00', NULL, NULL, NULL, '2020-04-27 00:45:14', '2020-04-27 00:45:14', '2020-04-26 22:45:14'),
(8, 'Schuld und Sühne', 'Dostojewski, Fjodor Michailowitsch', 1, 2, 'Aaa 2', '1866-07-15', 98, 'Izdatelstwo predstupljenija', '38.95', '1995-12-18', NULL, NULL, '2020-04-30 14:22:29', '2020-04-30 14:22:29', '2020-04-30 12:22:29'),
(9, 'Bednaja Lisa', 'Karamsin, Nikolaj', 1, 2, 'Aaa 23', '1792-01-01', 24, 'Vorobjey', '9.95', '1990-07-01', NULL, NULL, '2020-04-30 14:26:43', '2020-04-30 14:26:43', '2020-04-30 12:26:43');

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `ausleihe`
--
ALTER TABLE `ausleihe`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `kategorie`
--
ALTER TABLE `kategorie`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `leser`
--
ALTER TABLE `leser`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `medientyp`
--
ALTER TABLE `medientyp`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `medium`
--
ALTER TABLE `medium`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `ausleihe`
--
ALTER TABLE `ausleihe`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `kategorie`
--
ALTER TABLE `kategorie`
  MODIFY `id` smallint(6) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT für Tabelle `leser`
--
ALTER TABLE `leser`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `medientyp`
--
ALTER TABLE `medientyp`
  MODIFY `id` smallint(6) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT für Tabelle `medium`
--
ALTER TABLE `medium`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
