import pymysql

commands = (

    """CREATE TABLE IF NOT EXISTS `mydb`.`Users` (
      `User_id` INT(11) NOT NULL,
      `login` VARCHAR(45) NULL DEFAULT NULL,
      `password` VARCHAR(45) NULL DEFAULT NULL,
      `first_name` VARCHAR(45) NULL DEFAULT NULL,
      `last_name` VARCHAR(45) NULL DEFAULT NULL,
      PRIMARY KEY (`User_id`))
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8""",

    """CREATE TABLE IF NOT EXISTS `mydb`.`Blog` (
      `Blog_id` INT(11) NOT NULL,
      `User_id` INT(11) NOT NULL,
      `name` VARCHAR(45) NULL DEFAULT NULL,
      `deleted` TINYINT(1) NULL DEFAULT '0',
      PRIMARY KEY (`Blog_id`),
      INDEX `fk_Blog_1_idx` (`User_id` ASC),
      CONSTRAINT `fk_Blog_1`
        FOREIGN KEY (`User_id`)
        REFERENCES `mydb`.`Users` (`User_id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8""",

    """CREATE TABLE IF NOT EXISTS `mydb`.`Post` (
      `Post_id` INT(11) NOT NULL,
      `User_id` INT(11) NULL DEFAULT NULL,
      `headline` VARCHAR(45) NULL DEFAULT NULL,
      `text` VARCHAR(45) NULL DEFAULT NULL,
      `deleted` TINYINT(1) NULL DEFAULT '0',
      PRIMARY KEY (`Post_id`),
      INDEX `User_id_idx` (`User_id` ASC),
      CONSTRAINT `User_id`
        FOREIGN KEY (`User_id`)
        REFERENCES `mydb`.`Users` (`User_id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8""",

    """CREATE TABLE IF NOT EXISTS `mydb`.`Comment` (
      `id` INT(11) NOT NULL,
      `Post_id` INT(11) NOT NULL,
      `Сom_id` INT(11) NULL DEFAULT '0',
      `User_id` INT(11) NOT NULL,
      `text` VARCHAR(45) NULL DEFAULT NULL,
      PRIMARY KEY (`id`),
      INDEX `fk_Comment_1_idx` (`User_id` ASC),
      INDEX `fk_Comment_2_idx` (`Post_id` ASC),
      INDEX `fk_Comment_3_idx` (`Сom_id` ASC),
      CONSTRAINT `fk_Comment_1`
        FOREIGN KEY (`User_id`)
        REFERENCES `mydb`.`Users` (`User_id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
      CONSTRAINT `fk_Comment_2`
        FOREIGN KEY (`Post_id`)
        REFERENCES `mydb`.`Post` (`Post_id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
      CONSTRAINT `fk_Comment_3`
        FOREIGN KEY (`Сom_id`)
        REFERENCES `mydb`.`Comment` (`id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8""",

    """CREATE TABLE IF NOT EXISTS `mydb`.`Post_list` (
      `id` INT(11) NOT NULL,
      `Post_id` INT(11) NOT NULL,
      `Blog_id` INT(11) NOT NULL,
      PRIMARY KEY (`id`),
      INDEX `fk_Post_list_1_idx` (`Post_id` ASC),
      INDEX `fk_Post_list_2_idx` (`Blog_id` ASC),
      CONSTRAINT `fk_Post_list_1`
        FOREIGN KEY (`Post_id`)
        REFERENCES `mydb`.`Post` (`Post_id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
      CONSTRAINT `fk_Post_list_2`
        FOREIGN KEY (`Blog_id`)
        REFERENCES `mydb`.`Blog` (`Blog_id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8""",

    """CREATE TABLE IF NOT EXISTS `mydb`.`Session` (
      `Session_id` INT(11) NOT NULL,
      `User_id` INT(11) NOT NULL,
      `session` VARCHAR(45) NULL DEFAULT NULL,
      PRIMARY KEY (`Session_id`),
      INDEX `fk_Session_1_idx` (`User_id` ASC),
      CONSTRAINT `fk_Session_1`
        FOREIGN KEY (`User_id`)
        REFERENCES `mydb`.`Users` (`User_id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8""")


def create_tables():
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='root',
                                 db='mydb',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    for command in commands:
        cursor.execute(command)
