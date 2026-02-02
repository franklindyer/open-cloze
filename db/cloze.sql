CREATE TABLE puzzle_groups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    label CHAR(30) NOT NULL
);

CREATE TABLE langs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    iso3 CHAR(3) NOT NULL
);

CREATE TABLE sentences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    position INT NOT NULL,
    group_id INT NOT NULL,
    lang_id INT NOT NULL,
    text TEXT NOT NULL
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
