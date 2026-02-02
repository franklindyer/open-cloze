CREATE TABLE groups (
    id INT NOT NULL AUTO_INCREMENT,
    label CHAR(3) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE langs (
    id INT NOT NULL AUTO_INCREMENT,
    iso2 CHAR(2) NOT NULL,
    iso3 CHAR(3) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE sentences (
    id INT NOT NULL AUTO_INCREMENT,
    group_id INT NOT NULL,
    lang_id INT NOT NULL,
    text TEXT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE lemma (
    id INT NOT NULL AUTO_INCREMENT,
    lang_id INT NOT NULL,
    text TEXT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE puzzles (
    id INT NOT NULL AUTO_INCREMENT,
    sentence_id INT NOT NULL,
    lemma_id INT NOT NULL,
    intervals TEXT NOT NULL,
    PRIMARY KEY (id)
);
