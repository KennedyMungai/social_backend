-- Active: 1678836168521@@127.0.0.1@3306@social_backend

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

-- A drop table query

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

-- DROP TABLE posts;

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

-- Created the posts table

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

CREATE TABLE
    IF NOT EXISTS posts (
        id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        title VARCHAR(255) NOT NULL,
        content VARCHAR(255),
        published BOOLEAN,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

-- Imserting data to the posts table

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

INSERT INTO posts VALUES("") 