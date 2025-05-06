import os
import random
from mysql.connector import Error
from utils.mysql import mysql_connect

def create_schema(connection, schema_sql):
    try:
        cursor = connection.cursor()
        for statement in schema_sql.split(';'):
            if statement.strip():
                cursor.execute(statement)
        connection.commit()
        print("Database schema created successfully!")
    except Error as e:
        print(f"Error creating schema: {e}")
    finally:
        cursor.close()

def faker(connection):
    try:
        cursor = connection.cursor()
        data = [(f'client{i}', f'client{i}@example.com', random.choice(['Active', 'Inactive']), None) for i in range(1, 1001)]
        
        insert_query = """
        INSERT INTO subscriptions (client_code, email, status, updated_by) 
        VALUES (%s, %s, %s, %s)
        """
        cursor.executemany(insert_query, data)
        connection.commit()
        print("1000 fake records inserted successfully into subscriptions and subscriptions_temp!")
    except Error as e:
        print(f"Error inserting fake data: {e}")
    finally:
        cursor.close()

schema = """
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

DROP TABLE IF EXISTS `clients`;
CREATE TABLE `clients` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `client_code` varchar(20) NOT NULL,
  `boid` varchar(20) NOT NULL,
  `mobile` varchar(16) DEFAULT NULL,
  `email` varchar(64) DEFAULT NULL,
  `bank_name` varchar(64) DEFAULT NULL,
  `bank_account` varchar(30) DEFAULT NULL,
  `status` enum('Active','Inactive') NOT NULL DEFAULT 'Active',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);
"""

def main():
    connection = mysql_connect()
    if connection:
        create_schema(connection, schema)
        faker(connection)
        connection.close()

if __name__ == "__main__":
    main()
