-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: mysql
-- Generation Time: May 27, 2025 at 09:05 PM
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

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`%` PROCEDURE `get_items_by_location` (IN `city` VARCHAR(100))   SELECT * FROM items
WHERE item_address LIKE CONCAT('%', city, '%')
  AND item_deleted_at IS NULL$$

CREATE DEFINER=`root`@`%` PROCEDURE `get_users_items` (IN `uid` INT)   SELECT * FROM items WHERE item_created_by = uid AND item_deleted_at IS NULL$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `images`
--

CREATE TABLE `images` (
  `image_pk` int UNSIGNED NOT NULL,
  `item_id` int UNSIGNED NOT NULL,
  `item_image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `item_image_2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `item_image_3` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `image_created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `image_updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `image_deleted_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `images`
--

INSERT INTO `images` (`image_pk`, `item_id`, `item_image`, `item_image_2`, `item_image_3`, `image_created_at`, `image_updated_at`, `image_deleted_at`) VALUES
(20, 21, 'e136b52b5dd54319877b3938b78ff46d.jpg', '', '', '2025-05-12 16:21:07', '2025-05-12 16:21:07', NULL),
(21, 22, 'cad7e635c1b340218b0262e33d29830c.jpg', '', '', '2025-05-12 16:22:28', '2025-05-12 16:22:28', NULL),
(22, 23, 'fce2d2436f5b49049959ac1c6b6c1c8c.jpg', '', '', '2025-05-12 16:23:14', '2025-05-12 16:23:14', NULL),
(23, 24, '8432097daab547c2a73d11ec1be4119b.jpg', '', '', '2025-05-12 16:23:56', '2025-05-12 16:23:56', NULL),
(24, 25, '299f13682bf242a68067cf1b40da609f.jpg', '', '', '2025-05-12 16:24:40', '2025-05-12 16:24:40', NULL),
(25, 26, 'df7dd809d2c14e1782226bafa82be775.jpg', '', '', '2025-05-12 16:25:19', '2025-05-12 16:25:19', NULL),
(26, 27, '7efaefed4b514abf86cfc006902d61fd.jpg', '', '', '2025-05-12 16:25:58', '2025-05-12 16:25:58', NULL),
(27, 28, 'ff63daad13344df69b755164c85999eb.jpg', '', '', '2025-05-12 16:26:29', '2025-05-12 16:26:29', NULL),
(28, 29, '70858e302bc9413abc10299330e56b29.jpg', '', '', '2025-05-12 16:26:57', '2025-05-12 16:26:57', NULL),
(29, 30, 'b878a9e999bc4e6394201800224ea451.jpg', '', '', '2025-05-12 16:27:30', '2025-05-12 16:27:30', NULL),
(30, 31, 'f4300f21247744f99a36f86587220ae6.jpg', '', '', '2025-05-12 16:28:03', '2025-05-12 16:28:03', NULL),
(31, 32, '805e3124a8044f5c8c525a3cc19929e0.jpg', '', '', '2025-05-12 16:28:50', '2025-05-12 16:28:50', NULL),
(32, 33, 'f1a7940cb3c14e798e597b89945a7a14.jpg', '', '', '2025-05-12 16:29:24', '2025-05-12 16:29:24', NULL),
(33, 34, '4701b9b024e44a1ba328b8334484b1a8.jpg', '', '', '2025-05-12 16:29:56', '2025-05-12 16:29:56', NULL),
(34, 35, 'e711ba5b993646d1b75b628372584b67.jpg', '', '', '2025-05-12 16:30:33', '2025-05-12 16:30:33', NULL),
(40, 43, 'c21d8f543efa4bd7afab8a0de6cbd440.jpg', 'd6c2354a1c88474db6160387db3254ce.jpg', '8168c72fa28e4a26a04076be894cfad5.jpg', '2025-05-23 08:22:39', '2025-05-23 08:22:39', NULL),
(41, 44, '5e18f88b52de4103b11a471ce5dfb2a5.jpg', NULL, NULL, '2025-05-23 12:33:01', '2025-05-23 12:33:01', NULL),
(44, 52, 'c40079999ace4e9589ebf2906db429d6.jpg', 'ee00e3c7c0764d6b9ea2d49fa1b01d98.jpg', 'cc3173591c034b128d1c5c9b6e712d97.jpg', '2025-05-26 08:58:23', '2025-05-26 08:58:23', NULL),
(66, 83, '0cc418d893ee424ea0ed21408b5b9e9e.jpg', '36b3bd83c4974d20abe71248e74c02b3.jpg', NULL, '2025-05-27 05:29:55', '2025-05-27 05:44:37', NULL),
(68, 85, '0c2059c5e68d4ae38d910498494b2932.jpg', NULL, NULL, '2025-05-27 06:56:39', '2025-05-27 06:56:39', NULL),
(69, 86, 'a9e781027c7947279494b82a9920f79d.jpg', NULL, NULL, '2025-05-27 09:02:39', '2025-05-27 09:02:39', NULL),
(70, 87, '493b197250614e9885fd9cf0a2d55252.jpg', NULL, NULL, '2025-05-27 10:08:42', '2025-05-27 10:08:42', NULL),
(71, 88, 'e8e4924206cc433396a1c307adc08f24.jpg', NULL, NULL, '2025-05-27 17:08:39', '2025-05-27 17:08:39', NULL),
(72, 89, 'c56cab33a41b4df2ae524f9abaa86e8b.jpg', NULL, NULL, '2025-05-27 17:15:28', '2025-05-27 17:15:28', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `items`
--

CREATE TABLE `items` (
  `item_pk` int UNSIGNED NOT NULL,
  `item_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `item_address` varchar(255) NOT NULL,
  `item_price` int UNSIGNED NOT NULL,
  `item_latitude` decimal(8,6) NOT NULL,
  `item_longitude` decimal(9,6) NOT NULL,
  `item_created_by` int UNSIGNED NOT NULL,
  `item_is_blocked` tinyint(1) NOT NULL DEFAULT '0',
  `item_created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `item_updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `item_deleted_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `items`
--

INSERT INTO `items` (`item_pk`, `item_name`, `item_address`, `item_price`, `item_latitude`, `item_longitude`, `item_created_by`, `item_is_blocked`, `item_created_at`, `item_updated_at`, `item_deleted_at`) VALUES
(21, 'Skolekrogens Læsehjørne Værløse', 'Skolekrogen 107, 3550 Værløse', 15, 55.782855, 12.389090, 4, 0, '2025-05-12 16:21:07', '2025-05-12 16:21:07', NULL),
(22, 'Ledøjes Frie Bogskab', 'Præstetoften 5, 2765 Smørum', 8, 55.713183, 12.308311, 5, 1, '2025-05-12 16:22:28', '2025-05-27 10:47:03', NULL),
(23, 'Bogskab i Esbjerg', 'Kirkegade 10, 6700 Esbjerg', 16, 55.465823, 8.448625, 6, 1, '2025-05-12 16:23:14', '2025-05-27 10:51:31', NULL),
(24, 'Litteraturhylden i Kolding', 'Slotsgade 5, 6000 Kolding', 18, 55.490568, 9.475102, 7, 1, '2025-05-12 16:23:56', '2025-05-27 20:32:32', NULL),
(25, 'Lille Bibliotek Kastrup', 'Rhodesiavej 31, 2770 Kastrup', 20, 55.604021, 12.577747, 8, 1, '2025-05-12 16:24:40', '2025-05-27 10:30:59', NULL),
(26, 'Vedbæks Litteraturskur', 'Sandbjergvej 36, 2950 Vedbæk', 10, 55.855784, 12.527768, 9, 0, '2025-05-12 16:25:19', '2025-05-12 16:25:19', NULL),
(27, 'Fredensborg Boghus', 'Humlebækvej 39, 3480 Fredensborg', 9, 55.967820, 12.463436, 15, 0, '2025-05-12 16:25:58', '2025-05-27 18:13:58', NULL),
(28, 'Bogbyttehuset i Aarhus', 'Nørre Allé 23, 8000 Aarhus', 5, 56.160146, 10.206950, 16, 1, '2025-05-12 16:26:29', '2025-05-27 18:13:39', NULL),
(29, 'Ågades Byttehylde Frederikssund', 'Ågade 56, 3600 Frederikssund', 6, 55.833654, 12.089242, 17, 0, '2025-05-12 16:26:57', '2025-05-12 16:26:57', NULL),
(30, 'Hylden i Lyngby', 'Caroline Amalie Vej 22, 2800 Kongens Lyngby', 7, 55.780486, 12.503138, 18, 1, '2025-05-12 16:27:30', '2025-05-27 13:43:06', NULL),
(31, 'Lille Bibliotek Odense', 'Skibhusvej 52, 5000 Odense', 17, 55.404212, 10.392146, 19, 1, '2025-05-12 16:28:03', '2025-05-27 17:55:07', NULL),
(32, 'Byttebogskassen i Aalborg', 'Boulevarden 15, 9000 Aalborg', 14, 57.045671, 9.918571, 20, 0, '2025-05-12 16:28:50', '2025-05-27 18:56:18', NULL),
(33, 'Bogskabet på Otto Busses København', 'Otto Busses Vej 54, 2450 København', 12, 55.660573, 12.543567, 21, 0, '2025-05-12 16:29:24', '2025-05-27 13:29:43', NULL),
(34, 'Virum Bogkasse', 'Brovænget 44, 2830 Virum', 11, 55.799546, 12.460818, 22, 0, '2025-05-12 16:29:56', '2025-05-27 09:16:09', NULL),
(35, 'Ballerup Bøger', 'Egebjerghuse 5, 2750 Ballerup', 22, 55.752111, 12.374680, 23, 0, '2025-05-12 16:30:33', '2025-05-27 20:32:27', NULL),
(43, 'Test', 'vinkelvej 7, ganløse', 10, 55.788205, 12.264440, 4, 0, '2025-05-23 08:22:39', '2025-05-23 08:22:39', NULL),
(44, 'test biblo', 'jernbanegade 2, roskilde', 10, 55.639611, 12.088510, 42, 0, '2025-05-23 12:33:01', '2025-05-27 20:28:50', NULL),
(52, 'Julebiblo', 'Jernbanegade 24, Roskilde', 24, 55.638906, 12.087587, 63, 0, '2025-05-26 08:58:23', '2025-05-27 09:16:19', NULL),
(83, 'hjjhjiiiiiii', 'ny østergade 16, roskilde', 9, 55.637970, 12.091464, 63, 0, '2025-05-27 05:29:55', '2025-05-27 09:16:22', NULL),
(85, 'hhhhhhhhhh', 'hhhhhh', 8, 32.368779, -6.443559, 70, 0, '2025-05-27 06:56:38', '2025-05-27 09:42:11', NULL),
(86, 'jkljlkhhgg', 'jlkj', 0, 0.000000, 0.000000, 63, 1, '2025-05-27 09:02:39', '2025-05-27 09:41:25', NULL),
(87, 'hjjjjhkhjk', 'hjkhkjhj', 9, 0.000000, 0.000000, 63, 1, '2025-05-27 10:08:42', '2025-05-27 18:14:35', NULL),
(88, 'mllk', 'kijoj', 8, 0.000000, 0.000000, 63, 0, '2025-05-27 17:08:39', '2025-05-27 17:08:39', NULL),
(89, 'jio', 'hupi', 9, 13.501373, 122.028189, 63, 0, '2025-05-27 17:15:28', '2025-05-27 17:15:28', NULL);

--
-- Triggers `items`
--
DELIMITER $$
CREATE TRIGGER `soft_delete_images` AFTER UPDATE ON `items` FOR EACH ROW IF NEW.item_deleted_at IS NOT NULL AND OLD.item_deleted_at IS NULL THEN
  UPDATE images
  SET image_deleted_at = NOW()
  WHERE item_id = NEW.item_pk;
END IF
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Stand-in structure for view `items_with_coordinates_missing`
-- (See below for the actual view)
--
CREATE TABLE `items_with_coordinates_missing` (
`item_address` varchar(255)
,`item_created_at` timestamp
,`item_created_by` int unsigned
,`item_deleted_at` timestamp
,`item_is_blocked` tinyint(1)
,`item_latitude` decimal(8,6)
,`item_longitude` decimal(9,6)
,`item_name` varchar(64)
,`item_pk` int unsigned
,`item_price` int unsigned
,`item_updated_at` timestamp
);

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
  `user_password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `user_is_admin` tinyint(1) NOT NULL DEFAULT '0',
  `user_is_blocked` tinyint(1) NOT NULL DEFAULT '0',
  `user_blocked_at` timestamp NULL DEFAULT NULL,
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

INSERT INTO `users` (`user_pk`, `user_name`, `user_last_name`, `user_username`, `user_email`, `user_password`, `user_is_admin`, `user_is_blocked`, `user_blocked_at`, `user_password_reset_token`, `user_password_reset_expires`, `user_verification_token`, `user_verified_at`, `user_created_at`, `user_updated_at`, `user_deleted_at`) VALUES
(3, 'Admin', 'Web', 'AdminWeb', 'admin@web.com', 'scrypt:32768:8:1$XzY9joqnpXD7LUsI$3046a9f0e4492d1d54bd2103ca93cc929c2205f6ddc2ea3d8bad9c9df521006bb336535b24bf997dfe726cd889ad459c869b42fa6e563ca67e6df0da32a5eba1', 1, 0, NULL, NULL, NULL, NULL, NULL, '2025-05-07 10:09:55', '2025-05-07 10:10:24', NULL),
(4, 'Anders', 'Andersen', 'AndersA', 'anders@a.com', 'scrypt:32768:8:1$vcPwVuLo9KUxlThS$6d63d78ce8f7744a178d66e0a9ef749556f38f414a2b0c95cb7b34342ab7e9cde372797e7466782f5acfc8088c9acad90cd3ac8685675322daefff3aa88f42f0', 0, 1, NULL, NULL, NULL, NULL, NULL, '2025-05-07 10:26:14', '2025-05-23 10:49:03', '2025-05-23 10:49:03'),
(5, 'Lars', 'Larsen', 'LarsL', 'lars@l.com', 'scrypt:32768:8:1$yg01MTeDKTlZf4nS$bdbde58418102188118462b2296b769eb8524c801fffaf8a0333285b76b4e89c7f3d0452e16f00c99eb2d85b27ace281f795932f0937108fde3ec0c531c2c9d9', 0, 1, '2025-05-27 10:47:03', NULL, NULL, NULL, NULL, '2025-05-07 10:26:54', '2025-05-27 10:47:03', NULL),
(6, 'Bente', 'Bentsen', 'BenteB', 'bente@b.com', 'scrypt:32768:8:1$CuJxGiYAJmcJAjJ1$7b735f2ec55a51efd56243ad10b7d1d92d8e67cf02ee23d5cabe8d5b545ff314b37cda7267c6b6a9687918cbaf7dce4d1a1a3777371830d42dbee34d18e249d4', 0, 1, '2025-05-27 10:51:31', NULL, NULL, NULL, NULL, '2025-05-07 10:28:06', '2025-05-27 10:51:31', NULL),
(7, 'Carl', 'Carlsen', 'CarlC', 'carl@c.com', 'scrypt:32768:8:1$ZL7xslcUDSVFeftc$9cf202b12f0b268daec4a8efbce26d106b4dcfaeb9b1ce7df71f6f110d348ef0ac1363a20ffe1bbcbc901f6de546300e7325d117ea2643f6187eebd4cb490cfd', 0, 1, '2025-05-27 20:32:32', NULL, NULL, NULL, NULL, '2025-05-07 10:28:26', '2025-05-27 20:32:32', NULL),
(8, 'Hans', 'Hansen', 'HansH', 'hans@h.com', 'scrypt:32768:8:1$3rsfBSzwDXFln2JO$10ef90875cd9e86619d726de66f7f6a40dc2d9da20f4b3d8f1ccfc6d6930ffcad9ebaa1f76beaa49da04b8495037eb4457538516968150d10b25fc3b18598b3a', 0, 1, '2025-05-27 10:30:59', NULL, NULL, NULL, NULL, '2025-05-07 10:29:46', '2025-05-27 10:30:59', NULL),
(9, 'Mads', 'Madsen', 'MadsM', 'mads@m.com', 'scrypt:32768:8:1$OeJjEHHDPPmK4in5$8fff9444f9b562e659d70814e465d7fbbcd044df7c62204b5b3792b6ee9cecc3544899acb79e64e5668b5afbe8272a6665ad81d574a27a3688d41972993475f2', 0, 0, NULL, NULL, NULL, NULL, NULL, '2025-05-07 10:30:09', '2025-05-27 07:26:52', NULL),
(15, 'Kristine', 'Kristensen', 'KristineK', 'kristine@k.com', 'scrypt:32768:8:1$kiJI2BuVe3ICPHHU$18d020e06f505e2afecd3045037a7f3cd475785fb5c9800e1d503b8934a9d76e5115b7f374cb4726cb334afe0897964f4a64c475366956f53d61a8d3b0d270a5', 0, 0, NULL, NULL, NULL, NULL, NULL, '2025-05-07 10:49:26', '2025-05-27 07:26:45', NULL),
(16, 'Frederik', 'Frederiksen', 'FrederikF', 'frederik@f.com', 'scrypt:32768:8:1$ysuXKR7rE6tzPSyt$588d739df605a544ef7b8b9d028a484aedffde938a19287e9bbcfbf1eb8a3223f56e0ed0b73191ae3298dbedf02ff046cefcad0a942edaf27d5d3bf9f755ff88', 0, 1, '2025-05-27 18:13:39', NULL, NULL, NULL, NULL, '2025-05-07 10:50:00', '2025-05-27 18:13:39', NULL),
(17, 'Inge', 'Ingersen', 'IngeI', 'inge@i.com', 'scrypt:32768:8:1$eSR9r1UxGFgSfTt8$ca2c7ea3ac15223f665c068a4f85a452ff724226bcb7e32d80b5b5967922299fe34e74b397b443a9ec19c2e60c3b54185884ada719e2c54dd78b88c4eae8cb74', 0, 0, NULL, NULL, NULL, NULL, NULL, '2025-05-07 10:50:29', '2025-05-07 10:50:29', NULL),
(18, 'Johanne', 'Johansen', 'JohanneJ', 'johanne@j.com', 'scrypt:32768:8:1$Tui3GfIKHhcBl6ix$2c5ad178d8bebca717bd9f033b69e27f2f9e333fec87b7c1c3f977e8c500c411a0feabf44fb1185e8a0620d9f54706cce0d110cbb5af3f19123b48dffee2cd62', 0, 0, NULL, NULL, NULL, NULL, NULL, '2025-05-07 10:50:51', '2025-05-27 07:26:56', NULL),
(19, 'Niels', 'Nielsen', 'NielsN', 'niels@n.com', 'scrypt:32768:8:1$Ti0xrUPnpLXbkLEa$76f3aa91cc74904661c89f2782055ca300d0d62ae09a9dd0838550b39e9fc8082f6f2453a27bfe54e7304603c2779c6b54421687218fc930ba9ffc8f27db2af7', 0, 1, '2025-05-27 17:55:07', NULL, NULL, NULL, NULL, '2025-05-07 10:51:20', '2025-05-27 17:55:07', NULL),
(20, 'Pede', 'Pedersen', 'PedeP', 'pede@p.com', 'scrypt:32768:8:1$xHTFXxNH43cG1p1R$d39893e71606aa590b91a26e9f355eb0fa83d5a0a01b0c92bb2dc2920a546b2cabe10b917ad1b37d1920f3b0a9668d9b8a08dd2c32bcd261acab2d296414bd98', 0, 0, NULL, NULL, NULL, NULL, NULL, '2025-05-07 10:51:44', '2025-05-07 10:51:44', NULL),
(21, 'Rasmus', 'Rasmussen', 'RasmusR', 'rasmus@r.com', 'scrypt:32768:8:1$rfeKQuhuowxl7Md8$208c5e55507ddda667c840325d8266ae284c2f14097bc72fa13e444581d7f72aad61de364a1aad67a72da7ec5ad7c0d619538ed539c52f45a7985dcec5434231', 0, 0, NULL, NULL, NULL, NULL, NULL, '2025-05-07 10:52:08', '2025-05-07 10:52:08', NULL),
(22, 'Simone', 'Simonsen', 'SimoneS', 'simone@s.com', 'scrypt:32768:8:1$wc8yeVFagsWHt9iY$9771b50175104ff1c992e5dec9a8df543a54c6bd8336d4178c1cb1069fed7b7c74f8de4d617bb3fb062a11fe5f94ed665be759c689f964443a2e6e6d789e2531', 0, 0, NULL, NULL, NULL, NULL, NULL, '2025-05-07 10:52:26', '2025-05-07 10:52:26', NULL),
(23, 'Vilhelm', 'Vilhelmsen', 'VilhelmV', 'vilhelm@v.com', 'scrypt:32768:8:1$O90QeB1b7FqxRYgy$7f75c5c2b073be975a570da9935b51a2372d9064911ce96df1ee1dc3b9bb74d5632e5bdc73a71f8f9bff915dcb5d93f5f591ad10d13f582205e182ca283b5fa4', 0, 0, NULL, NULL, NULL, NULL, NULL, '2025-05-07 10:53:07', '2025-05-12 16:33:05', NULL),
(42, 'Anders', 'Andersen', 'AndersABC', 'anders@ab.com', 'scrypt:32768:8:1$dn7LWHKA7FwYIaoK$ab8f820ecb1e5e30cec3cfb66cfc694211e3c57c21f4f997fdcd9dc050d1485e24697b3b2ab14dbb6adc49e055910746d39fa1ff3a31a99a5e632d422b7e9b24', 0, 0, '2025-05-27 20:28:48', NULL, NULL, NULL, NULL, '2025-05-23 10:50:32', '2025-05-27 20:28:50', NULL),
(63, 'jul', 'jul', 'jul', 'jul@jul.com', 'scrypt:32768:8:1$mIEAkkSoj6UxQCJT$0586acd4a7e865a53b43dff985f3f454402bc50413e42e403a635720547c6b965533d64fb85c06ac1afe68b4ee4220d746e4dd85d6c5c138d6982446bdcdc8c1', 0, 0, NULL, '43487469-d2fa-40fc-a415-c37e3f934fe7', '2025-05-27 18:27:56', '7a81ffc6-49a6-4b12-a685-93924dec4893', '2025-05-25 17:35:42', '2025-05-25 17:33:03', '2025-05-27 17:27:56', NULL),
(65, 'kl', 'kl', 'kl', 'kl@kl.com', 'scrypt:32768:8:1$y6h93HhhGOSRlU8q$8a7ec4e619b357fda6097ee4243d0f1f2d5a92d973e9c2b08c41dde903d7d9cbe025a18a7141d1dbff0111cd7e5da3a37693232f9b51a2c5574210bbc3e43ed7', 0, 1, '2025-05-26 16:56:13', NULL, NULL, '043bf345-b42b-4bcb-acb7-62a630ec0e86', '2025-05-26 16:54:39', '2025-05-26 16:54:17', '2025-05-26 16:56:13', '2025-05-26 16:56:13'),
(66, 'mko', 'ii', 'ui', 'ii@k.com', 'scrypt:32768:8:1$Y8gAH0oCzLSNFxKs$597faa57bc11d5380dda8d851fdbea94f660fc6122550ee76cd806ae698188692db2fc30c7e5c6b2d9e5811ee9d574919391471306b4bce544a4287d37ea56c4', 0, 1, '2025-05-27 05:56:08', NULL, NULL, '942518c9-e5c8-44ab-acb4-473d20c953af', '2025-05-27 05:25:49', '2025-05-27 05:24:28', '2025-05-27 05:56:08', '2025-05-27 05:56:08'),
(67, 'del', 'del', 'del', 'del@del.com', 'scrypt:32768:8:1$s1TgIiMoXLkfbzRE$9e110484d21ba8021cb10d02c3ad14ec6553cdf9e1421e51397440060232b2a63f831049a2a9cf74144a57d2d4a03b64ffcb177836438339a4e0225e0828f220', 0, 1, '2025-05-27 05:59:33', NULL, NULL, '5130b717-b4cc-4bd7-99ad-158615e22cf1', '2025-05-27 05:59:21', '2025-05-27 05:59:11', '2025-05-27 05:59:33', '2025-05-27 05:59:33'),
(68, 'olo', 'olo', 'olo', 'olo@o.com', 'scrypt:32768:8:1$wZtBjVt9tgnZraXs$bbe91d4a350ca27018ec09a7370d1344af74fcf27de8372deba943d7a1591888b8f9589be43a4522d6bf682b28a857b78ff1c9889da8f8d1713ccddff069a944', 0, 1, '2025-05-27 06:07:02', NULL, NULL, '7526658f-18b8-4db3-8161-eea3c57594ac', '2025-05-27 06:06:12', '2025-05-27 06:06:04', '2025-05-27 06:07:02', '2025-05-27 06:07:02'),
(69, 'ooo', 'ooo', 'oooo', 'oo@o.com', 'scrypt:32768:8:1$mq2GKsGKhZgKgYnL$3bd80ebfc737c08086faab625d7c1a25e23bfcb3a5dbad25ab01c742f3f075b8c68a04d90b988015b35519f8f61ac8a8d013209bda6381d3a112c601e3ae582d', 0, 1, '2025-05-27 07:22:03', NULL, NULL, 'e2bf1273-c651-4fd0-a3d2-64f15fe342fc', '2025-05-27 06:08:08', '2025-05-27 06:07:56', '2025-05-27 07:22:03', '2025-05-27 06:08:47'),
(70, 'tt', 'tt', 'tt', 't@t.com', 'scrypt:32768:8:1$i6GbSDvyzHmkAxII$12cdedb44256d5beaaafddac7ede36914eabad9b6a09bcbe15e00e74f883754e8e5bacf7aef97f14830b4e0325b4c1eceea33960ff8409679dd387777ed87dff', 0, 0, '2025-05-27 09:41:51', NULL, NULL, 'b5dd6317-7b91-4105-8b75-b4023a1d0b3b', '2025-05-27 06:15:22', '2025-05-27 06:15:12', '2025-05-27 09:42:11', NULL),
(71, 'bn', 'bn', 'bn', 'bn@bn.com', 'scrypt:32768:8:1$nOoXncbAd4s9RqZw$223caec5d96dff98e55d301cee189ed187c039f19a9d09236b109bad7793b401bce4640a207bb8d2b5719e27ddb6d75cf359636fc326921690d646e26bc7c6b0', 0, 0, NULL, NULL, NULL, 'b7f668fa-ca70-4f11-86cb-5b521b11a543', NULL, '2025-05-27 17:18:20', '2025-05-27 17:18:20', NULL);

--
-- Triggers `users`
--
DELIMITER $$
CREATE TRIGGER `timestamp_user_blocked` BEFORE UPDATE ON `users` FOR EACH ROW IF NEW.user_is_blocked = 1 AND OLD.user_is_blocked = 0 THEN
  SET NEW.user_blocked_at = NOW();
END IF
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Stand-in structure for view `users_with_no_items`
-- (See below for the actual view)
--
CREATE TABLE `users_with_no_items` (
`user_email` varchar(255)
,`user_last_name` varchar(20)
,`user_name` varchar(20)
,`user_pk` int unsigned
);

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
ALTER TABLE `items` ADD FULLTEXT KEY `item_name_2` (`item_name`,`item_address`);

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
  MODIFY `image_pk` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=73;

--
-- AUTO_INCREMENT for table `items`
--
ALTER TABLE `items`
  MODIFY `item_pk` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=90;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_pk` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=72;

-- --------------------------------------------------------

--
-- Structure for view `items_with_coordinates_missing`
--
DROP TABLE IF EXISTS `items_with_coordinates_missing`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `items_with_coordinates_missing`  AS SELECT `items`.`item_pk` AS `item_pk`, `items`.`item_name` AS `item_name`, `items`.`item_address` AS `item_address`, `items`.`item_price` AS `item_price`, `items`.`item_latitude` AS `item_latitude`, `items`.`item_longitude` AS `item_longitude`, `items`.`item_created_by` AS `item_created_by`, `items`.`item_is_blocked` AS `item_is_blocked`, `items`.`item_created_at` AS `item_created_at`, `items`.`item_updated_at` AS `item_updated_at`, `items`.`item_deleted_at` AS `item_deleted_at` FROM `items` WHERE (((`items`.`item_latitude` = 0) OR (`items`.`item_longitude` = 0)) AND (`items`.`item_deleted_at` is null)) ;

-- --------------------------------------------------------

--
-- Structure for view `users_with_no_items`
--
DROP TABLE IF EXISTS `users_with_no_items`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `users_with_no_items`  AS SELECT `u`.`user_pk` AS `user_pk`, `u`.`user_name` AS `user_name`, `u`.`user_last_name` AS `user_last_name`, `u`.`user_email` AS `user_email` FROM (`users` `u` left join `items` `i` on((`u`.`user_pk` = `i`.`item_created_by`))) WHERE ((`i`.`item_pk` is null) AND (`u`.`user_deleted_at` is null)) ;

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
