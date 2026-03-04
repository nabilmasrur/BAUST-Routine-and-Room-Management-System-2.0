-- BAUST Routine Management System Database
-- Created for: Abu Nabil MD. Masrur
-- Date: 2024

SET FOREIGN_KEY_CHECKS = 0;

-- Create Database
CREATE DATABASE IF NOT EXISTS `baust_routine` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `baust_routine`;

-- Table structure for table `departments`
CREATE TABLE `departments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `code` varchar(10) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table `teachers`
CREATE TABLE `teachers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `short_name` varchar(10) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `department_id` int(11) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `short_name` (`short_name`),
  KEY `department_id` (`department_id`),
  CONSTRAINT `teachers_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table `rooms`
CREATE TABLE `rooms` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `room_number` varchar(20) NOT NULL,
  `capacity` int(11) NOT NULL,
  `room_type` enum('classroom','lab') NOT NULL,
  `has_projector` tinyint(1) DEFAULT 0,
  `has_ac` tinyint(1) DEFAULT 0,
  `is_available` tinyint(1) DEFAULT 1,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `room_number` (`room_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table `courses`
CREATE TABLE `courses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_code` varchar(20) NOT NULL,
  `title` varchar(200) NOT NULL,
  `credit` decimal(3,1) NOT NULL,
  `department_id` int(11) DEFAULT NULL,
  `is_lab` tinyint(1) DEFAULT 0,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `course_code` (`course_code`),
  KEY `department_id` (`department_id`),
  CONSTRAINT `courses_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table `routines`
CREATE TABLE `routines` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `department_id` int(11) DEFAULT NULL,
  `semester` enum('Summer','Winter') NOT NULL,
  `year` int(11) NOT NULL,
  `level_term` varchar(10) NOT NULL,
  `section` varchar(5) NOT NULL,
  `advisor_name` varchar(100) NOT NULL,
  `advisor_phone` varchar(15) NOT NULL,
  `dpc_name` varchar(100) DEFAULT NULL,
  `dpc_phone` varchar(15) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `department_id` (`department_id`),
  CONSTRAINT `routines_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table `schedules`
CREATE TABLE `schedules` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `routine_id` int(11) DEFAULT NULL,
  `course_id` int(11) DEFAULT NULL,
  `teacher_id` int(11) DEFAULT NULL,
  `room_id` int(11) DEFAULT NULL,
  `day_of_week` enum('Sunday','Monday','Tuesday','Wednesday','Thursday') NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `duration_hours` int(11) DEFAULT 1,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `routine_id` (`routine_id`),
  KEY `course_id` (`course_id`),
  KEY `teacher_id` (`teacher_id`),
  KEY `room_id` (`room_id`),
  CONSTRAINT `schedules_ibfk_1` FOREIGN KEY (`routine_id`) REFERENCES `routines` (`id`) ON DELETE CASCADE,
  CONSTRAINT `schedules_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`),
  CONSTRAINT `schedules_ibfk_3` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`),
  CONSTRAINT `schedules_ibfk_4` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table `users`
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `role` enum('admin','faculty') DEFAULT 'faculty',
  `department_id` int(11) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  KEY `department_id` (`department_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for table `departments`
INSERT INTO `departments` (`id`, `name`, `code`, `created_at`) VALUES
(1, 'Computer Science & Engineering', 'CSE', NOW()),
(2, 'Electrical & Electronic Engineering', 'EEE', NOW()),
(3, 'Industrial & Production Engineering', 'IPE', NOW()),
(4, 'Information & Communication Technology', 'ICT', NOW()),
(5, 'Mechanical Engineering', 'ME', NOW()),
(6, 'Business Administration', 'BBA', NOW()),
(7, 'Department of English', 'ENGLISH', NOW());

