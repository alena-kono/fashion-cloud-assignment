import pytest

from src.extractor.reader import Row
from src.transformer.transformer import (
    MapAttr,
    Mapping,
    MappingUnit,
    transform_row,
)


@pytest.mark.parametrize(
    ("row", "expected"),
    [
        (
            {
                "source": "1",
                "destination": "black",
                "source_type": "color_code",
                "destination_type": "color",
            },
            MappingUnit(
                source=MapAttr(val="1", type_="color_code"),
                destination=MapAttr(val="black", type_="color"),
            ),
        ),
    ],
)
def test_mapping_unit_from_row(row: Row, expected: MappingUnit) -> None:
    assert MappingUnit.from_row(row) == expected


@pytest.mark.unit()
@pytest.mark.parametrize(
    (
        "mapping_rows",
        "expected_direct_items",
        "expected_composite_items",
        "expected_glob_items",
    ),
    [
        (
            [
                {
                    "source": "1",
                    "destination": "black",
                    "source_type": "color_code",
                    "destination_type": "color",
                },
            ],
            {
                "1.color_code": MappingUnit(
                    source=MapAttr(val="1", type_="color_code"),
                    destination=MapAttr(val="black", type_="color"),
                )
            },
            {},
            {},
        ),
        (
            [
                {
                    "source": "1",
                    "destination": "black",
                    "source_type": "color_code",
                    "destination_type": "color",
                },
                {
                    "source": "2",
                    "destination": "green",
                    "source_type": "color_code",
                    "destination_type": "color",
                },
            ],
            {
                "1.color_code": MappingUnit(
                    source=MapAttr(val="1", type_="color_code"),
                    destination=MapAttr(val="black", type_="color"),
                ),
                "2.color_code": MappingUnit(
                    source=MapAttr(val="2", type_="color_code"),
                    destination=MapAttr(val="green", type_="color"),
                ),
            },
            {},
            {},
        ),
        (
            [
                {
                    "source": "EU|36",
                    "destination": "European size 36",
                    "source_type": "size_group_code|size_code",
                    "destination_type": "size",
                },
            ],
            {},
            {
                "EU|36.size_group_code|size_code": MappingUnit(
                    source=MapAttr(val="EU|36", type_="size_group_code|size_code"),
                    destination=MapAttr(val="European size 36", type_="size"),
                ),
            },
            {},
        ),
        (
            [
                {
                    "source": "*",
                    "destination": "*",
                    "source_type": "price|currency",
                    "destination_type": "price_currency",
                },
            ],
            {},
            {},
            {
                "*.price|currency": MappingUnit(
                    source=MapAttr(val="*", type_="price|currency"),
                    destination=MapAttr(val="*", type_="price_currency"),
                ),
            },
        ),
    ],
    ids=[
        "one_mapping_color",
        "two_mappings_colors",
        "one_mapping_combined_size",
        "one_glob_item",
    ],
)
def test_mapping_build_ok(
    mapping_rows: list[Row],
    expected_direct_items: dict[str, MapAttr],
    expected_composite_items: dict[str, MapAttr],
    expected_glob_items: dict[str, MapAttr],
) -> None:
    mapping = Mapping()
    mapping.build(mapping_rows=mapping_rows)

    assert mapping.direct_items == expected_direct_items
    assert mapping.composite_items == expected_composite_items
    assert mapping.glob_items == expected_glob_items


@pytest.mark.parametrize(
    ("source_row", "expected_row"),
    [
        (
            {
                "article_number": "001",
                "name": "tee",
                "price": "1500",
                "size_code": "36",
                "color_code": "1",
            },
            {
                "article_number": "001",
                "name": "tee",
                "price": "1500",
                "size_code": "36",
                "color_code": "1",
                "size": "36 EUR",
                "color": "black",
                "color_code_size_code": "1 36",
                "price_size_code": "1500 for 36 size",
            },
        ),
        (
            {
                "article_number": "001",
                "name": "tee",
                "size_code": "36",
            },
            {
                "article_number": "001",
                "name": "tee",
                "size_code": "36",
                "size": "36 EUR",
            },
        ),
        (
            {
                "article_number": "001",
                "size_code": "36",
                "size": "36 EUR",
                "price": "1500",
            },
            {
                "article_number": "001",
                "size_code": "36",
                "size": "36 EUR",
                "price": "1500",
                "price_size_code": "1500 for 36 size",
            },
        ),
        (
            {
                "article_number": "001",
                "size_code": "36",
                "size": "36 EUR",
                "price": "888",
            },
            {
                "article_number": "001",
                "size_code": "36",
                "size": "36 EUR",
                "price": "888",
            },
        ),
        (
            {
                "article_number": "001",
                "size_code": "36",
                "size": "36 EUR",
                "color_code": "1",
                "color": "black",
            },
            {
                "article_number": "001",
                "size_code": "36",
                "size": "36 EUR",
                "color_code": "1",
                "color": "black",
                "color_code_size_code": "1 36",
            },
        ),
        (
            {
                "article_number": "001",
                "unmapped_type": "abc",
            },
            {
                "article_number": "001",
                "unmapped_type": "abc",
            },
        ),
        ({}, {}),
    ],
    ids=[
        "transform_all_attrs",
        "transform_direct_attrs",
        "transform_composite_attrs",
        "not_transform_not_equal_composite_attrs",
        "transform_glob_attrs",
        "no matching attributes",
        "empty row",
    ],
)
def test_transform_row(source_row: Row, expected_row: Row) -> None:
    mapping = Mapping()
    mapping.build(
        [
            {
                "source": "1",
                "source_type": "color_code",
                "destination": "black",
                "destination_type": "color",
            },
            {
                "source": "36",
                "source_type": "size_code",
                "destination": "36 EUR",
                "destination_type": "size",
            },
            {
                "source": "*",
                "source_type": "color_code|size_code",
                "destination": "*",
                "destination_type": "color_code_size_code",
            },
            {
                "source": "1500|36",
                "source_type": "price|size_code",
                "destination": "1500 for 36 size",
                "destination_type": "price_size_code",
            },
        ]
    )
    assert transform_row(source_row, mapping) == expected_row
