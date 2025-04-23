-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: mysql
-- Generation Time: Feb 25, 2025 at 11:26 AM
-- Server version: 9.2.0
-- PHP Version: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `web`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`%` PROCEDURE `get_users` ()   SELECT * FROM users$$

CREATE DEFINER=`root`@`%` PROCEDURE `get_users_by_name` (IN `name` VARCHAR(20))   SELECT * FROM users WHERE user_name = name$$

CREATE DEFINER=`root`@`%` PROCEDURE `users_by_name_and_last_name` (IN `name` VARCHAR(20), IN `last_name` VARCHAR(20))   SELECT * FROM users WHERE user_name = name AND user_last_name = last_name$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Stand-in structure for view `get_users_with_phones`
-- (See below for the actual view)
--
CREATE TABLE `get_users_with_phones` (
`user_pk` bigint unsigned
,`user_name` varchar(20)
,`phones` text
);

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `post_pk` bigint UNSIGNED NOT NULL,
  `post_data` varchar(500) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`post_pk`, `post_data`) VALUES
(1, 'Post from A'),
(2, 'Post from B');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_pk` bigint UNSIGNED NOT NULL,
  `user_username` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `user_name` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `user_last_name` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `user_email` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `user_password` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `user_created_at` bigint UNSIGNED NOT NULL,
  `user_updated_at` bigint UNSIGNED NOT NULL DEFAULT '0',
  `user_deleted_at` bigint UNSIGNED NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_pk`, `user_username`, `user_name`, `user_last_name`, `user_email`, `user_password`, `user_created_at`, `user_updated_at`, `user_deleted_at`) VALUES
(1, '', 'Sa', 'Do', 'a@a.com', 'scrypt:32768:8:1$Whz964jkeO8RYZno$92f77133c7b1fc6cb1ca3975908a4fa255b0e67af4f7e2c3e58f3faa46058031339c6007fee16479a8087e900c8a5f912ada679c4e01420cacc9d929376858bb', 1740477137, 0, 0),
(8, 'santiago', 'sa', 'do', 'sa@do.com', 'scrypt:32768:8:1$AnzqOsPaGEKsAstq$b18fd8111f02a6a6e18d110728e401640a1740fed877267d3df794dbcefbe59322cffe39e3bc1bf9c92534423c69b7d50e18627cdefddde3654a1842df9d83d8', 1740479110, 0, 0),
(11, 'xxxxxx', 'John', 'Doe', 'mari@sdd.com', 'scrypt:32768:8:1$6objM2mb0hODHnYj$a9504eac4d1085e4f0aed209d1d74e1c18235a3c17ddb8d9d8307ab5f7b4648e07cac6786269f65c2e5e0d0179cc0beeb590d4b8b517cb005272e6edd73636c9', 1740482734, 0, 0);

--
-- Triggers `users`
--
DELIMITER $$
CREATE TRIGGER `update_user` BEFORE UPDATE ON `users` FOR EACH ROW SET NEW.user_updated_at = NOW()
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `users_phones`
--

CREATE TABLE `users_phones` (
  `user_fk` bigint UNSIGNED NOT NULL,
  `user_phone` char(8) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users_phones`
--

INSERT INTO `users_phones` (`user_fk`, `user_phone`) VALUES
(1, '111'),
(1, '112'),
(2, '222');

-- --------------------------------------------------------

--
-- Table structure for table `users__posts`
--

CREATE TABLE `users__posts` (
  `user_fk` bigint UNSIGNED NOT NULL,
  `post_fk` bigint UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users__posts`
--

INSERT INTO `users__posts` (`user_fk`, `post_fk`) VALUES
(1, 1),
(2, 2);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`post_pk`),
  ADD UNIQUE KEY `post_pk` (`post_pk`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_pk`),
  ADD UNIQUE KEY `user_pk` (`user_pk`),
  ADD UNIQUE KEY `user_email` (`user_email`),
  ADD UNIQUE KEY `user_username` (`user_username`);

--
-- Indexes for table `users_phones`
--
ALTER TABLE `users_phones`
  ADD PRIMARY KEY (`user_fk`,`user_phone`);

--
-- Indexes for table `users__posts`
--
ALTER TABLE `users__posts`
  ADD PRIMARY KEY (`user_fk`,`post_fk`),
  ADD KEY `post_fk` (`post_fk`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `posts`
--
ALTER TABLE `posts`
  MODIFY `post_pk` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_pk` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

-- --------------------------------------------------------

--
-- Structure for view `get_users_with_phones`
--
DROP TABLE IF EXISTS `get_users_with_phones`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `get_users_with_phones`  AS SELECT `u`.`user_pk` AS `user_pk`, `u`.`user_name` AS `user_name`, group_concat(`p`.`user_phone` order by `p`.`user_phone` ASC separator ',') AS `phones` FROM (`users` `u` left join `users_phones` `p` on((`u`.`user_pk` = `p`.`user_fk`))) GROUP BY `u`.`user_pk` ;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `users_phones`
--
ALTER TABLE `users_phones`
  ADD CONSTRAINT `users_phones_ibfk_1` FOREIGN KEY (`user_fk`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE ON UPDATE RESTRICT;

--
-- Constraints for table `users__posts`
--
ALTER TABLE `users__posts`
  ADD CONSTRAINT `users__posts_ibfk_1` FOREIGN KEY (`user_fk`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE ON UPDATE RESTRICT,
  ADD CONSTRAINT `users__posts_ibfk_2` FOREIGN KEY (`post_fk`) REFERENCES `posts` (`post_pk`) ON DELETE CASCADE ON UPDATE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
