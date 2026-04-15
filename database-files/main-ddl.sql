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
    user_type ENUM ('student', 'club_rep', 'admin', 'data_analyst') NOT NULL
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

-- ============================================================
-- Apollo Booking – Sample Data

-- ------------------------------------------------------------
-- users  (no FKs)
-- ------------------------------------------------------------
INSERT INTO users (f_name, l_name, email, user_type) VALUES
    ('Sarah',  'Chen',    'chen.sar@northeastern.edu',    'admin'),
    ('Marcus', 'Webb',    'webb.ma@northeastern.edu',     'student'),
    ('Priya',  'Nair',    'nair.pr@northeastern.edu',     'club_rep'),
    ('Jordan', 'Ellis',   'ellis.jo@northeastern.edu',    'data_analyst'),
    ('Tyler',  'Okafor',  'okafor.ty@northeastern.edu',   'student');

-- ------------------------------------------------------------
-- buildings  (FK → users.creator_id)
-- ------------------------------------------------------------
INSERT INTO buildings (building_name, street, city, state, zip, creator_id) VALUES
    ('Curry Student Center',   '346 Huntington Ave',  'Boston', 'MA', '02115', 1),
    ('Marino Recreation Center','259 Huntington Ave', 'Boston', 'MA', '02115', 1),
    ('Shillman Hall',           '115 Forsyth St',     'Boston', 'MA', '02115', 1);

-- ------------------------------------------------------------
-- clubs  (no FKs)
-- ------------------------------------------------------------
INSERT INTO clubs (club_name, description, email, suspended) VALUES
    ('NEU Robotics Club',     'Builds and competes with autonomous robots.',   'robotics@northeastern.edu',     0),
    ('NEU Squash Club',       'Competitive and recreational squash team.',     'squash@northeastern.edu',       0),
    ('NEU Photography Club',  'Campus photography community and darkroom use.','photography@northeastern.edu',  0);

-- ------------------------------------------------------------
-- spaces  (FK → users.creator_id, buildings.building_id)
-- ------------------------------------------------------------
INSERT INTO spaces (permissions, availability_start, availability_end, space_type, room_name, size, creator_id, building_id) VALUES
    ('all',  '08:00:00', '22:00:00', 'room',          '340 Multipurpose Room', 'medium', 1, 1),
    ('club', '07:00:00', '21:00:00', 'dance_studio',  'Studio A',              'large',  1, 2),
    ('all',  '09:00:00', '20:00:00', 'lecture_hall',  'Shillman 105',          'large',  1, 3);

-- ------------------------------------------------------------
-- club_reps  (FK → clubs, users)
-- ------------------------------------------------------------
INSERT INTO club_reps (club_id, user_id) VALUES
    (1, 3),   -- Priya is rep for Robotics
    (2, 3),   -- Priya is rep for Squash
    (3, 3);   -- Priya is rep for Photography

-- ------------------------------------------------------------
-- facility_managers  (FK → buildings)
-- ------------------------------------------------------------
INSERT INTO facility_managers (f_name, l_name, email, phone, building_id) VALUES
    ('David',  'Park',   'dpark@northeastern.edu',  '617-555-0101', 1),
    ('Angela', 'Torres', 'atorres@northeastern.edu','617-555-0182', 2);

-- ------------------------------------------------------------
-- accommodations  (FK → spaces.space_id; one row per space)
-- ------------------------------------------------------------
INSERT INTO accommodations (space_id, whiteboard, screen, desks, sound_system, tables_avail, camera) VALUES
    (1, TRUE,  TRUE,  TRUE,  FALSE, TRUE,  FALSE),
    (2, FALSE, FALSE, FALSE, TRUE,  FALSE, TRUE),
    (3, TRUE,  TRUE,  TRUE,  TRUE,  TRUE,  TRUE);

