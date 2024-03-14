/*
 Navicat Premium Data Transfer

 Source Server         : alivepools
 Source Server Type    : MySQL
 Source Server Version : 80030
 Source Host           : db-mysql-sgp1-19924-do-user-15764718-0.c.db.ondigitalocean.com:25060
 Source Schema         : defaultdb

 Target Server Type    : MySQL
 Target Server Version : 80030
 File Encoding         : 65001

 Date: 14/03/2024 04:14:41
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tasks
-- ----------------------------
DROP TABLE IF EXISTS `tasks`;
CREATE TABLE "tasks" (
  "id" int NOT NULL AUTO_INCREMENT,
  "user_id" int NOT NULL,
  "domain" varchar(255) NOT NULL,
  "email" varchar(255) NOT NULL,
  "send_frequency" int DEFAULT NULL,
  "created_at" datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "status" enum('active','inactive') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'active',
  "last_run_time" datetime DEFAULT NULL,
  PRIMARY KEY ("id"),
  KEY "user_id" ("user_id"),
  CONSTRAINT "tasks_ibfk_1" FOREIGN KEY ("user_id") REFERENCES "users" ("id")
);

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE "users" (
  "id" int NOT NULL AUTO_INCREMENT,
  "email" varchar(255) NOT NULL,
  "email_status" enum('verified','unverified') NOT NULL,
  "password" varchar(255) NOT NULL,
  "created_at" datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY ("id"),
  UNIQUE KEY "email" ("email")
);

SET FOREIGN_KEY_CHECKS = 1;
