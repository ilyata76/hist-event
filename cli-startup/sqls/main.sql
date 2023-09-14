
-- УДАЛИТЬ ТАБЛИЦЫ, если те существуют

BEGIN;

DROP TABLE IF EXISTS dates CASCADE; -- банк дат, на которые будут ссылаться другие сущности

DROP TABLE IF EXISTS persons CASCADE; -- банк исторических личностей, или по-другому персон

DROP TABLE IF EXISTS sources CASCADE; -- банк исторических разных источников

DROP TABLE IF EXISTS source_fragments CASCADE; -- банк ФРАГМЕНТОВ исторических разных источников

DROP TABLE IF EXISTS biblios CASCADE; -- банк библиографических источников

DROP TABLE IF EXISTS biblio_fragments CASCADE; -- банк ФРАГМЕНТОВ Библиографических источников

DROP TABLE IF EXISTS places CASCADE; -- банк всяческих мест

DROP TABLE IF EXISTS others CASCADE; -- банк всего остального, что не попало ни в какую из категорий

DROP TABLE IF EXISTS events CASCADE; -- банк событий, главной сущности базы данных

DROP TABLE IF EXISTS bonds CASCADE;

COMMIT;


-- СОЗДАТЬ ТАБЛИЦЫ 

BEGIN;

CREATE TABLE dates (
	id INTEGER PRIMARY KEY,
	name TEXT,
	description TEXT,
	date DATE,
	time TIME,
	start_date DATE,
	start_time TIME,
	end_date DATE,
	end_time TIME,
	events INTEGER ARRAY,
	ex_events INTEGER ARRAY,
	dates INTEGER ARRAY,
	ex_dates INTEGER ARRAY,
	places INTEGER ARRAY,
	ex_places INTEGER ARRAY,
	persons INTEGER ARRAY,
	ex_persons INTEGER ARRAY,
	sources INTEGER ARRAY,
	ex_sources INTEGER ARRAY,
	others INTEGER ARRAY,
	ex_others INTEGER ARRAY,
	source_fragments INTEGER ARRAY,
	ex_source_fragments INTEGER ARRAY,
	biblios INTEGER ARRAY,
	ex_biblios INTEGER ARRAY,
	biblio_fragments INTEGER ARRAY,
	ex_biblio_fragments INTEGER ARRAY
);

CREATE TABLE persons (
	id INTEGER PRIMARY KEY,
	name TEXT,
	description TEXT,
	date INTEGER NOT NULL,
		CONSTRAINT FK_date_id FOREIGN KEY (date) REFERENCES dates(id),
	person TEXT NOT NULL,
	events INTEGER ARRAY,
	ex_events INTEGER ARRAY,
	dates INTEGER ARRAY,
	ex_dates INTEGER ARRAY,
	places INTEGER ARRAY,
	ex_places INTEGER ARRAY,
	persons INTEGER ARRAY,
	ex_persons INTEGER ARRAY,
	sources INTEGER ARRAY,
	ex_sources INTEGER ARRAY,
	others INTEGER ARRAY,
	ex_others INTEGER ARRAY,
	source_fragments INTEGER ARRAY,
	ex_source_fragments INTEGER ARRAY,
	biblios INTEGER ARRAY,
	ex_biblios INTEGER ARRAY,
	biblio_fragments INTEGER ARRAY,
	ex_biblio_fragments INTEGER ARRAY
);

CREATE TABLE sources (
	id INTEGER PRIMARY KEY,
	name TEXT,
	description TEXT,
	author INTEGER NOT NULL,
		CONSTRAINT FK_person_id FOREIGN KEY (author) REFERENCES persons(id), 
	link TEXT,
	date INTEGER NOT NULL,
		CONSTRAINT FK_date_id FOREIGN KEY (date) REFERENCES dates(id), 
	type TEXT,
	subtype TEXT,
	events INTEGER ARRAY,
	ex_events INTEGER ARRAY,
	dates INTEGER ARRAY,
	ex_dates INTEGER ARRAY,
	places INTEGER ARRAY,
	ex_places INTEGER ARRAY,
	persons INTEGER ARRAY,
	ex_persons INTEGER ARRAY,
	sources INTEGER ARRAY,
	ex_sources INTEGER ARRAY,
	others INTEGER ARRAY,
	ex_others INTEGER ARRAY,
	source_fragments INTEGER ARRAY,
	ex_source_fragments INTEGER ARRAY,
	biblios INTEGER ARRAY,
	ex_biblios INTEGER ARRAY,
	biblio_fragments INTEGER ARRAY,
	ex_biblio_fragments INTEGER ARRAY
);

