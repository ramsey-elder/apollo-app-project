INSERT INTO spaces (space_id, permissions, availability_start, availability_end, space_type, room_name, size, creator_id, building_id) VALUES
-- Building 1: Snell Library
(1,  'all',  '08:00:00', '22:00:00', 'room', 'Study Room LL10',      'small',  1, 1),
(2,  'all',  '08:00:00', '22:00:00', 'room', 'Study Room 101',       'small',  2, 1),
(3,  'all',  '08:00:00', '22:00:00', 'room', 'Study Room 201',       'small',  1, 1),
(4,  'all',  '08:00:00', '22:00:00', 'room', 'Study Room 401',       'medium', 2, 1),
(5,  'all',  '08:00:00', '22:00:00', 'room', 'Group Study Room 402', 'medium', 1, 1),

-- Building 2: Curry Student Center
(6,  'club', '09:00:00', '23:00:00', 'dance_studio', 'Studio A',         'medium', 2, 2),
(7,  'all',  '09:00:00', '23:00:00', 'music_studio', 'Music Studio',     'medium', 1, 2),
(8,  'all',  '08:00:00', '22:00:00', 'room',         'Meeting Room 301', 'small',  2, 2),
(9,  'all',  '08:00:00', '22:00:00', 'room',         'Event Hall 401',   'large',  1, 2),
(10, 'all',  '08:00:00', '22:00:00', 'room',         'Study Lounge 210', 'small',  2, 2),

-- Building 3: Marino Recreation Center
(11, 'club', '09:00:00', '23:00:00', 'dance_studio', 'Studio A',          'large',  1, 3),
(12, 'club', '09:00:00', '23:00:00', 'dance_studio', 'Studio B',          'medium', 2, 3),
(13, 'all',  '08:00:00', '22:00:00', 'room',         'Multipurpose Room', 'large',  1, 3),
(14, 'all',  '08:00:00', '22:00:00', 'room',         'Gymnasium Court 1', 'large',  2, 3),
(15, 'all',  '08:00:00', '22:00:00', 'room',         'Gymnasium Court 2', 'medium', 1, 3),

-- Building 4: SquashBusters Center
(16, 'all', '08:00:00', '22:00:00', 'room', 'Squash Court 1',    'small',  2, 4),
(17, 'all', '08:00:00', '22:00:00', 'room', 'Squash Court 2',    'small',  1, 4),
(18, 'all', '08:00:00', '22:00:00', 'room', 'Squash Court 3',    'small',  2, 4),
(19, 'all', '08:00:00', '22:00:00', 'room', 'Multipurpose Court','medium', 1, 4),
(20, 'all', '08:00:00', '22:00:00', 'room', 'Conference Room 101','small', 2, 4),

-- Building 5: ISEC
(21, 'club', '08:00:00', '21:00:00', 'lecture_hall', '102 ISEC',              'medium', 1, 5),
(22, 'club', '08:00:00', '21:00:00', 'lecture_hall', 'ISEC Auditorium',       'large',  2, 5),
(23, 'club', '08:00:00', '21:00:00', 'lecture_hall', 'Lecture Hall 108',      'medium', 1, 5),
(24, 'all',  '08:00:00', '22:00:00', 'room',         'Active Learning Rm 120','medium', 2, 5),
(25, 'all',  '08:00:00', '22:00:00', 'room',         'Seminar Room 250',      'small',  1, 5),

-- Building 6: Dodge Hall
(26, 'club', '08:00:00', '21:00:00', 'lecture_hall', 'Dodge 101',        'large',  2, 6),
(27, 'club', '08:00:00', '21:00:00', 'lecture_hall', 'Dodge 201',        'medium', 1, 6),
(28, 'all',  '08:00:00', '22:00:00', 'room',         'Seminar Room 102', 'medium', 2, 6),
(29, 'all',  '08:00:00', '22:00:00', 'room',         'Conference Room 301','small', 1, 6),
(30, 'all',  '08:00:00', '22:00:00', 'room',         'Study Room 410',   'small',  2, 6),

