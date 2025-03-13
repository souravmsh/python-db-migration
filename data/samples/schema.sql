
DROP TABLE IF EXISTS `Temp_Email`;
CREATE TABLE `Temp_Email` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `Investor_Code` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `e-mail` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `approved_by` bigint DEFAULT NULL,
  `approved_dt` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `subscriptions`;
CREATE TABLE `subscriptions` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `client_code` varchar(32) NOT NULL,
  `email` varchar(64) NOT NULL,
  `status` enum('Active','Inactive') NOT NULL DEFAULT 'Active',
  `updated_by` bigint DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `subscriptions_temp`;
CREATE TABLE `subscriptions_temp` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `client_code` varchar(32) NOT NULL,
  `email` varchar(64) NOT NULL,
  `status` enum('Active','Inactive') NOT NULL DEFAULT 'Active',
  `updated_by` bigint DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


