BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "weather" (
	"Name"	TEXT
);
CREATE TABLE IF NOT EXISTS "navigation" (
	"Fall"	TEXT,
	"Water"	TEXT,
	"If_fought"	BOOLEAN,
	"If_rowed"	BOOLEAN,
	"Bird"	INTEGER
);
CREATE TABLE IF NOT EXISTS "cards" (
	"Name"	TEXT,
	"Can_Be_Activated"	Boolean,
	"Add_Strength"	INTEGER,
	"Heal"	INTEGER
);
INSERT INTO "navigation" VALUES ('capitan','first_mate','true','false',1);
INSERT INTO "navigation" VALUES ('capitan','frenchy','false','false',0);
INSERT INTO "navigation" VALUES ('capitan','sir','true','true',0);
INSERT INTO "navigation" VALUES ('capitan','capitan','false','false',0);
INSERT INTO "navigation" VALUES ('first_mate','capitan;first_mate','false','true',0);
INSERT INTO "navigation" VALUES ('first_mate','lady','false','false',0);
INSERT INTO "navigation" VALUES ('first_mate','capitan;frenchy','true','true',0);
INSERT INTO "navigation" VALUES ('first_mate','kid','true','false',1);
INSERT INTO "navigation" VALUES ('frenchy','capitan;first_mate;kid','false','true',0);
INSERT INTO "navigation" VALUES ('frenchy','capitan;first_mate;lady','true','false',0);
INSERT INTO "navigation" VALUES ('frenchy','capitan;first_mate;frenchy;sir','true','true',0);
INSERT INTO "navigation" VALUES ('frenchy','capitan;first_mate;frenchy','false','false',1);
INSERT INTO "navigation" VALUES ('lady','everyone;!kid','false','true',-1);
INSERT INTO "navigation" VALUES ('sir','capitan','false','false',0);
INSERT INTO "navigation" VALUES ('sir','capitan;kid','false','true',1);
INSERT INTO "navigation" VALUES ('sir','capitan;first_mate;frenchy;','true','true',0);
INSERT INTO "navigation" VALUES ('sir','capitan;lady','true','false',0);
INSERT INTO "navigation" VALUES ('kid','capitan;first_mate;frenchy;lady','true','false',0);
INSERT INTO "navigation" VALUES ('kid','capitan;first_mate;frenchy;kid','true','false',0);
INSERT INTO "navigation" VALUES ('kid','everyone;!kid','false','true',0);
INSERT INTO "navigation" VALUES ('kid','everyone;!lady','true','true',1);
INSERT INTO "navigation" VALUES ('everyone','everyone','true','false',0);
INSERT INTO "navigation" VALUES ('everyone','everyone','true','true',1);
INSERT INTO "navigation" VALUES ('noone',NULL,'false','false',1);
INSERT INTO "cards" VALUES ('water','true',0,0);
INSERT INTO "cards" VALUES ('water','true',0,0);
INSERT INTO "cards" VALUES ('water','true',0,0);
INSERT INTO "cards" VALUES ('water','true',0,0);
INSERT INTO "cards" VALUES ('water','true',0,0);
INSERT INTO "cards" VALUES ('water','true',0,0);
INSERT INTO "cards" VALUES ('water','true',0,0);
INSERT INTO "cards" VALUES ('water','true',0,0);
INSERT INTO "cards" VALUES ('water','true',0,0);
INSERT INTO "cards" VALUES ('water','true',0,0);
INSERT INTO "cards" VALUES ('water','true',0,0);
INSERT INTO "cards" VALUES ('water','true',0,0);
INSERT INTO "cards" VALUES ('water','true',0,0);
INSERT INTO "cards" VALUES ('water','true',0,0);
INSERT INTO "cards" VALUES ('water','true',0,0);
INSERT INTO "cards" VALUES ('water','true',0,0);
INSERT INTO "cards" VALUES ('cash','false',0,0);
INSERT INTO "cards" VALUES ('cash','false',0,0);
INSERT INTO "cards" VALUES ('cash','false',0,0);
INSERT INTO "cards" VALUES ('cash','false',0,0);
INSERT INTO "cards" VALUES ('cash','false',0,0);
INSERT INTO "cards" VALUES ('cash','false',0,0);
INSERT INTO "cards" VALUES ('medical kit','true',0,1);
INSERT INTO "cards" VALUES ('medical kit','true',0,1);
INSERT INTO "cards" VALUES ('medical kit','true',0,1);
INSERT INTO "cards" VALUES ('jewels','false',0,0);
INSERT INTO "cards" VALUES ('jewels','false',0,0);
INSERT INTO "cards" VALUES ('jewels','false',0,0);
INSERT INTO "cards" VALUES ('painting','false',0,0);
INSERT INTO "cards" VALUES ('painting','false',0,0);
INSERT INTO "cards" VALUES ('painting','false',0,0);
INSERT INTO "cards" VALUES ('oar','true',1,0);
INSERT INTO "cards" VALUES ('oar','true',1,0);
INSERT INTO "cards" VALUES ('bucket of chum','true',0,0);
INSERT INTO "cards" VALUES ('bucket of chum','true',0,0);
INSERT INTO "cards" VALUES ('compass','true',0,0);
INSERT INTO "cards" VALUES ('gun','true',8,0);
INSERT INTO "cards" VALUES ('hook','true',4,0);
INSERT INTO "cards" VALUES ('knife','true',3,0);
INSERT INTO "cards" VALUES ('bat','true',2,0);
INSERT INTO "cards" VALUES ('umbrella','true',0,0);
INSERT INTO "cards" VALUES ('saver','true',0,0);
COMMIT;