-- ------------------------------------------------------------
-- bookings  (FK → spaces, clubs, users)
-- ------------------------------------------------------------
INSERT INTO bookings (status, time_start, time_end, approved, space_id, club_id, creator_id) VALUES
    ('active',    '2026-04-10 14:00:00', '2026-04-10 16:00:00', 1, 1, 1, 2),  -- Marcus books room for Robotics
    ('active',    '2026-04-11 09:00:00', '2026-04-11 11:00:00', 1, 2, 2, 3),  -- Priya books studio for Squash
    ('completed', '2026-04-05 10:00:00', '2026-04-05 12:00:00', 1, 3, NULL, 2); -- Marcus booked lecture hall (no club)

-- ------------------------------------------------------------
-- help_tickets  (FK → users: admin_id nullable, creator_id)
-- ------------------------------------------------------------
INSERT INTO help_tickets (ticket_type, title, description, admin_id, creator_id) VALUES
    ('booking_issue', 'Cannot cancel booking #1',
     'I submitted a cancellation but the status has not changed.', 1, 2),
    ('access_request', 'Request access to Studio A',
     'Our club needs recurring access to the dance studio on weekends.', 1, 3);

-- ------------------------------------------------------------
-- booking_participants  (FK → bookings, users)
-- ------------------------------------------------------------
INSERT INTO booking_participants (booking_id, user_id, managing) VALUES
    (1, 2, 1),   -- Marcus manages booking 1
    (1, 5, 0),   -- Tyler is a participant in booking 1
    (2, 3, 1);   -- Priya manages booking 2

-- ------------------------------------------------------------
-- events  (FK → bookings)
-- ------------------------------------------------------------
INSERT INTO events (event_name, event_type, description, booking_id) VALUES
    ('Spring Robotics Demo',      'showcase',  'Public demo of semester robot builds.',       1),
    ('Squash Intramural Tryouts', 'tryout',    'Open tryouts for the spring intramural team.', 2);

-- ------------------------------------------------------------
-- features  (FK → events.event_id; one row per event)
-- ------------------------------------------------------------
INSERT INTO features (event_id, nupd, catering, photographer, folding_table, emt, sound_system) VALUES
    (1, TRUE,  FALSE, TRUE,  TRUE,  FALSE, FALSE),
    (2, FALSE, FALSE, FALSE, FALSE, TRUE,  FALSE);

--- PERSONA 1: SYSTEM ADMIN (Adam)

-- 1.1  View all current and upcoming bookings across all spaces
SELECT b.booking_id,
       b.status,
       b.time_start,
       b.time_end,
       b.approved,
       s.room_name,
       s.space_type,
       bl.building_name,
       u.f_name,
       u.l_name,
       c.club_name
  FROM bookings b
  JOIN spaces s    ON b.space_id   = s.space_id
  JOIN buildings bl ON s.building_id = bl.building_id
  JOIN users u     ON b.creator_id  = u.user_id
  LEFT JOIN clubs c ON b.club_id    = c.club_id
 WHERE b.status = 'active'
   AND b.time_end >= NOW()
 ORDER BY b.time_start;

-- 1.2  Cancel or update an existing booking (example: cancel booking 5)
UPDATE bookings
   SET status = 'cancelled'
 WHERE booking_id = 5;

-- 1.3  Add a new bookable space to the system
INSERT INTO spaces (permissions, availability_start, availability_end,
                    space_type, room_name, size, creator_id, building_id)
VALUES ('all', '08:00:00', '22:00:00',
        'room', 'New Study Room 101', 'medium', 1, 2);

-- 1.4  Deactivate / remove an existing space
DELETE FROM spaces
 WHERE space_id = 10;

-- 1.5  Approve a user-requested unconventional space (via help ticket)
--      An admin reviews open space-request tickets and closes them
SELECT ht.ticket_id,
       ht.title,
       ht.description,
       ht.created_at,
       u.f_name,
       u.l_name
  FROM help_tickets ht
  JOIN users u ON ht.creator_id = u.user_id
 WHERE ht.ticket_type = 'space_request'
   AND ht.closed_at IS NULL;

-- 1.6  View and remove registered users
--      View all users:
SELECT user_id,
       f_name,
       l_name,
       email,
       user_type
  FROM users
 ORDER BY l_name, f_name;

--      Remove a specific user:
DELETE FROM users
 WHERE user_id = 12;

