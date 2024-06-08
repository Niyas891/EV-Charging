-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 09, 2023 at 07:07 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `ev_charging`
--

-- --------------------------------------------------------

--
-- Table structure for table `ev_admin`
--

CREATE TABLE `ev_admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ev_admin`
--

INSERT INTO `ev_admin` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `ev_booking`
--

CREATE TABLE `ev_booking` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `station` varchar(30) NOT NULL,
  `carno` varchar(20) NOT NULL,
  `reserve` varchar(20) NOT NULL,
  `slot` int(11) NOT NULL,
  `cimage` varchar(20) NOT NULL,
  `mins` int(11) NOT NULL,
  `plan` int(11) NOT NULL,
  `amount` double NOT NULL,
  `rtime` varchar(20) NOT NULL,
  `etime` varchar(20) NOT NULL,
  `rdate` varchar(15) NOT NULL,
  `edate` varchar(15) NOT NULL,
  `otp` varchar(10) NOT NULL,
  `charge` double NOT NULL,
  `charge_time` int(11) NOT NULL,
  `charge_min` int(11) NOT NULL,
  `charge_sec` int(11) NOT NULL,
  `charge_st` int(11) NOT NULL,
  `pay_mode` varchar(20) NOT NULL,
  `pay_st` int(11) NOT NULL,
  `sms_st` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `btime1` varchar(20) NOT NULL,
  `btime2` varchar(20) NOT NULL,
  `alert_st` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ev_booking`
--

INSERT INTO `ev_booking` (`id`, `uname`, `station`, `carno`, `reserve`, `slot`, `cimage`, `mins`, `plan`, `amount`, `rtime`, `etime`, `rdate`, `edate`, `otp`, `charge`, `charge_time`, `charge_min`, `charge_sec`, `charge_st`, `pay_mode`, `pay_st`, `sms_st`, `status`, `btime1`, `btime2`, `alert_st`) VALUES
(1, 'dinesh', '1', 'TN5566', '1', 2, 'evch.jpg', 0, 0, 0, '14:15:09', '', '02-04-2023', '', '', 0, 0, 0, 0, 0, '', 0, 0, 1, '18:45', '19:10', 7),
(2, 'dinesh', '2', 'TN4548', '1', 3, 'evch.jpg', 0, 0, 0, '11:50:35', '', '07-04-2023', '', '', 0, 0, 0, 0, 0, '', 0, 0, 1, '11:50', '11:55', 7);

-- --------------------------------------------------------

--
-- Table structure for table `ev_register`
--

CREATE TABLE `ev_register` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `address` varchar(40) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `account` varchar(20) NOT NULL,
  `card` varchar(20) NOT NULL,
  `bank` varchar(20) NOT NULL,
  `amount` double NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `latitude` varchar(20) NOT NULL,
  `longitude` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ev_register`
--

INSERT INTO `ev_register` (`id`, `name`, `address`, `mobile`, `email`, `account`, `card`, `bank`, `amount`, `uname`, `pass`, `latitude`, `longitude`) VALUES
(1, 'Rahul', 'Salem', 6381082863, 'rahul@gmail.com', '2200774433', '270600042828', 'SBI', 10000, 'rahul', '123456', '13.0703', '80.2691'),
(2, 'Dinesh', '75, MK Road', 9894442716, 'dinesh@gmail.com', '2356897414', '2257451548789454', 'SBI', 10000, 'dinesh', '123456', '10.836283', '78.689255'),
(3, 'Vinay', '22,FF', 9894442716, 'vinay@gmail.com', '25586554455', '4255865555522455', 'SBI', 10000, 'vinay', '123456', '13.0703', '80.2691');

-- --------------------------------------------------------

--
-- Table structure for table `ev_slot`
--

CREATE TABLE `ev_slot` (
  `id` int(11) NOT NULL,
  `station` varchar(20) NOT NULL,
  `slot` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ev_slot`
--

INSERT INTO `ev_slot` (`id`, `station`, `slot`) VALUES
(1, '1', 1),
(2, '1', 2),
(3, '1', 3),
(4, '1', 4),
(5, '1', 5),
(6, '2', 1),
(7, '2', 2),
(8, '2', 3),
(9, '3', 1),
(10, '3', 2),
(11, '3', 3),
(12, '3', 4),
(13, '3', 5);

-- --------------------------------------------------------

--
-- Table structure for table `ev_station`
--

CREATE TABLE `ev_station` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `stype` varchar(20) NOT NULL,
  `num_charger` int(11) NOT NULL,
  `area` varchar(30) NOT NULL,
  `city` varchar(30) NOT NULL,
  `lat` varchar(20) NOT NULL,
  `lon` varchar(20) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `status` int(11) NOT NULL,
  `landmark` varchar(30) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `distance` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ev_station`
--

INSERT INTO `ev_station` (`id`, `name`, `stype`, `num_charger`, `area`, `city`, `lat`, `lon`, `uname`, `pass`, `status`, `landmark`, `mobile`, `email`, `distance`) VALUES
(1, 'Evstation1', 'Private', 5, 'SS Road', 'Trichy', '13.0703', '80.2691', 'station1', '123456', 1, 'Bus Stand', 9638528847, 'evstation1@gmail.com', 13),
(2, 'Evstation2', 'Private', 3, 'DD Nagar', 'Trichy', '10.815771', '78.697214', 'station2', '123456', 1, 'Market', 9638577584, 'evstation2@gmail.com', 13),
(3, 'Evstation3', 'Private', 5, 'FF Road', 'Trichy', '10.836396', '78.688743', 'station3', '123456', 1, 'Bus Stand', 9638527412, 'evstation@gmail.com', 0);
