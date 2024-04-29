# Catsume

Web scraper for [Montreal SPCA](spca.com) adoption pages.

## Setup

Install requirements using `pip`:

```sh
pip install -r requirements.txt
```

## Usage

Run the following command to output JSON representing animals that are
currently available for adoption:

```sh
python -m libcatsume --cats
```

In order to minimize scraping, only animal types specified via runtime arguments
will be included in the output. Available arguments are as follows:

| Flag | Name              | Description                                       |
| ---- | ----------------- | ------------------------------------------------- |
| `-a` | `--all`           | Include all animals available for adoption.       |
| `-b` | `--birds`         | Include all birds available for adoption.         |
| `-c` | `--cats`          | Include all cats available for adoption.          |
| `-d` | `--dogs`          | Include all dogs available for adoption.          |
| `-r` | `--rabbits`       | Include all rabbits available for adoption.       |
| `-s` | `--small-animals` | Include all small animals available for adoption. |

## License

[MIT](LICENSE.md)
