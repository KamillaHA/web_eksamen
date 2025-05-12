-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: mysql
-- Generation Time: May 05, 2025 at 12:15 PM
-- Server version: 9.3.0
-- PHP Version: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `new`
--

-- --------------------------------------------------------

--
-- Table structure for table `images`
--

CREATE TABLE `images` (
  `image_pk` int UNSIGNED NOT NULL,
  `item_id` int UNSIGNED NOT NULL,
  `item_image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `image_slot` tinyint(1) NOT NULL,
  `image_created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `image_updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `image_deleted_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `items`
--

CREATE TABLE `items` (
  `item_pk` int UNSIGNED NOT NULL,
  `item_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `item_address` varchar(255) NOT NULL,
  `item_price` decimal(6,2) NOT NULL,
  `item_latitude` decimal(8,6) NOT NULL,
  `item_longitude` decimal(9,6) NOT NULL,
  `item_created_by` int UNSIGNED NOT NULL,
  `item_is_blocked` tinyint(1) NOT NULL DEFAULT '0',
  `item_created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `item_updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `item_deleted_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_pk` int UNSIGNED NOT NULL,
  `user_name` varchar(20) NOT NULL,
  `user_last_name` varchar(20) NOT NULL,
  `user_username` varchar(20) NOT NULL,
  `user_email` varchar(255) NOT NULL,
  `user_password` char(60) NOT NULL,
  `user_is_admin` tinyint(1) NOT NULL DEFAULT '0',
  `user_is_blocked` tinyint(1) NOT NULL DEFAULT '0',
  `user_password_reset_token` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `user_password_reset_expires` timestamp NULL DEFAULT NULL,
  `user_verification_token` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `user_verified_at` timestamp NULL DEFAULT NULL,
  `user_created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_deleted_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_pk`, `user_name`, `user_last_name`, `user_username`, `user_email`, `user_password`, `user_is_admin`, `user_is_blocked`, `user_password_reset_token`, `user_password_reset_expires`, `user_verification_token`, `user_verified_at`, `user_created_at`, `user_updated_at`, `user_deleted_at`) VALUES
(1, 'Aa', 'Bb', 'AaBb', 'Aa@Bb.com', '', 0, 0, NULL, NULL, NULL, NULL, '2025-05-05 12:13:40', '2025-05-05 12:13:40', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `images`
--
ALTER TABLE `images`
  ADD PRIMARY KEY (`image_pk`),
  ADD KEY `item_id` (`item_id`);

--
-- Indexes for table `items`
--
ALTER TABLE `items`
  ADD PRIMARY KEY (`item_pk`),
  ADD UNIQUE KEY `item_pk` (`item_pk`),
  ADD UNIQUE KEY `item_name` (`item_name`),
  ADD UNIQUE KEY `item_address` (`item_address`),
  ADD KEY `item_created_by` (`item_created_by`);
ALTER TABLE `items` ADD FULLTEXT KEY `item_name_2` (`item_name`);
ALTER TABLE `items` ADD FULLTEXT KEY `item_address_2` (`item_address`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_pk`),
  ADD UNIQUE KEY `user_pk` (`user_pk`),
  ADD UNIQUE KEY `user_username` (`user_username`),
  ADD UNIQUE KEY `user_email` (`user_email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `images`
--
ALTER TABLE `images`
  MODIFY `image_pk` int UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `items`
--
ALTER TABLE `items`
  MODIFY `item_pk` int UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_pk` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `images`
--
ALTER TABLE `images`
  ADD CONSTRAINT `images_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `items` (`item_pk`) ON DELETE CASCADE ON UPDATE RESTRICT;

--
-- Constraints for table `items`
--
ALTER TABLE `items`
  ADD CONSTRAINT `items_ibfk_1` FOREIGN KEY (`item_created_by`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE ON UPDATE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