-- Building 7: Richards Hall
(31, 'club', '08:00:00', '21:00:00', 'lecture_hall', 'Richards 101',    'large',  1, 7),
(32, 'club', '08:00:00', '21:00:00', 'lecture_hall', 'Richards 201',    'medium', 2, 7),
(33, 'all',  '08:00:00', '22:00:00', 'room',         'Seminar Room 210','medium', 1, 7),
(34, 'all',  '08:00:00', '22:00:00', 'room',         'Computer Lab 120','medium', 2, 7),
(35, 'all',  '08:00:00', '22:00:00', 'room',         'Study Room 305',  'small',  1, 7),

-- Building 8: Behrakis Health Sciences Center
(36, 'club', '08:00:00', '21:00:00', 'lecture_hall', 'Behrakis 101',      'large',  2, 8),
(37, 'club', '08:00:00', '21:00:00', 'lecture_hall', 'Behrakis 201',      'medium', 1, 8),
(38, 'all',  '08:00:00', '22:00:00', 'room',         'Lab Room 110',      'medium', 2, 8),
(39, 'all',  '08:00:00', '22:00:00', 'room',         'Seminar Room 205',  'small',  1, 8),
(40, 'all',  '08:00:00', '22:00:00', 'room',         'Conference Room 301','small', 2, 8),

-- Building 9: Shillman Hall
(41, 'club', '08:00:00', '21:00:00', 'lecture_hall', '105 Shillman',      'large',  1, 9),
(42, 'club', '08:00:00', '21:00:00', 'lecture_hall', '305 Shillman',      'medium', 2, 9),
(43, 'all',  '09:00:00', '23:00:00', 'music_studio', 'Recording Studio',  'small',  1, 9),
(44, 'all',  '08:00:00', '22:00:00', 'room',         'Study Room 220',    'small',  2, 9),
(45, 'all',  '08:00:00', '22:00:00', 'room',         'Conference Room 215','medium',1, 9),

-- Building 10: Hayden Hall
(46, 'club', '08:00:00', '21:00:00', 'lecture_hall', 'Hayden 010',        'large',  2, 10),
(47, 'club', '08:00:00', '21:00:00', 'lecture_hall', 'Hayden 210',        'medium', 1, 10),
(48, 'all',  '08:00:00', '22:00:00', 'room',         'Study Room 315',    'small',  2, 10),
(49, 'all',  '08:00:00', '22:00:00', 'room',         'Seminar Room 205',  'medium', 1, 10),
(50, 'all',  '08:00:00', '22:00:00', 'room',         'Conference Room 120','small', 2, 10),

-- Building 11: Ryder Hall
(51, 'all', '09:00:00', '23:00:00', 'music_studio', 'Ryder 364 Music Room','medium', 1, 11),
(52, 'all', '09:00:00', '23:00:00', 'music_studio', 'Practice Room 201',   'small',  2, 11),
(53, 'all', '08:00:00', '22:00:00', 'room',         'Seminar Room 110',    'medium', 1, 11),
(54, 'all', '08:00:00', '22:00:00', 'room',         'Conference Room 305', 'small',  2, 11),
(55, 'all', '08:00:00', '22:00:00', 'room',         'Study Room 410',      'small',  1, 11),

-- Building 12: Ell Hall
(56, 'club', '08:00:00', '21:00:00', 'lecture_hall', 'Ell Hall Auditorium','large',  2, 12),
(57, 'club', '08:00:00', '21:00:00', 'lecture_hall', 'Ell 312',            'medium', 1, 12),
(58, 'all',  '08:00:00', '22:00:00', 'room',         'Seminar Room 105',   'medium', 2, 12),
(59, 'all',  '08:00:00', '22:00:00', 'room',         'Study Room 210',     'small',  1, 12),
(60, 'all',  '08:00:00', '22:00:00', 'room',         'Conference Room 301','small',  2, 12),

-- Building 13: Churchill Hall
(61, 'club', '08:00:00', '21:00:00', 'lecture_hall', 'Churchill 101',      'large',  1, 13),
(62, 'club', '08:00:00', '21:00:00', 'lecture_hall', 'Churchill 201',      'medium', 2, 13),
(63, 'all',  '08:00:00', '22:00:00', 'room',         'Seminar Room 210',   'medium', 1, 13),
(64, 'all',  '08:00:00', '22:00:00', 'room',         'Study Room 105',     'small',  2, 13),
(65, 'all',  '08:00:00', '22:00:00', 'room',         'Conference Room 305','small',  1, 13),

