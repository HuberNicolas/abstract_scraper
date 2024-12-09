
# Abstract Scraper

`abstract-scraper` is a Python-based CLI tool for fetching abstracts of scientific articles from DOIs. It uses the [Pyalex](https://github.com/mattbierbaum/pyalex) library for accessing metadata from the OpenAlex API, allowing efficient and parallelized processing of large datasets.

## Features
- Fetches abstracts for scientific articles using their DOIs.
- Supports parallel processing with configurable worker count.
- Periodically saves progress to prevent data loss.
- Simple and intuitive command-line interface (CLI).

---

## Installation

### Prerequisites
- Python 3.12 or later
- [Poetry](https://python-poetry.org/) for dependency management

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/HuberNicolas/abstract_scraper
   cd abstract-scraper
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

---

## Usage

Run the script with the following command:
```bash
python -m main <input_file> <output_file> [--num_workers <int>] [--save_interval <int>]
```

### Required Arguments
- `<input_file>`: Path to the CSV file containing a column `doi` with DOIs of the articles.
- `<output_file>`: Path where the updated CSV with fetched abstracts will be saved.

### Optional Arguments
- `--num_workers`: Number of parallel workers to use (default: 4).
- `--save_interval`: Save progress after processing this many rows (default: 50).

### Example
```bash
poetry shell # activate poetry env
python -m main data/sdg_data.csv data/sdg_data_abstracts.csv --num_workers 2 --save_interval 10
```

---

## Input File Format

The input CSV file must include a `doi` column with the DOIs of the articles. Example:

| doi                   |
|-----------------------|
| 10.1234/example-doi-1 |
| 10.5678/example-doi-2 |

---

## Output File

The script saves the output CSV with the following additional column:
- **`abstract`**: Contains the fetched abstract for each article.

Example output:
| doi                   | abstract                                |
|-----------------------|-----------------------------------------|
| 10.1234/example-doi-1 | This is an example abstract.           |
| 10.5678/example-doi-2 | Another example abstract.              |

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.
