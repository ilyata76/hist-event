-- УДАЛИТЬ ТАБЛИЦЫ, если те существуют

DROP TABLE IF EXISTS sources CASCADE; -- банк исторических разных источников

DROP TABLE IF EXISTS dates CASCADE; -- банк дат, на которые будут ссылаться другие сущности

DROP TABLE IF EXISTS places CASCADE; -- банк всяческих мест

DROP TABLE IF EXISTS persons CASCADE; -- банк исторических личностей, или по-другому персон

DROP TABLE IF EXISTS others CASCADE; -- банк всего остального, что не попало ни в какую из категорий

DROP TABLE IF EXISTS events CASCADE; -- банк событий, главной сущности базы данных

-- СОЗДАТЬ ТАБЛИЦЫ 

CREATE TABLE sources (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    date TEXT,
    description TEXT,
    author TEXT NOT NULL,
    link TEXT,
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
    ex_others INTEGER ARRAY
);

CREATE TABLE dates (
    id INTEGER PRIMARY KEY,
    name TEXT,
    date TEXT NOT NULL,
    description TEXT,
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
    ex_others INTEGER ARRAY
);

CREATE TABLE places (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    geo TEXT,
    description TEXT,
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
    ex_others INTEGER ARRAY
);

CREATE TABLE persons (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    person TEXT NOT NULL,
    description TEXT,
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
    ex_others INTEGER ARRAY
);

CREATE TABLE others (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    meta TEXT,
    description TEXT,
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
    ex_others INTEGER ARRAY
);

CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    min TEXT NOT NULL,
    max TEXT NOT NULL,
    level TEXT,
    description TEXT,
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
    ex_others INTEGER ARRAY
);

-- ЗАПОЛНИТЬ ТАБЛИЦЫ 

INSERT INTO sources VALUES 
(
    '1', 'Запись из личного архива №123321. Может быть автор.', '1 авг', 'Описание источника. Автор. Доступно по ссылке http://aboba', 'Абоба боба бибиович', 'http://aboba',
    null, '{1, 6}', null, '{1, 2, 5}',
    null, '{1}', null, '{1, 2}',
    null, '{2}', null, '{1}'
),
(
    '2', 'Запись из личного архива №123321-2. Может быть автор.', 'IX-XX вв.', 'Описание источника. Автор. Доступно по ссылке http://aboba {source:1}[родительский источник]', 'Абоба боба бибиович', 'http://aboba',
    null, '{2, 6}', null, null,
    null, null, null, null,
    '{1}', null, null, null
);

INSERT INTO dates VALUES 
(
    '1', '31.08.2023 20:27:11111', 'АБОБА DATE', 'Описание для ?внутренних целей? ({source : 1}[источник])', 
    null, null, null, '{5}',
    null, null, null, '{1}',
    '{1}', null, null, null
),
(
    '2', '23.08.2023', 'АБОБА DATE', 'Многострочное описание события 2 ({source : 1}[источник]) а теперь здесь есть ссылка на {person:1}[челика]', 
    null, null, null, null,
    null, '{1}', '{1}', null,
    '{1}', null, null, null
),
(
    '3', '"Дата августовского путча"', 'АБОБА DATE', null, 
    null, null, null, null,
    null, '{1}', null, '{2}',
    null, null, null, null
),
(
    '4', '18 ноября 2024', 'АБОБА DATE', null, 
    null, null, null, null,
    null, '{1}', null, null,
    null, null, null, null
),
(
    '5', '23 июня 2023', 'АБОБА DATE', 'Описание события 5, которое было бы после {date:1}[этого], но не случилось ({source : 1}[источник])', 
    null, null, '{1}', null,
    null, null, null, null,
    '{1}', null, null, null
);

INSERT INTO places VALUES 
(
    '1', 'Жепа', 'геолокация или имя или ещё чего', 'Город Жепа основан в {date:4}[основание города жепа] мог бы быть, но так не случилось, поэтому в {date:3}[какое-то контекстное название] тоже ничего не получилось, а в {date:2}[склонение] вообще так не получилось, что до сих пор не получается. ({source : 1}[источник])', 
    null, '{6}', '{2, 3, 4}', null,
    null, null, null, '{1, 2}',
    '{1}', null, null, null
);

