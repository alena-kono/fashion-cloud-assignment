# Fashion Cloud Assignment: code

## Overview

This ETL (Extract, Transform, Load) pipeline is designed to process data from 
a source CSV file and a mappings CSV file. It performs the following operations:

1. **Extract**: Reads data from the source and mappings CSV files.
2. **Transform**: Applies predefined transformation strategies.
3. **Group**: Organizes the transformed data into a catalog.
4. **Consolidate**: Aggregates common attributes at the article and catalog levels.
5. **Load**: Serializes the catalog into JSON format and outputs it to stdout.

## Solution
### Assumptions

After the requirements analysis, I made the following assumptions.

#### Size of data

- According to the task, we receive a price catalog with shoes from 
a shoe supplier as an input.

- Large supplier can have up to 1800 articles in the active assortment.
See [ref](https://www.blog.datahut.co/post/competitive-analysis-nike-vs-adidas).

- I calculated size of data roughly assuming that
full size range and multiple colours are presented in the supplier's product line.


| Metric                          | Value         |
|---------------------------------|---------------|
| Articles count                  | 1,799         |
| Sizes count per article         | 28            |
| Colours count per article       | 14            |
| Rows count per article          | 392           |
| Chars in field, incl delimiters | 145           |
| Fields count per row            | 21            |
| Row size, bytes                 | 3,045         |
| Rows count                      | 705,249       |
| Total size, bytes               | 2,147,358,360 |
| Total size, GB                  | 2             |

- _Assumption: 2-3 Gb of data can be received from a big shoe supplier at once._
- However, an average scenario is a supplier loading data into our system incrementally.
Therefore, the size of the data would be smaller in the average scenarios.

#### Frequency of updates
- Updates should be loaded 1-2 times per quarter. It is not frequent operation.

#### State of the source data
- Source data may be unsorted.
- The original order of the data does not necessarily need to be retained after mapping.

#### Output
- Output data may be unsorted.
- The original order of the data does not necessarily need to be retained after mapping.

### Decisions

Taking into account the above assumptions, I have made the following decisions:
- Process source data in-memory with generators: read, transform, group.
MapReduce would be an overkill even in production (if less than 100 Tb of data) because of its complex setup.
- Process mapping data all at once, as we need a complete picture for further transformations.
- Use hashmap (dictionary) with a composite key for efficient access to mappings data.
- Consolidate grouped data (level up common attributes) all at once.
- Output consolidated data to stdout as it can be streamed into the file if needed.

If developing such app for production (with no `pandas` allowed), I would consider firstly:
- Focus on corner cases.
- Handle exceptions properly, maybe implement back-off/recovering system.
- Save intermediate results to the temp files. It will allow to recover smoothly.
- Maybe sort source data to be able to perform grouping in efficient manner.
- Log.

## Features

- [x] Apply following mapping strategies to transform data: direct and combined.
- [x] (Bonus) Have configurable option to combine multiple fields into a new field
using whitespace as a separator. 
It can be configured via mappings.csv file as follows:

| source | destination | source_type             | destination_type       |
|--------|-------------|-------------------------|------------------------|
| *      | *           | price_buy_net\|currency | price_buy_net_currency |

Check the last line in [mappings_bonus.csv](tests/data/input/mappings_bonus.csv).

- [x] Group data into a hierarchical catalog structure.
- [x] Identify and consolidate common attributes at multiple levels (variations, articles).
- [x] Output the final catalog in JSON format to stdout.
- [x] (Bonus) Provide basic (very basic) tests coverage (unit, integration, e2e).

## Prerequisites

- `python3.12`

## Installation

No external dependencies is needed.

### Development
`poetry` is used for the development.

To install the required dev dependencies, use the following command:

```bash
poetry install
```

## Usage

1. Activate `python` virtual environment. 
2. To run the pipeline, you need to provide paths to the source CSV file 
and the mappings CSV file.

The CLI allows to run the pipeline with the following arguments:

- `-s` or `--source`: Path to the source CSV file (required).
- `-m` or `--mappings`: Path to the mappings CSV file (required).
- `-d` or `--delimiter`: Delimiter used in the CSV files (optional, default is `;`).

### Example Command

```bash
python -m src.main \
          -s tests/data/input/pricat.csv \
          -m tests/data/input/mappings.csv \
          -d ";"
```

### Example Output

The output will be a JSON representation of the consolidated catalog printed to stdout.
<details>
  <summary>Click to check output example</summary>
  
```json
{
  "articles": {
    "15189-02": {
      "article_number": "15189-02",
      "variations": [
        {
          "ean": "8719245200978",
          "article_number_2": "15189-02 Aviation Nero",
          "article_number_3": "Aviation",
          "color_code": "1",
          "size_code": "38",
          "size_name": "38",
          "price_buy_net": "58.5",
          "size": "European size 38",
          "color": "Nero"
        }
      ],
      "common_attributes": {
        "article_structure": "Pump",
        "article_structure_code": "10"
      }
    },
    "4701013-00": {
      "article_number": "4701013-00",
      "variations": [
        {
          "ean": "8719245192310",
          "article_number_2": "4701013-00 Caipirinha Nero",
          "article_number_3": "Caipirinha",
          "color_code": "1",
          "size_code": "38",
          "size_name": "38",
          "size": "European size 38",
          "color": "Nero"
        }
      ],
      "common_attributes": {
        "price_buy_net": "71",
        "article_structure_code": "4",
        "article_structure": "Boot"
      }
    }
  },
  "common_attributes": {
    "brand": "Via Vai"
  }
}
```
</details>


## Running tests

```bash
pytest
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.