-- Dumping data for table `teachers`
INSERT INTO `teachers` (`id`, `short_name`, `full_name`, `department_id`, `email`, `phone`, `is_active`) VALUES
(1, 'AKZ', 'Abdullah Al Kafi Zaman', 1, 'akz@baust.edu.bd', '01784055149', 1),
(2, 'KS', 'Md. Khalid Syfullah', 1, 'ks@baust.edu.bd', '01712345678', 1),
(3, 'RA', 'Rifat Ahmed', 1, 'ra@baust.edu.bd', '01787654321', 1),
(4, 'JB', 'Jahangir Badsha', 1, 'jb@baust.edu.bd', '01711223344', 1),
(5, 'RR', 'Rafsan Reza', 1, 'rr@baust.edu.bd', '01755667788', 1),
(6, 'SIA', 'Syed Iftekhar Ahmed', 1, 'sia@baust.edu.bd', '01799887766', 1);

-- Dumping data for table `rooms`
INSERT INTO `rooms` (`id`, `room_number`, `capacity`, `room_type`, `has_projector`, `has_ac`, `is_available`) VALUES
(1, '101', 50, 'classroom', 1, 1, 1),
(2, '102', 45, 'classroom', 1, 0, 1),
(3, '201', 40, 'classroom', 0, 1, 1),
(4, '202', 35, 'classroom', 1, 0, 1),
(5, '304', 30, 'lab', 1, 1, 1),
(6, '411', 25, 'classroom', 1, 0, 1),
(7, 'Lab-1', 20, 'lab', 1, 1, 1),
(8, 'Lab-2', 25, 'lab', 1, 0, 1);

-- Dumping data for table `courses`
INSERT INTO `courses` (`id`, `course_code`, `title`, `credit`, `department_id`, `is_lab`) VALUES
(1, 'CSE 2201', 'Data Structures and Algorithms II', 3.0, 1, 0),
(2, 'CSE 2202', 'Data Structures and Algorithms II Sessional', 1.5, 1, 1),
(3, 'CSE 2203', 'Theory of Computation', 3.0, 1, 0),
(4, 'CSE 2205', 'Digital Logic Design', 3.0, 1, 0),
(5, 'CSE 2206', 'Digital Logic Design Sessional', 1.5, 1, 1),
(6, 'MATH 2247', 'Math-IV', 3.0, 1, 0),
(7, 'HUM 2249', 'Engineering Ethics', 2.0, 1, 0),
(8, 'EEE 3101', 'Power Systems', 3.0, 2, 0),
(9, 'EEE 3102', 'Control Systems', 3.0, 2, 0);

-- Dumping data for table `routines`
INSERT INTO `routines` (`id`, `department_id`, `semester`, `year`, `level_term`, `section`, `advisor_name`, `advisor_phone`, `dpc_name`, `dpc_phone`) VALUES
(1, 1, 'Summer', 2025, '2-II', 'B', 'Anite Halim Sagor', '01784055149', 'Dr. Mohammad Ali', '01712345678'),
(2, 2, 'Winter', 2025, '3-I', 'A', 'Dr. Rahman', '01712345678', 'Dr. Ahmed Hussain', '01787654321');

-- Dumping data for table `schedules`
INSERT INTO `schedules` (`id`, `routine_id`, `course_id`, `teacher_id`, `room_id`, `day_of_week`, `start_time`, `end_time`, `duration_hours`) VALUES
(1, 1, 1, 1, 1, 'Sunday', '08:00:00', '09:00:00', 1),
(2, 1, 2, 2, 5, 'Monday', '10:00:00', '11:30:00', 2),
(3, 1, 3, 3, 2, 'Tuesday', '11:30:00', '12:30:00', 1);

-- Dumping data for table `users`
INSERT INTO `users` (`id`, `username`, `email`, `password_hash`, `full_name`, `role`, `department_id`, `is_active`) VALUES
(1, 'admin', 'admin@baust.edu.bd', '$2b$12$LQv3c1yqBWVHxkd5L6CQ/O6L6CkS7cK7p6c6p6c6p6c6p6c6p6c6', 'System Administrator', 'admin', 1, 1),
(2, 'nabil', 'nabil@baust.edu.bd', '$2b$12$LQv3c1yqBWVHxkd5L6CQ/O6L6CkS7cK7p6c6p6c6p6c6p6c6p6c6', 'Abu Nabil MD. Masrur', 'admin', 1, 1);

SET FOREIGN_KEY_CHECKS = 1;