INSERT INTO persons VALUES 
(
    '1', 'Абоба Максим Маркович', 'Абоба Максим Маркович', 'Абоба Максим Маркович родился {date:1}[сегодня] в городе {place:1}[Жепа] ({source : 1}[источник])', 
    null, '{1, 6}', '{1}', '{2}',
    '{1}', null, null, '{2}',
    '{1}', null, null, '{1}'
),
(
    '2', 'Абоба Марк Андреевич', 'Абоба Максим Маркович', 'Абоба-старший родился задолго до {date:3}[авг путча], но только после этого он эмигрировал в {place:1}[Жепу]. Тогда как {person:1}[Абоба Максим] остался. ({source:1}[источник])', 
    null, null, '{3}', null,
    '{1}', null, '{1}', null,
    '{1}', null, null, null
);

INSERT INTO others VALUES 
(
    '1', 'ABOBA NMAE', 'КАКАЯ_ТО_МЕТА_ИНФОРМАЦИЯ', 'DESCRIPTION {source:1}[источник] ааа {person:1}[Абоба Максим]', 
    null, null, null, null,
    null, null, '{1}', null,
    '{1}', null, null, null
);

INSERT INTO events VALUES 
(
    '1', 'Крестьянина выгнали', 'дата, когда его выгнали нафик', 'Креста {person:1}[Жопошника] выгнали за то, что он был жопошником.', 'Подробное объяснение, что креста {person:1}[Жопошника] выгнали за то, что он был жопошником, да ещё таким отпетым жопошником. {source:1}[По свидетельствам] жопопинателей, он был жопошником.', 'FACT', null, 
    null, '{2}', null, null,
    null, null, '{1}', null,
    '{1}', null, null, null
),
(
    '2', 'Жопошников выгоняли', 'промежуток дат', 'Крестов-жопошников выгоняли по мнгогим причинам', 'Крестов-жопошников выгоняли по мнгогим причинам: так, {event:1}[?]. Таким образом, если учитывать {source:2}[источники], жопошников выгоняли нафик', 'GENERAL', null, 
    '{1}', '{3}', null, null,
    null, null, null, null,
    '{2}', null, null, null
),
(
    '3', 'Процесс ослабления общин', 'не знаю, как обрабатывать потом такое количество свободно описываемых в форматах дат', 'Общины ослаблялись по многим причинам (причины)', 'По многим причинам ослаблялись общины. {event:2}[?]. Таким образом, общины ослаблялись.', 'PROCESS', null, 
    '{2}', '{4}', null, null,
    null, null, null, null,
    null, null, null, null
),
(
    '4', 'ЧТО БЫЛО', '1-1', 'Было очень плохо. Жопошников выгоняли. Ещё чего только не делали.', 'Было очень плохо (текст как было плохо). Общины ослаблялись {event:3}[?] Ещё подзаголовок Вот как было плохо', 'STATE', null, 
    '{3}', '{5}', null, null,
    null, null, null, null,
    null, null, null, null
),
(
    '5', 'Аграрная реформа', 'век-век год-год', 'Реформа была крутая, а ещё немного некрутая.', 'Реформа была крутая, потому что назрела. Состояние сельского хозяйство было плачевным. {event:4}[?]. Реформа должна была преследовать цели. Таким образом, был запущен процесс чего-то (ХОД) В итоге всё сталок руто но не очень круто (ИТОГИ).', 'EVENT', null, 
    '{4}', '{6}', null, null,
    null, null, null, null,
    null, null, null, null
),
(
    '6', 'Столыпин', 'ВЕК', 'да вот тако мужик', 'мужик ничё вот {source:1}[aboba] {source:2}[aboba] {event:5}[его реформа] {person:1}[перс] {place:1}[место]', 'CORE', null, 
    '{5}', null, null, null,
    '{1}', null, '{1}', null,
    '{1, 2}', null, null, null
);

