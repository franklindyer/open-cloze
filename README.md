TODO:
- [ ] a huge number of sentences in the DB are not used for puzzles or linked to any sentences that are, either prune these from the DB or build the DB in such a way that they never get added
- [ ] I think sentences should be given a globally unique ID from now on, rather than being uniquely IDed by the combo of their group and (inner-group) ID number, which may also offer a speedup (in addition to just simplifying things a whole lot)
- [ ] add optional "maximum length" field to API queries so the user can specify a max result length
- [ ] add actual documentation with setup instructions and API specs

Sample `conf.json` file for just the test data:
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

## Existing API usage

TODO

## Creating your own puzzle database

TODO
