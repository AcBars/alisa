BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "subjects"
(
    id        INTEGER,
    "subject" TEXT NOT NULL,
    PRIMARY KEY (id AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "classes"
(
    id       INTEGER,
    "level"  INTEGER,
    "symbol" TEXT,
    PRIMARY KEY (id AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "students"
(
    id           INTEGER,
    "first_name" TEXT,
    "last_name"  TEXT,
    "id_class"   INTEGER NOT NULL,
    PRIMARY KEY (id AUTOINCREMENT),
    FOREIGN KEY ("id_class") REFERENCES "classes" (id)
);
CREATE TABLE IF NOT EXISTS "week"
(
    id           INTEGER,
    "name"       TEXT NOT NULL,
    "short_name" TEXT,
    PRIMARY KEY (id AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "schedule"
(
    id           INTEGER,
    "id_week"    INTEGER,
    "time_start" TEXT,
    "id_class"   INTEGER,
    "id_subject" INTEGER,
    PRIMARY KEY (id AUTOINCREMENT),
    FOREIGN KEY ("id_subject") REFERENCES "subjects" (id),
    FOREIGN KEY ("id_class") REFERENCES "classes" (id),
    FOREIGN KEY ("id_week") REFERENCES "week" (id)
);

INSERT INTO "subjects" (id, subject)
VALUES (1, 'Русский язык'),
       (2, 'Арифметика'),
       (3, 'Рисование'),
       (4, 'Пение'),
       (5, 'Физкультура');

INSERT INTO "classes" (id, level, symbol)
VALUES (1, 1, 'А'),
       (2, 1, 'Б'),
       (3, 2, 'А'),
       (4, 2, 'Б'),
       (5, 1, 'В'),
       (6, 3, 'А'),
       (7, 3, 'Б');

INSERT INTO "students" (id, first_name, last_name, id_class)
VALUES (1, 'Владислав', 'Перов', 1),
       (2, 'Глеб', 'Смирнов', 1),
       (3, 'Маша', 'Распутина', 2),
       (4, 'Андрей', 'Миронов', 7);

INSERT INTO "week" (id, name, short_name)
VALUES (1, 'понедельник', 'пн'),
       (2, 'вторник', 'вт'),
       (3, 'среда', 'ср'),
       (4, 'четверг', 'чт'),
       (5, 'пятница', 'пт'),
       (6, 'суббота', 'сб'),
       (7, 'воскресенье', 'вс');

INSERT INTO "schedule" (id, id_week, time_start, id_class, id_subject)
VALUES (1, 1, '10:00', 2, 2),
       (2, 1, '19:00', 2, 1),
       (3, 4, '12:00', 1, 3);

COMMIT;
