import argparse
import pathlib

from src.extractor import reader
from src.extractor import schemas as extractor_schemas
from src.grouper import catalog as catalog_grouper
from src.loader import encoders as loader_enc
from src.loader import loader
from src.transformer import transformer

CSV_DELIMITER_DEFAULT = ";"


def run_pipeline(
    source_file: reader.CsvFileReaderMeta, mappings_file: reader.CsvFileReaderMeta
) -> None:
    """Run the ETL pipeline.

    Perform following operations:

        - Extract data from the source and mappings CSV files.
        - Transform it using predefined strategies.
        - Group the transformed data into a catalog.
        - Consolidate common attributes at the article and catalog levels.
        - Serialize the catalog to JSON and output to stdout.

    Args:
        source_file (reader.CsvFileReaderMeta): Metadata for the source CSV file.
        mappings_file (reader.CsvFileReaderMeta): Metadata for the mappings CSV file.
    """
    # Extract
    # Read all mappings at once
    mappings_reader_by_row = reader.CsvReader(
        file_meta=mappings_file,
        validation_schema=extractor_schemas.CsvMappingSchemaRequired,
    ).read_by_row()

    # Transform all mappings at once
    mapping = transformer.Mapping()
    mapping.build(mapping_rows=mappings_reader_by_row)

    # Read, transform and group source file into a catalog by row
    catalog = catalog_grouper.Catalog.new()

    for row in reader.CsvReader(
        file_meta=source_file,
        validation_schema=extractor_schemas.CsvSourceSchemaRequired,
    ).read_by_row():
        transformed_row = transformer.transform_row(source_row=row, mapping=mapping)
        catalog = catalog.add(flat_data_row=transformed_row)

    # Regroup catalog
    catalog_grouper.consolidate_common_attributes(catalog=catalog)

    # Load
    serialised_catalog = loader.encode_to_json(
        obj=catalog, encoder_cls=loader_enc.DataClassJsonEncoder
    )
    # Output to stdout
    print(serialised_catalog)


def parse_cli() -> tuple[reader.CsvFileReaderMeta, reader.CsvFileReaderMeta]:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--source",
        type=pathlib.Path,
        help="Path to the source file",
        required=True,
    )
    parser.add_argument(
        "-m",
        "--mappings",
        type=pathlib.Path,
        help="Path to the mappings file",
        required=True,
    )
    parser.add_argument(
        "-d",
        "--delimiter",
        type=str,
        help="Delimiter",
        required=False,
        default=CSV_DELIMITER_DEFAULT,
    )
    args = parser.parse_args()
    return (
        reader.CsvFileReaderMeta(
            path=pathlib.Path(args.source), delimiter=args.delimiter
        ),
        reader.CsvFileReaderMeta(
            path=pathlib.Path(args.mappings), delimiter=args.delimiter
        ),
    )


def main() -> None:
    """Parse CLI args and run the ETL pipeline."""
    run_pipeline(*parse_cli())


if __name__ == "__main__":
    main()
