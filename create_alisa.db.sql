BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "subjects" (
	"id_subject"	INTEGER,
	"subject"	TEXT NOT NULL,
	PRIMARY KEY("id_subject" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "classes" (
	"id_class"	INTEGER,
	"level"	INTEGER,
	"symbol"	TEXT,
	PRIMARY KEY("id_class" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "students" (
	"id_student"	INTEGER,
	"first_name"	TEXT,
	"second_name"	TEXT,
	"id_class"	INTEGER NOT NULL,
	PRIMARY KEY("id_student" AUTOINCREMENT),
	FOREIGN KEY("id_class") REFERENCES "classes"("id_class")
);
CREATE TABLE IF NOT EXISTS "schedule" (
	"id"	INTEGER,
	"day_of_week"	TEXT,
	"time_start"	TEXT,
	"id_class"	INTEGER,
	"id_subject"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_subject") REFERENCES "subjects"("id_subject"),
	FOREIGN KEY("id_class") REFERENCES "classes"("id_class")
);
INSERT INTO "subjects" VALUES (1,'Русский язык');
INSERT INTO "subjects" VALUES (2,'Арифметика');
INSERT INTO "subjects" VALUES (3,'Рисование');
INSERT INTO "subjects" VALUES (4,'Пение');
INSERT INTO "students" VALUES (2,'Владислав','Перов',1);
INSERT INTO "students" VALUES (3,'Глеб','Смирнов',1);
INSERT INTO "students" VALUES (4,'Маша','Распутина',2);
INSERT INTO "classes" VALUES (1,1,'А');
INSERT INTO "classes" VALUES (2,1,'Б');
INSERT INTO "classes" VALUES (3,2,'А');
INSERT INTO "classes" VALUES (4,2,'Б');
INSERT INTO "classes" VALUES (5,1,'В');
INSERT INTO "classes" VALUES (6,3,'А');
INSERT INTO "classes" VALUES (7,3,'Б');
COMMIT;
