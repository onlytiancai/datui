CREATE TABLE IF NOT EXISTS `Liwu_Items` (
  `ItemId` bigint(20) NOT NULL,
  `UserSinaUserId` bigint(20) NOT NULL,
  `Text` varchar(512) NOT NULL,
  `SinaUserName` varchar(64) NOT NULL,
  `CreateTime` datetime NOT NULL,
  `ThumbnailPic` varchar(512) NOT NULL,
  `BmiddlePic` varchar(512) NOT NULL,
  `OriginalPc` varchar(512) NOT NULL,
  `UserHeaderPic` varchar(512) NOT NULL,
  `Hits` int(11) NOT NULL,
  `Sell` tinyint(1) NOT NULL,
  `Recommend` tinyint(1) NOT NULL,
  UNIQUE KEY `ItemId` (`ItemId`),
  KEY `CreateTime` (`CreateTime`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `Liwu_Likes` (
  `SinaUserId` bigint(20) NOT NULL,
  `ItemId` bigint(20) NOT NULL,
  KEY `SinaUserId` (`SinaUserId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
