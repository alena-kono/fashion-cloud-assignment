import pytest

from src.grouper.catalog import (
    Article,
    Catalog,
    FlatDictRow,
    _level_up_common_attributes_to_article_level,
    _level_up_common_attributes_to_catalog_level,
)


@pytest.mark.unit()
@pytest.mark.parametrize(
    ("flat_rows", "expected"),
    [
        (
            [
                {
                    "article_number": "a",
                    "name": "fancy dream",
                    "colour": "black",
                    "price": "125",
                },
                {
                    "article_number": "a",
                    "name": "fancy dream hearts",
                    "colour": "red",
                    "price": "2",
                },
            ],
            Catalog(
                common_attributes={},
                articles={
                    "a": Article(
                        article_number="a",
                        variations=[
                            {
                                "name": "fancy dream",
                                "colour": "black",
                                "price": "125",
                            },
                            {
                                "name": "fancy dream hearts",
                                "colour": "red",
                                "price": "2",
                            },
                        ],
                        common_attributes={},
                    ),
                },
            ),
        ),
        (
            [
                {
                    "article_number": "a",
                    "name": "fancy dream",
                    "colour": "black",
                    "price": "125",
                },
                {
                    "article_number": "b",
                    "name": "another",
                    "colour": "blue",
                    "price": "35",
                },
            ],
            Catalog(
                common_attributes={},
                articles={
                    "a": Article(
                        article_number="a",
                        variations=[
                            {
                                "name": "fancy dream",
                                "colour": "black",
                                "price": "125",
                            },
                        ],
                        common_attributes={},
                    ),
                    "b": Article(
                        article_number="b",
                        variations=[
                            {
                                "name": "another",
                                "colour": "blue",
                                "price": "35",
                            },
                        ],
                        common_attributes={},
                    ),
                },
            ),
        ),
        (
            [],
            Catalog(articles={}, common_attributes={}),
        ),
    ],
    ids=["one_article_two_variations", "two_articles_one_variation", "empty_input"],
)
def test_catalog_add(flat_rows: list[FlatDictRow], expected: Catalog) -> None:
    catalog = Catalog.new()

    for row in flat_rows:
        catalog.add(flat_data_row=row)

    assert catalog == expected


@pytest.mark.functional()
@pytest.mark.parametrize(
    ("article", "expected_article"),
    [
        (
            Article(
                article_number="001",
                variations=[
                    {"name": "same", "colour": "black", "price": "125"},
                    {"name": "same", "colour": "white", "price": "125"},
                    {"name": "same", "colour": "red", "price": "125"},
                ],
                common_attributes={},
            ),
            Article(
                article_number="001",
                variations=[
                    {"colour": "black"},
                    {"colour": "white"},
                    {"colour": "red"},
                ],
                common_attributes={"name": "same", "price": "125"},
            ),
        ),
        (
            Article(
                article_number="002",
                variations=[
                    {"name": "A", "colour": "black", "price": "125"},
                    {"name": "B", "colour": "white", "price": "150"},
                    {"name": "C", "colour": "red", "price": "175"},
                ],
                common_attributes={},
            ),
            Article(
                article_number="002",
                variations=[
                    {"name": "A", "colour": "black", "price": "125"},
                    {"name": "B", "colour": "white", "price": "150"},
                    {"name": "C", "colour": "red", "price": "175"},
                ],
                common_attributes={},
            ),
        ),
        (
            Article(article_number="003", variations=[], common_attributes={}),
            Article(article_number="003", variations=[], common_attributes={}),
        ),
        (
            Article(
                article_number="004",
                variations=[
                    {"name": "same", "colour": "black", "price": "125"},
                    {"name": "same", "colour": "white", "price": "125"},
                    {"name": "same", "colour": "red", "price": "125"},
                ],
                common_attributes={},
            ),
            Article(
                article_number="004",
                variations=[
                    {"colour": "black"},
                    {"colour": "white"},
                    {"colour": "red"},
                ],
                common_attributes={"name": "same", "price": "125"},
            ),
        ),
    ],
    ids=[
        "common_attributes_are_leveled_up",
        "no_common_attributes",
        "empty_variations",
        "same_common_attributes_are_leveled_up",
    ],
)
def test_level_up_common_attributes_to_article_level(
    article: Article, expected_article: Article
) -> None:
    _level_up_common_attributes_to_article_level(article)

    assert article.variations == expected_article.variations
    assert article.common_attributes == expected_article.common_attributes


@pytest.mark.functional()
@pytest.mark.parametrize(
    ("catalog", "expected_catalog"),
    [
        (
            Catalog(
                articles={
                    "001": Article(
                        article_number="001",
                        variations=[
                            {"name": "A", "colour": "black", "price": "125"},
                            {"name": "B", "colour": "white", "price": "150"},
                        ],
                        common_attributes={"brand": "asos"},
                    ),
                    "002": Article(
                        article_number="002",
                        variations=[
                            {"name": "C", "colour": "red", "price": "175"},
                            {"name": "D", "colour": "blue", "price": "200"},
                        ],
                        common_attributes={"brand": "asos"},
                    ),
                },
                common_attributes={},
            ),
            Catalog(
                articles={
                    "001": Article(
                        article_number="001",
                        variations=[
                            {"name": "A", "colour": "black", "price": "125"},
                            {"name": "B", "colour": "white", "price": "150"},
                        ],
                        common_attributes={},
                    ),
                    "002": Article(
                        article_number="002",
                        variations=[
                            {"name": "C", "colour": "red", "price": "175"},
                            {"name": "D", "colour": "blue", "price": "200"},
                        ],
                        common_attributes={},
                    ),
                },
                common_attributes={"brand": "asos"},
            ),
        ),
        (
            Catalog(
                articles={
                    "001": Article(
                        article_number="001",
                        variations=[
                            {"name": "A", "colour": "black", "price": "125"},
                            {"name": "B", "colour": "white", "price": "150"},
                        ],
                        common_attributes={},
                    ),
                    "002": Article(
                        article_number="002",
                        variations=[
                            {"name": "C", "colour": "red", "price": "175"},
                            {"name": "D", "colour": "blue", "price": "200"},
                        ],
                        common_attributes={},
                    ),
                },
                common_attributes={},
            ),
            Catalog(
                articles={
                    "001": Article(
                        article_number="001",
                        variations=[
                            {"name": "A", "colour": "black", "price": "125"},
                            {"name": "B", "colour": "white", "price": "150"},
                        ],
                        common_attributes={},
                    ),
                    "002": Article(
                        article_number="002",
                        variations=[
                            {"name": "C", "colour": "red", "price": "175"},
                            {"name": "D", "colour": "blue", "price": "200"},
                        ],
                        common_attributes={},
                    ),
                },
                common_attributes={},
            ),
        ),
        (
            Catalog(articles={}, common_attributes={}),
            Catalog(articles={}, common_attributes={}),
        ),
    ],
    ids=[
        "common_attributes_are_leveled_up_including_common_article_attrs",
        "no_common_attributes",
        "empty_catalog",
    ],
)
def test_level_up_common_attributes_to_catalog_level(
    catalog: Catalog, expected_catalog: Catalog
) -> None:
    _level_up_common_attributes_to_catalog_level(catalog)

    assert catalog.articles == expected_catalog.articles
    assert catalog.common_attributes == expected_catalog.common_attributes
