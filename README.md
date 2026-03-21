# open-cloze

Open-source software for generating Cloze puzzles (in the style of Clozemaster) from parallel sentence data using the Python SpaCy library for tokenization/lemmatization.

Compatible with my open-source Flashcard app called [Pfeil](https://github.com/franklindyer/flashcards).

![example cloze flashcard](/img/puzzle-example.png)

## Existing API usage

API requests can be made via `GET` or `POST` requests to the server's URL endpoint. The supported arguments are as follows:

- `tgt` (required): the 3-letter ISO code for the target language
- `src` (required): a comma-separated list of 3-letter ISO codes for your known/source languages
- `lemma` (required): the base form of the word that you want Cloze puzzles for
- `n` (optional): the desired number of results (server may return based on its own result cap and how many puzzles are available)
- `maxlen` (optional): the desired maximum length of returned sentences

## Creating your own puzzle database

By following these steps, you can create your own Cloze puzzles and access them through a web API.

**Step 1.** Identify sources of parallel sentences that you can use for puzzles. A list of suggestions to get you started is in the section below. Come up with a short "nickname" for each source.

**Step 2.** In the `./data` folder, create one subdirectory for each source of parallel sentences that you plan on using.

**Step 3.** For each of your data sources (i.e. for each subdirectory of `./data`), for each language of data that you want to use for that source, create a file called `./XXX.tsv`, replacing `XXX` with the 3-letter ISO language code for that language (e.g. `deu` for German, `eng` for English, etc). Each of those files should consist of rows with 2 entries, the first being a unique ID number for each sentence, and the second being the sentence itself. Sentences must not contain any newline or tab characters. Furthermore, ID numbers must be unique between ALL sentences within a subdirectory (not just unique within each TSV file).

**Step 4.** In each data source subdirectory, also add a file called `links.csv` in which each line contains a comma-separated pair of ID numbers. These "links" should describe which pairs of sentences in different language-segregated TSV files of that folder are "linked to each other", i.e. which pairs of sentences are translations of each other. 

Note that providing sentence-list TSV files and link-list CSV files is your responsibility - if you have parallel sentences in some other format, you will have to rework them into this required format on your own, e.g. by writing a Python or Bash script for doing so. However, there is some example data in `./data/test` to show you how these subdirectories should look.

**Step 5.** Create a JSON file called `conf.json` in the root directory. Here is an example of what that file should look like (using only data from the provided `test` subdirectory):

```
{
    "groups": {
        "test": {
            "sentences": ["eng", "spa"],
            "puzzles": ["spa"]
        }
    }
}
```

The `groups` subobject should contain a field for each subdirectory in `./data` that you want to generate puzzles from. (Any subdirectories not referenced in this JSON file will just be ignored.) For each subobject corresponding to a data-source subdirectory, `puzzles` is a list of languages whose sentences should be converted into "fill-in-the-blank" Cloze puzzles, whereas `sentences` is a list of languages whose sentences should be included as linked sentences (but not necessarily made into puzzles themselves). For example, if all of the people using your server are English speakers who want to learn Spanish, `sentences` should be `["eng", "spa"]`, but `puzzles` should be `["spa"]` (because those people do not need any Cloze puzzles for quizzing them on English words).

**Step 6.** Create a `python3.13` virtual environment, activate it, and install the dependencies in `requirements.txt`. Also make sure you have `Docker` and `sqlite3` installed.

**Step 7.** Run the following commands:

```
python3 src/puzzle_builder.py
sqlite3 db/cloze.sqlite < schemas/cloze.sqlite
python3 src/db_builder.py
python3 src/db_cleaner.py
```

Commands 1, 3 and/or 4 may take a long time to run, especially the first command, since it performs NLP using the Python library SpaCy on all of your provided sentences. This step requires a lot of CPU usage, so don't run it unless you are ready for a long wait and a battery drain.

**Step 8.** Now the database file `db/cloze.sqlite` has been built and you are ready to run the server! Run the following commands to build and run the server locally:

```
docker compose build server
docker compose up server -d
```

The server should be available at `http://localhost:5052` for API requests. To shut it down again:

```
docker compose down
```

## Data sources

- The [Tatoeba Project](https://tatoeba.org/en) is a great source of parallel sentences, and it's open source!
- The [EUROPARL Parallel Corpus](https://www.statmt.org/europarl/) is a good source of sentence pairs using formal/elevated language in many European languages
- You can also try to scrape subtitles/captions [from your favorite games](https://github.com/franklindyer/skyrim-subtitles)

## Creating a specialized puzzle generator for a language

TODO

## Developer TODO list

- [ ] a huge number of sentences in the DB are not used for puzzles or linked to any sentences that are, either prune these from the DB or build the DB in such a way that they never get added
- [ ] I think sentences should be given a globally unique ID from now on, rather than being uniquely IDed by the combo of their group and (inner-group) ID number, which may also offer a speedup (in addition to just simplifying things a whole lot)
- [ ] add optional "maximum length" field to API queries so the user can specify a max result length
- [ ] add actual documentation with setup instructions and API specs