-- PERSONA 2: DATA ANALYST (Michael)

-- 2.1  View aggregated booking data across all spaces and time periods
SELECT s.room_name,
       bl.building_name,
       s.space_type,
       COUNT(b.booking_id)                          AS total_bookings,
       ROUND(AVG(TIMESTAMPDIFF(MINUTE,
             b.time_start, b.time_end)), 0)          AS avg_duration_min,
       DATE_FORMAT(b.time_start, '%Y-%m')            AS booking_month
  FROM bookings b
  JOIN spaces s     ON b.space_id    = s.space_id
  JOIN buildings bl ON s.building_id = bl.building_id
 GROUP BY s.room_name, bl.building_name, s.space_type, booking_month
 ORDER BY booking_month, total_bookings DESC;

-- 2.2  Filter booking data by building, space type, and user type
SELECT bl.building_name,
       s.space_type,
       u.user_type,
       COUNT(b.booking_id) AS total_bookings
  FROM bookings b
  JOIN spaces s     ON b.space_id    = s.space_id
  JOIN buildings bl ON s.building_id = bl.building_id
  JOIN users u      ON b.creator_id  = u.user_id
 WHERE bl.building_name = 'Snell Library'
   AND s.space_type     = 'room'
   AND u.user_type      = 'student'
 GROUP BY bl.building_name, s.space_type, u.user_type;

-- 2.3  See which buildings are consistently underused
SELECT bl.building_name,
       COUNT(b.booking_id) AS total_bookings,
       COUNT(DISTINCT s.space_id) AS total_spaces,
       ROUND(COUNT(b.booking_id) / COUNT(DISTINCT s.space_id), 2)
                            AS bookings_per_space
  FROM buildings bl
  JOIN spaces s     ON bl.building_id = s.building_id
  LEFT JOIN bookings b ON s.space_id  = b.space_id
                      AND b.status    = 'active'
 GROUP BY bl.building_name
 ORDER BY bookings_per_space ASC;

-- 2.4  Flag irregular booking patterns (repeated no-shows)
SELECT u.user_id,
       u.f_name,
       u.l_name,
       u.email,
       COUNT(b.booking_id) AS no_show_count
  FROM bookings b
  JOIN users u ON b.creator_id = u.user_id
 WHERE b.status = 'no_show'
 GROUP BY u.user_id, u.f_name, u.l_name, u.email
HAVING no_show_count >= 3
 ORDER BY no_show_count DESC;

-- 2.5  Export booking reports (select all detail for CSV/report export)
SELECT b.booking_id,
       b.status,
       b.time_start,
       b.time_end,
       b.approved,
       s.room_name,
       s.space_type,
       s.size,
       bl.building_name,
       bl.city,
       u.f_name       AS creator_first,
       u.l_name       AS creator_last,
       u.user_type,
       c.club_name
  FROM bookings b
  JOIN spaces s      ON b.space_id    = s.space_id
  JOIN buildings bl  ON s.building_id = bl.building_id
  JOIN users u       ON b.creator_id  = u.user_id
  LEFT JOIN clubs c  ON b.club_id     = c.club_id
 ORDER BY b.time_start;

-- 2.6  View cancellation rates and trends
SELECT DATE_FORMAT(b.time_start, '%Y-%m')           AS booking_month,
       COUNT(b.booking_id)                           AS total_bookings,
       SUM(b.status = 'cancelled')                   AS cancelled_count,
       ROUND(SUM(b.status = 'cancelled')
             / COUNT(b.booking_id) * 100, 2)         AS cancellation_rate
  FROM bookings b
 GROUP BY booking_month
 ORDER BY booking_month;

-- PERSONA 3: CLUB REPRESENTATIVE (Maddie)

-- 3.1  Book a space weekly for club practice
INSERT INTO bookings (status, time_start, time_end, approved,
                      space_id, club_id, creator_id)
VALUES ('active', '2026-04-13 18:00:00', '2026-04-13 20:00:00', 0,
        3, 2, 7);