CREATE TABLE source_fragments (
	id INTEGER PRIMARY KEY,
	name TEXT,
	description TEXT,
	source INTEGER NOT NULL,
		CONSTRAINT FK_source_id FOREIGN KEY (source) REFERENCES sources(id),
	events INTEGER ARRAY,
	ex_events INTEGER ARRAY,
	dates INTEGER ARRAY,
	ex_dates INTEGER ARRAY,
	places INTEGER ARRAY,
	ex_places INTEGER ARRAY,
	persons INTEGER ARRAY,
	ex_persons INTEGER ARRAY,
	sources INTEGER ARRAY,
	ex_sources INTEGER ARRAY,
	others INTEGER ARRAY,
	ex_others INTEGER ARRAY,
	source_fragments INTEGER ARRAY,
	ex_source_fragments INTEGER ARRAY,
	biblios INTEGER ARRAY,
	ex_biblios INTEGER ARRAY,
	biblio_fragments INTEGER ARRAY,
	ex_biblio_fragments INTEGER ARRAY
);

CREATE TABLE biblios (
	id INTEGER PRIMARY KEY,
	name TEXT,
	description TEXT,
	author TEXT NOT NULL,
	link TEXT,
	date TEXT,
	state TEXT, 
	period TEXT,
	events INTEGER ARRAY,
	ex_events INTEGER ARRAY,
	dates INTEGER ARRAY,
	ex_dates INTEGER ARRAY,
	places INTEGER ARRAY,
	ex_places INTEGER ARRAY,
	persons INTEGER ARRAY,
	ex_persons INTEGER ARRAY,
	sources INTEGER ARRAY,
	ex_sources INTEGER ARRAY,
	others INTEGER ARRAY,
	ex_others INTEGER ARRAY,
	source_fragments INTEGER ARRAY,
	ex_source_fragments INTEGER ARRAY,
	biblios INTEGER ARRAY,
	ex_biblios INTEGER ARRAY,
	biblio_fragments INTEGER ARRAY,
	ex_biblio_fragments INTEGER ARRAY
);

CREATE TABLE biblio_fragments (
	id INTEGER PRIMARY KEY,
	name TEXT,
	description TEXT,
	biblio INTEGER NOT NULL,
		CONSTRAINT FK_biblio_id FOREIGN KEY (biblio) REFERENCES biblios(id),
	events INTEGER ARRAY,
	ex_events INTEGER ARRAY,
	dates INTEGER ARRAY,
	ex_dates INTEGER ARRAY,
	places INTEGER ARRAY,
	ex_places INTEGER ARRAY,
	persons INTEGER ARRAY,
	ex_persons INTEGER ARRAY,
	sources INTEGER ARRAY,
	ex_sources INTEGER ARRAY,
	others INTEGER ARRAY,
	ex_others INTEGER ARRAY,
	source_fragments INTEGER ARRAY,
	ex_source_fragments INTEGER ARRAY,
	biblios INTEGER ARRAY,
	ex_biblios INTEGER ARRAY,
	biblio_fragments INTEGER ARRAY,
	ex_biblio_fragments INTEGER ARRAY
);

CREATE TABLE places (
	id INTEGER PRIMARY KEY,
	name TEXT,
	description TEXT,
	geo TEXT,
	events INTEGER ARRAY,
	ex_events INTEGER ARRAY,
	dates INTEGER ARRAY,
	ex_dates INTEGER ARRAY,
	places INTEGER ARRAY,
	ex_places INTEGER ARRAY,
	persons INTEGER ARRAY,
	ex_persons INTEGER ARRAY,
	sources INTEGER ARRAY,
	ex_sources INTEGER ARRAY,
	others INTEGER ARRAY,
	ex_others INTEGER ARRAY,
	source_fragments INTEGER ARRAY,
	ex_source_fragments INTEGER ARRAY,
	biblios INTEGER ARRAY,
	ex_biblios INTEGER ARRAY,
	biblio_fragments INTEGER ARRAY,
	ex_biblio_fragments INTEGER ARRAY
);

