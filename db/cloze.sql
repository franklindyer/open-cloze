CREATE TABLE puzzle_groups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    label CHAR(3) NOT NULL
);

CREATE TABLE langs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    iso2 CHAR(2) NOT NULL,
    iso3 CHAR(3) NOT NULL
);

CREATE TABLE sentences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    group_id INT NOT NULL,
    lang_id INT NOT NULL,
    text TEXT NOT NULL
);

CREATE TABLE links (
    id1 INT NOT NULL,
    id2 INT NOT NULL
);

CREATE TABLE lemmas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lang_id INT NOT NULL,
    text TEXT NOT NULL
);

CREATE TABLE puzzles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sentence_id INT NOT NULL,
    lemma_id INT NOT NULL,
    intervals TEXT NOT NULL
);