-- Building 14: West Village H
(66, 'all', '08:00:00', '22:00:00', 'room', 'Study Room 101',     'small',  2, 14),
(67, 'all', '08:00:00', '22:00:00', 'room', 'Study Room 102',     'small',  1, 14),
(68, 'all', '08:00:00', '22:00:00', 'room', 'Meeting Room 201',   'medium', 2, 14),
(69, 'all', '08:00:00', '22:00:00', 'room', 'Lounge 301',         'large',  1, 14),
(70, 'all', '08:00:00', '22:00:00', 'room', 'Conference Room 105','small',  2, 14),

-- Building 15: EXP
(71, 'club', '08:00:00', '21:00:00', 'lecture_hall', 'EXP Lecture Hall 102','large',  1, 15),
(72, 'all',  '08:00:00', '22:00:00', 'room',         'EXP Seminar 201',    'medium', 2, 15),
(73, 'all',  '08:00:00', '22:00:00', 'room',         'EXP Lab 110',        'medium', 1, 15),
(74, 'all',  '08:00:00', '22:00:00', 'room',         'EXP Study Room 301', 'small',  2, 15),
(75, 'all',  '08:00:00', '22:00:00', 'room',         'EXP Conference 205', 'small',  1, 15),

-- Building 16: Carter Field
(76, 'club', '07:00:00', '21:00:00', 'field', 'Main Soccer Field', 'large',  2, 16),
(77, 'club', '07:00:00', '21:00:00', 'field', 'Practice Field A',  'medium', 1, 16),
(78, 'club', '07:00:00', '21:00:00', 'field', 'Tennis Court 1',    'small',  2, 16),
(79, 'club', '07:00:00', '21:00:00', 'field', 'Tennis Court 2',    'small',  1, 16),
(80, 'club', '07:00:00', '21:00:00', 'field', 'Track Field',       'large',  2, 16),

-- Building 17: Matthews Arena
(81, 'club', '07:00:00', '21:00:00', 'field', 'Main Ice Rink',      'large',  1, 17),
(82, 'club', '07:00:00', '21:00:00', 'field', 'Practice Rink',      'medium', 2, 17),
(83, 'club', '07:00:00', '21:00:00', 'field', 'Basketball Court',   'large',  1, 17),
(84, 'all',  '08:00:00', '22:00:00', 'room',  'Locker Room A',      'medium', 2, 17),
(85, 'all',  '08:00:00', '22:00:00', 'room',  'Conference Room 101','small',  1, 17),

-- Building 18: Lake Hall
(86, 'all',  '09:00:00', '23:00:00', 'music_studio', 'Lake Hall Music Studio','medium', 2, 18),
(87, 'all',  '09:00:00', '23:00:00', 'music_studio', 'Lake Recording Studio', 'small',  1, 18),
(88, 'club', '08:00:00', '21:00:00', 'lecture_hall', 'Lake Hall 101',         'large',  2, 18),
(89, 'all',  '08:00:00', '22:00:00', 'room',         'Seminar Room 201',      'medium', 1, 18),
(90, 'all',  '08:00:00', '22:00:00', 'room',         'Practice Room 105',     'small',  2, 18),

-- Building 19: Nightingale Hall
(91, 'club', '08:00:00', '21:00:00', 'lecture_hall', 'Nightingale 101',     'large',  1, 19),
(92, 'club', '08:00:00', '21:00:00', 'lecture_hall', 'Nightingale 201',     'medium', 2, 19),
(93, 'all',  '08:00:00', '22:00:00', 'room',         'Seminar Room 210',    'medium', 1, 19),
(94, 'all',  '08:00:00', '22:00:00', 'room',         'Study Room 105',      'small',  2, 19),
(95, 'all',  '08:00:00', '22:00:00', 'room',         'Conference Room 305', 'small',  1, 19)
;