CREATE TABLE others (
	id INTEGER PRIMARY KEY,
	name TEXT,
	description TEXT,
	meta TEXT,
	events INTEGER ARRAY,
	ex_events INTEGER ARRAY,
	dates INTEGER ARRAY,
	ex_dates INTEGER ARRAY,
	places INTEGER ARRAY,
	ex_places INTEGER ARRAY,
	persons INTEGER ARRAY,
	ex_persons INTEGER ARRAY,
	sources INTEGER ARRAY,
	ex_sources INTEGER ARRAY,
	others INTEGER ARRAY,
	ex_others INTEGER ARRAY,
	source_fragments INTEGER ARRAY,
	ex_source_fragments INTEGER ARRAY,
	biblios INTEGER ARRAY,
	ex_biblios INTEGER ARRAY,
	biblio_fragments INTEGER ARRAY,
	ex_biblio_fragments INTEGER ARRAY
);

CREATE TABLE events (
	id INTEGER PRIMARY KEY,
	name TEXT,
	description TEXT,
	date INTEGER NOT NULL,
		CONSTRAINT FK_date_id FOREIGN KEY (date) REFERENCES dates(id),
	min TEXT NOT NULL,
	max TEXT NOT NULL,
	level TEXT,
	events INTEGER ARRAY,
	ex_events INTEGER ARRAY,
	dates INTEGER ARRAY,
	ex_dates INTEGER ARRAY,
	places INTEGER ARRAY,
	ex_places INTEGER ARRAY,
	persons INTEGER ARRAY,
	ex_persons INTEGER ARRAY,
	sources INTEGER ARRAY,
	ex_sources INTEGER ARRAY,
	others INTEGER ARRAY,
	ex_others INTEGER ARRAY,
	source_fragments INTEGER ARRAY,
	ex_source_fragments INTEGER ARRAY,
	biblios INTEGER ARRAY,
	ex_biblios INTEGER ARRAY,
	biblio_fragments INTEGER ARRAY,
	ex_biblio_fragments INTEGER ARRAY
);

CREATE TABLE bonds (
	id SERIAL PRIMARY KEY,
	event INTEGER NOT NULL,
		CONSTRAINT FK_event_id FOREIGN KEY (id) REFERENCES events(id),
	parents INTEGER ARRAY,
	childs INTEGER ARRAY,
	prerequisites INTEGER ARRAY
); -- таблица связей

COMMIT;


-- ЗАПОЛНИТЬ ТАБЛИЦЫ 

BEGIN;

INSERT INTO dates VALUES 
	( '1', 'название', 'Описание для ?внутренних целей? ({biblio_fragment:1}[?]) ({source : 1}[источник])',
	  '2023-08-23', '10:10:10',
	  null, null,
	  null, null,
	  null, null,
	  null, '{5}',
	  null, null,
	  null, '{1}',
	  '{1}', null,
	  null, null,
	  null, null,
	  null, null,
	  '{1}', null ),
	( '2', 'название', 'Многострочное описание события 2 ({source : 1}[источник]) а теперь здесь есть ссылка на {person:1}[челика]',
	  '2023-08-23', null,
	  null, null,
	  null, null,
	  null, null,
	  null, null,
	  null, '{1}',
	  '{1}', null,
	  '{1}', null,
	  null, null,
	  null, null,
	  null, null,
	  null, null ),
	( '3', '"Дата августовского путча"', null,
	  '2023-07-23', null,
	  '2023-06-23', null,
	  '2023-08-23', null,
	  null, null,
	  null, null,
	  null, '{1}',
	  null, '{2}',
	  null, null,
	  null, null,
	  null, null,
	  null, null,
	  null, null ),
	( '4', '18 ноября 2024', null,
	  '2023-08-23', null,
	  '2023-08-23', '10:10:10',
	  null, null,
	  null, null,
	  null, null,
	  null, '{1}',
	  null, null,
	  null, null,
	  null, null,
	  null, null,
	  null, null,
	  null, null ),
	( '5', '23 августа 2023', 'Описание события 5, которое было {biblio:1}[?] бы после {date:1}[этого], но не случилось ({source : 1}[источник])',
	  '2023-08-23', null,
	  null, null,
	  null, null,
	  null, null,
	  '{1}', null,
	  null, null,
	  null, null,
	  '{1}', null,
	  null, null,
	  null, null,
	  '{1}', null,
	  null, null );

