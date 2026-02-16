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

## Database dump

You can enter the database container with the following command:

```
docker exec -it mysql bash -l
```

And you can dump the database to a file by running:

```
mysqldump -p -u root --databases cloze > /dump/cloze.sql
```
