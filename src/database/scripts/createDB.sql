DROP DATABASE IF EXISTS MLM_DB;
CREATE DATABASE MLM_DB;

use MLM_DB;

CREATE USER 'm_user' IDENTIFIED BY 'a:123456';
GRANT SELECT, INSERT, UPDATE, DELETE, EXECUTE ON MLM_DB.* TO 'm_user';
FLUSH PRIVILEGES;
-- verify user has been created
select host, user from mysql.user;

DROP TABLE IF EXISTS MLM_DB.users;
DROP TABLE IF EXISTS MLM_DB.books;


CREATE TABLE `users` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `email` VARCHAR(64) NOT NULL,
    `name` VARCHAR(64) NOT NULL,
    `is_admin` BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (`id`),
    UNIQUE KEY `email_unique_idx` (`email`)
)  ENGINE=INNODB DEFAULT CHARSET=LATIN1 COMMENT='This table stores all users';

INSERT INTO `MLM_DB`.`users` (`email`, `name`, `is_admin`) VALUES ('sara@gmail.com', 'sara', true);

CREATE TABLE `books` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `book_title` varchar(64) NOT NULL,
  `author_name`  varchar(64) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `checked_out_date`  DATETIME(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `book_title_unique_idx` (`book_title`),
  CONSTRAINT user_id_fk FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='This table stores book information';

commit;