INSERT INTO persons VALUES 
	( '1', 'Абоба Максим Маркович', 'Абоба Максим Маркович родился {date:1}[сегодня] в городе {place:1}[Жепа] ({source : 1}[источник])',
	  '1', 'Абоба Максим Маркович',
	  null, '{1, 6}',
	  '{1}', '{2}',
	  '{1}', null,
	  null, '{2}',
	  '{1}', null,
	  null, '{1}',
	  null, null,
	  null, null,
	  null, null ),
	( '2', 'Абоба Марк Андреевич', 'Абоба-старший родился задолго до {date:3}[авг путча], но только после этого он эмигрировал в {place:1}[Жепу]. Тогда как {person:1}[Абоба Максим] остался. ({source:1}[источник])',
	  '2', 'Абоба Максим Маркович',
	  null, null,
	  '{3}', null,
	  '{1}', null,
	  '{1}', null,
	  '{1}', null,
	  null, null,
	  null, null,
	  null, null,
	  null, null );

INSERT INTO sources VALUES 
	( '1', 'Запись из личного архива №123321. Может быть автор.', 'Описание источника. Автор. Доступно по ссылке http://aboba',
	  '1', 'http://aboba', '3',
	  null, null,
	  null, '{1, 6}',
	  null, '{1, 2, 5}',
	  null, '{1}',
	  null, '{1, 2}',
	  null, '{2}',
	  null, '{1}',
	  null, null,
	  null, null,
	  null, null ),
	( '2', 'Запись из личного архива №123321-2. Может быть автор.', 'Описание источника. Автор. Доступно по ссылке http://aboba {source:1}[родительский источник]',
	  '2', 'http://aboba', '4',
	  'тип', 'подтип',
	  null, '{2, 6}',
	  null, null,
	  null, null,
	  null, null,
	  '{1}', null,
	  null, null,
	  null, null,
	  null, null,
	  null, null );

INSERT INTO source_fragments VALUES 
	( '1', 'ссылка на главу с жопой', 'Глава пятая, строка двадцатая, улица Пушкина, дом Колотушкина',
	  '1',
	  null, '{5}',
	  null, null,
	  null, null,
	  null, null,
	  null, null,
	  null, null,
	  null, null,
	  null, null,
	  null, null );

INSERT INTO biblios VALUES 
	( '1', 'книшка', 'описании книшки',
	  'абоба бибобович', 'http://aboba', 'date здесь никак не валидируется',
	  'USSR', 'совочек',
	  null, null,
	  null, '{5}',
	  null, null,
	  null, null,
	  null, null,
	  null, null,
	  null, null,
	  null, null,
	  null, null );

INSERT INTO biblio_fragments VALUES 
	( '1', 'ссылка на главу с жопой', 'жопа в жопе',
	  '1',
	  null, null,
	  null, '{1}',
	  null, null,
	  null, null,
	  null, null,
	  null, null,
	  null, null,
	  null, null,
	  null, null );

INSERT INTO places VALUES 
	( '1', 'Жепа', 'Город Жепа основан в {date:4}[основание города жепа] мог бы быть, но так не случилось, поэтому в {date:3}[какое-то контекстное название] тоже ничего не получилось, а в {date:2}[склонение] вообще так не получилось, что до сих пор не получается. ({source : 1}[источник])',
	  'геолокация или имя или ещё чего',
	  null, '{6}',
	  '{2, 3, 4}', null,
	  null, null,
	  null, '{1, 2}',
	  '{1}', null,
	  null, null,
	  null, null,
	  null, null,
	  null, null );

