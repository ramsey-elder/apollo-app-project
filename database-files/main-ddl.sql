USE sys;

DROP DATABASE IF EXISTS apollo_booking;
CREATE DATABASE IF NOT EXISTS apollo_booking;
USE apollo_booking;

DROP TABLE IF EXISTS users;
CREATE TABLE users
(
    user_id   INT AUTO_INCREMENT PRIMARY KEY,
    f_name    VARCHAR(50)                                           NOT NULL,
    l_name    VARCHAR(50)                                           NOT NULL,
    email     VARCHAR(100)                                          NOT NULL UNIQUE,
    user_type ENUM ('student', 'admin', 'data_analyst') NOT NULL
);

DROP TABLE IF EXISTS buildings;
CREATE TABLE buildings
(
    building_id   INT AUTO_INCREMENT PRIMARY KEY,
    building_name VARCHAR(100) NOT NULL,
    street        VARCHAR(100) NOT NULL,
    city          VARCHAR(50)  NOT NULL,
    state         VARCHAR(2)   NOT NULL,
    zip           VARCHAR(10)  NOT NULL,
    creator_id    INT          NOT NULL,
    FOREIGN KEY (creator_id) REFERENCES users (user_id)
);

DROP TABLE IF EXISTS clubs;
CREATE TABLE clubs
(
    club_id     INT AUTO_INCREMENT PRIMARY KEY,
    club_name   VARCHAR(100) NOT NULL,
    description TEXT,
    email       VARCHAR(50)  NOT NULL,
    suspended   TINYINT(1)   NOT NULL
);

DROP TABLE IF EXISTS spaces;
CREATE TABLE spaces
(
    space_id           INT AUTO_INCREMENT PRIMARY KEY,
    permissions        ENUM ('club', 'all')                                                   NOT NULL,
    availability_start TIME                                                                   NOT NULL,
    availability_end   TIME                                                                   NOT NULL,
    space_type         ENUM ('room', 'dance_studio', 'field', 'lecture_hall', 'music_studio') NOT NULL,
    room_name          VARCHAR(50)                                                            NOT NULL,
    size               ENUM ('small', 'medium', 'large'),
    creator_id         INT                                                                    NOT NULL,
    building_id        INT                                                                    NOT NULL,
    FOREIGN KEY (creator_id) REFERENCES users (user_id),
    FOREIGN KEY (building_id) REFERENCES buildings (building_id)
);

DROP TABLE IF EXISTS club_reps;
CREATE TABLE club_reps
(
    club_id INT,
    user_id INT,
    PRIMARY KEY (club_id, user_id),
    FOREIGN KEY (club_id) REFERENCES clubs (club_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

DROP TABLE IF EXISTS facility_managers;
CREATE TABLE facility_managers
(
    manager_id  INT AUTO_INCREMENT PRIMARY KEY,
    f_name      VARCHAR(50)  NOT NULL,
    l_name      VARCHAR(50)  NOT NULL,
    email       VARCHAR(100) NOT NULL UNIQUE,
    phone       VARCHAR(15),
    building_id INT          NOT NULL,
    FOREIGN KEY (building_id) REFERENCES buildings (building_id)
);

DROP TABLE IF EXISTS accommodations;
CREATE TABLE accommodations
(
    space_id     INT PRIMARY KEY,
    whiteboard   BOOLEAN DEFAULT FALSE,
    screen       BOOLEAN DEFAULT FALSE,
    desks        BOOLEAN DEFAULT FALSE,
    sound_system BOOLEAN DEFAULT FALSE,
    tables_avail BOOLEAN DEFAULT FALSE,
    camera       BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (space_id) REFERENCES spaces (space_id)
);

DROP TABLE IF EXISTS bookings;
CREATE TABLE bookings
(
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    status     ENUM ('active', 'cancelled', 'completed', 'no_show') NOT NULL DEFAULT 'active',
    time_start DATETIME                                             NOT NULL,
    time_end   DATETIME                                             NOT NULL,
    approved   TINYINT(1)                                           NOT NULL DEFAULT 0,
    space_id   INT                                                  NOT NULL,
    club_id    INT,
    creator_id INT                                                  NOT NULL,
    FOREIGN KEY (space_id) REFERENCES spaces (space_id),
    FOREIGN KEY (club_id) REFERENCES clubs (club_id),
    FOREIGN KEY (creator_id) REFERENCES users (user_id)
);

DROP TABLE IF EXISTS help_tickets;
CREATE TABLE help_tickets (
    ticket_id     INT AUTO_INCREMENT PRIMARY KEY,
    ticket_type   VARCHAR(50) NOT NULL,
    title         VARCHAR(100) NOT NULL,
    description   TEXT,
    created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    closed_at     DATETIME,
    admin_id      INT,
    creator_id    INT NOT NULL,
    FOREIGN KEY (admin_id) REFERENCES users(user_id),
    FOREIGN KEY (creator_id) REFERENCES users(user_id)
);


DROP TABLE IF EXISTS booking_participants;
CREATE TABLE booking_participants
(
    booking_id INT,
    user_id    INT,
    managing   TINYINT(1) NOT NULL DEFAULT 0,
    PRIMARY KEY (booking_id, user_id),
    FOREIGN KEY (booking_id) REFERENCES bookings (booking_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

DROP TABLE IF EXISTS events;
CREATE TABLE events
(
    event_id    INT AUTO_INCREMENT PRIMARY KEY,
    event_name  VARCHAR(100) NOT NULL,
    event_type  VARCHAR(50)  NOT NULL,
    description TEXT,
    booking_id  INT          NOT NULL,
    FOREIGN KEY (booking_id) REFERENCES bookings (booking_id)
);

DROP TABLE IF EXISTS features;
CREATE TABLE features
(
    event_id      INT PRIMARY KEY,
    nupd          BOOLEAN DEFAULT FALSE,
    catering      BOOLEAN DEFAULT FALSE,
    photographer  BOOLEAN DEFAULT FALSE,
    folding_table BOOLEAN DEFAULT FALSE,
    emt           BOOLEAN DEFAULT FALSE,
    sound_system  BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (event_id) REFERENCES events (event_id)
);