-- 3.2  Cancel or adjust one of the club's bookings
UPDATE bookings
   SET status = 'cancelled'
 WHERE booking_id = 15
   AND club_id    = 2;

-- 3.3  Request an unconventional space via the Help Page
INSERT INTO help_tickets (ticket_type, title, description, creator_id)
VALUES ('space_request',
        'Request to book Blackman Lobby',
        'The Dance Club needs extra practice space during performance season. '
        'Requesting access to Blackman Lobby on weekday evenings.',
        7);

-- 3.4  Book a large field to accommodate 100+ people for the club
INSERT INTO bookings (status, time_start, time_end, approved,
                      space_id, club_id, creator_id)
SELECT 'active', '2026-04-20 14:00:00', '2026-04-20 17:00:00', 0,
       s.space_id, 2, 7
  FROM spaces s
 WHERE s.space_type = 'field'
   AND s.size       = 'large'
 LIMIT 1;

-- 3.5  Trade bookings with another club
--      (Two-step swap: reassign booking 20 from club 2 → club 5,
--       and booking 25 from club 5 → club 2)
UPDATE bookings
   SET club_id = CASE booking_id
                     WHEN 20 THEN 5
                     WHEN 25 THEN 2
                 END
 WHERE booking_id IN (20, 25);

-- 3.6  See the size of spaces around campus
SELECT s.room_name,
       s.space_type,
       s.size,
       bl.building_name
  FROM spaces s
  JOIN buildings bl ON s.building_id = bl.building_id
 ORDER BY bl.building_name, s.size;

-- PERSONA 4: STUDENT (Jason)

-- 4.1  View real-time availability of all campus spaces
SELECT s.space_id,
       s.room_name,
       s.space_type,
       s.size,
       bl.building_name,
       s.availability_start,
       s.availability_end
  FROM spaces s
  JOIN buildings bl ON s.building_id = bl.building_id
 WHERE s.permissions = 'all'
   AND s.space_id NOT IN (
       SELECT b.space_id
         FROM bookings b
        WHERE b.status = 'active'
          AND b.time_start <= NOW()
          AND b.time_end   >= NOW()
   )
 ORDER BY bl.building_name, s.room_name;

-- 4.2  Browse available spaces and existing reservations in advance
SELECT s.room_name,
       s.space_type,
       s.size,
       bl.building_name,
       b.time_start,
       b.time_end,
       b.status
  FROM spaces s
  JOIN buildings bl  ON s.building_id = bl.building_id
  LEFT JOIN bookings b ON s.space_id  = b.space_id
                      AND b.status    = 'active'
                      AND DATE(b.time_start) = '2026-04-10'
 WHERE s.permissions = 'all'
 ORDER BY bl.building_name, s.room_name, b.time_start;

-- 4.3  Cancel or adjust the time/date of a reservation
UPDATE bookings
   SET time_start = '2026-04-10 15:00:00',
       time_end   = '2026-04-10 17:00:00'
 WHERE booking_id = 30
   AND creator_id = 4;

-- 4.4  Filter spaces by size and location
SELECT s.room_name,
       s.space_type,
       s.size,
       bl.building_name,
       bl.street
  FROM spaces s
  JOIN buildings bl ON s.building_id = bl.building_id
 WHERE s.size = 'medium'
   AND bl.building_name = 'Snell Library'
   AND s.permissions = 'all'
 ORDER BY s.room_name;

-- 4.5  Request approval for an unconventional / unlisted space
INSERT INTO help_tickets (ticket_type, title, description, creator_id)
VALUES ('space_request',
        'Request to use Dodge Lobby',
        'Looking to reserve Dodge Lobby for a large group study session '
        'on April 15th from 6-9 PM.',
        4);

-- 4.6  View upcoming and past reservations
SELECT b.booking_id,
       b.status,
       b.time_start,
       b.time_end,
       s.room_name,
       s.space_type,
       bl.building_name
  FROM bookings b
  JOIN spaces s     ON b.space_id    = s.space_id
  JOIN buildings bl ON s.building_id = bl.building_id
 WHERE b.creator_id = 4
 ORDER BY b.time_start DESC;