INSERT INTO others VALUES 
	( '1', 'ABOBA NMAE', 'DESCRIPTION {source:1}[источник] ааа {person:1}[Абоба Максим]',
	  'КАКАЯ_ТО_МЕТА_ИНФОРМАЦИЯ',
	  null, null,
	  null, null,
	  null, null,
	  '{1}', null,
	  '{1}', null,
	  null, null,
	  null, null,
	  null, null,
	  null, null );

INSERT INTO events VALUES 
	( '1', 'Крестьянина выгнали', null,
	  '1',
	  'Креста {person:1}[Жопошника] выгнали за то, что он был жопошником.',
	  'Подробное объяснение, что креста {person:1}[Жопошника] выгнали за то, что он был жопошником, да ещё таким отпетым жопошником. {source:1}[По свидетельствам] жопопинателей, он был жопошником.',
	  'FACT',
	  null, '{2}',
	  null, null,
	  null, null,
	  '{1}', null,
	  '{1}', null,
	  null, null,
	  null, null,
	  null, null,
	  null, null ),
	( '2', 'Жопошников выгоняли', null,
	  '2',
	  'Крестов-жопошников выгоняли по мнгогим причинам',
	  'Крестов-жопошников выгоняли по мнгогим причинам: так, {event:1}[?]. Таким образом, если учитывать {source:2}[источники], жопошников выгоняли нафик',
	  'GENERAL',
	  '{1}', '{3}',
	  null, null,
	  null, null,
	  null, null,
	  '{2}', null,
	  null, null,
	  null, null,
	  null, null,
	  null, null ),
	( '3', 'Процесс ослабления общин', null,
	  '3',
	  'Общины ослаблялись по многим причинам (причины)',
	  'По многим причинам ослаблялись общины. {event:2}[?]. Таким образом, общины ослаблялись.',
	  'PROCESS',
	  '{2}', '{4}',
	  null, null,
	  null, null,
	  null, null,
	  null, null,
	  null, null,
	  null, null,
	  null, null,
	  null, null ),
	( '4', 'ЧТО БЫЛО', null,
	  '4',
	  'Было очень плохо. Жопошников выгоняли. Ещё чего только не делали.',
	  'Было очень плохо (текст как было плохо). Общины ослаблялись {event:3}[?] Ещё подзаголовок Вот как было плохо',
	  'STATE',
	  '{3}', '{5}',
	  null, null,
	  null, null,
	  null, null,
	  null, null,
	  null, null,
	  null, null,
	  null, null,
	  null, null ),
	( '5', 'Аграрная реформа', null,
	  '5',
	  'Реформа была крутая, а ещё немного некрутая.',
	  'Реформа была крутая, потому что назрела. Состояние сельского хозяйство было плачевным. {event:4}[?]. Реформа должна была преследовать цели. Таким образом, был запущен процесс чего-то (ХОД) {source_fragment:1}[абоба] В итоге всё сталок руто но не очень круто (ИТОГИ).',
	  'EVENT',
	  '{4}', '{6}',
	  null, null,
	  null, null,
	  null, null,
	  null, null,
	  null, null,
	  '{1}', null,
	  null, null,
	  null, null ),
	( '6', 'Столыпин', null,
	  '5',
	  'да вот тако мужик',
	  'мужик ничё вот {source:1}[aboba] {source:2}[aboba] {event:5}[его реформа] {person:1}[перс] {place:1}[место]',
	  'CORE',
	  '{5}', null,
	  null, null,
	  '{1}', null,
	  '{1}', null,
	  '{1, 2}', null,
	  null, null,
	  null, null,
	  null, null,
	  null, null );

INSERT INTO bonds (event, parents, childs, prerequisites) VALUES 
	( '1', '{2, 3}',
	  '{4, 5, 6}', null ),
	( '2', '{1, 3}',
	  null, null );

COMMIT;

BEGIN;

DROP VIEW IF EXISTS eventsbonds CASCADE;
DROP VIEW IF EXISTS bondswithoutid CASCADE;

CREATE OR REPLACE VIEW bondswithoutid
    AS SELECT event, parents, childs, prerequisites
        FROM bonds
;

CREATE OR REPLACE VIEW eventsbonds 
    AS SELECT * 
        FROM events as e
        JOIN bondswithoutid as b
            ON e.id = b.event
;

COMMIT;

