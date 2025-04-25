-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: mysql
-- Generation Time: Apr 24, 2025 at 08:38 AM
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
-- Database: `web`
--

-- --------------------------------------------------------

--
-- Table structure for table `images`
--

CREATE TABLE `images` (
  `image_pk` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `image_user_fk` varchar(32) NOT NULL,
  `image_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `items`
--

CREATE TABLE `items` (
  `item_pk` char(32) NOT NULL,
  `item_name` varchar(50) NOT NULL,
  `item_image` varchar(50) NOT NULL,
  `item_price` int UNSIGNED NOT NULL,
  `item_lon` varchar(50) NOT NULL,
  `item_lat` varchar(50) NOT NULL,
  `item_created_at` bigint UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `items`
--

INSERT INTO `items` (`item_pk`, `item_name`, `item_image`, `item_price`, `item_lon`, `item_lat`, `item_created_at`) VALUES
('193e055791ed4fa5a6f24d0ea7422a89', 'Tivoli Gardens', '2.jpg', 220000, '12.5673', '55.6731', 2),
('56f9d2171b2646f7a077a6ee4a0ce3c9', 'The Little Mermaid Statue', '3.jpg', 350950, '12.6030', '55.6910', 3),
('b8f0c4a9fa0d4d1c8c38a1d8986e9c7d', 'Nyhavn (Harbor)', '1.jpg', 100000, '12.5903', '55.6763', 1),
('cf9e4a6d71ea45cba17078df4d7b2516', 'Rosenborg Castle', '5.jpg', 5000000, '12.5844', '55.6838', 5),
('f08b6d7c45ff46a0a95cd13b56ab5676', 'Amalienborg Palace', '4.jpg', 495000, '12.5917', '55.6759', 4);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_pk` char(32) NOT NULL,
  `user_name` varchar(20) NOT NULL,
  `user_last_name` varchar(20) NOT NULL,
  `user_username` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `user_email` varchar(100) NOT NULL,
  `user_password` varchar(255) NOT NULL,
  `user_created_at` bigint UNSIGNED NOT NULL,
  `user_updated_at` bigint UNSIGNED NOT NULL,
  `user_deleted_at` bigint UNSIGNED NOT NULL DEFAULT '0',
  `is_admin` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_pk`, `user_name`, `user_last_name`, `user_username`, `user_email`, `user_password`, `user_created_at`, `user_updated_at`, `user_deleted_at`, `is_admin`) VALUES
('2e561df506cb460b927438f9070ff3f1', 'dd', '', '', 'd@d.com', '', 0, 0, 0, 0),
('3d7ff97dce6a4a01b21b53a5b3067d6d', 'cc', '', '', 'c@c.com', '', 0, 0, 0, 0),
('41f7eb4220e611f0814b0242ac160002', 'Admin', 'Web', 'admin', 'admin@web.com', 'admin', 1745483376, 1745483376, 0, 1),
('47c9425d30b84789b789d1ae69fe7ab3', 'ee', '', '', 'e@e.com', '', 0, 0, 0, 0),
('af12f713a8ff4b079b9564dfad0cc6d7', 'ff', '', '', 'f@f.com', '', 0, 0, 0, 0),
('b6e4a3f3192d46fcb2b7c927576e6f77', 'bb', '', '', 'b@b.com', '', 0, 0, 0, 0),
('ccad60125be84df5aca4df3fa005d628', 'aa', '', '', 'a@a.com', '', 0, 0, 1742382471, 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `images`
--
ALTER TABLE `images`
  ADD PRIMARY KEY (`image_pk`);

--
-- Indexes for table `items`
--
ALTER TABLE `items`
  ADD PRIMARY KEY (`item_pk`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_pk`),
  ADD UNIQUE KEY `user_email` (`user_email`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
