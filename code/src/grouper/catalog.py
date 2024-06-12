import dataclasses
import typing as tp

from src.grouper.exceptions import RequiredFieldMissingError
from src.grouper.utils import (
    collect_common_attributes,
    remove_attributes_inplace,
)

FlatDictRow = dict[str, str]
Variation = dict[str, tp.Any]
Attributes = dict[str, tp.Any]


@dataclasses.dataclass()
class Article:
    """An article with its variations and common attributes.

    Attributes:
        article_number (str): The unique identifier for the article.
        variations (list[Variation]): A list of variations for the article.
        common_attributes (Attributes): A dictionary of attributes common to
            all variations of the article.
    """

    article_number: str
    variations: list[Variation]
    common_attributes: Attributes


@dataclasses.dataclass()
class Catalog:
    """A catalog containing multiple articles and their common attributes.

    Attributes:
        articles (dict[str, Article]): A dictionary of articles
            indexed by their article number.
        common_attributes (Attributes): A dictionary of attributes
            common to all articles in the catalog.
    """

    articles: dict[str, Article]
    common_attributes: Attributes

    @classmethod
    def new(cls) -> tp.Self:
        """Create a new Catalog instance with empty articles and common attributes.

        Returns:
            Catalog: A new instance of the Catalog class.
        """
        return cls(articles={}, common_attributes={})

    def add(self, flat_data_row: FlatDictRow) -> tp.Self:
        """Add a new article or variation to the catalog from a flat data row.

        Args:
            flat_data_row (FlatDictRow): A dictionary representing a flat data row.

        Raises:
            RequiredFieldMissingError: If the required 'article_number'
                field is missing from the data row.

        Returns:
            Catalog: The updated instance of the Catalog class.
        """
        if not self.articles:
            self.articles: dict[str, Article] = {}

        grouper_row_name = "article_number"

        article_number = flat_data_row.get(grouper_row_name)
        if not article_number:
            raise RequiredFieldMissingError(
                f"Required field missing: '{grouper_row_name}'"
            )

        variations_without_grouper = flat_data_row.copy()
        variations_without_grouper.pop(grouper_row_name, None)

        if existing_article := self.articles.get(article_number):
            existing_article.variations.append(variations_without_grouper)
        else:
            self.articles[article_number] = Article(
                article_number=article_number,
                variations=[variations_without_grouper],
                common_attributes={},
            )

        return self


def consolidate_common_attributes(catalog: Catalog) -> Catalog:
    """Consolidate common attributes at both the article and catalog levels.

    Args:
        catalog (Catalog): The catalog to consolidate.

    Returns:
        Catalog: The updated catalog with common attributes consolidated.
    """
    for article in catalog.articles.values():
        _level_up_common_attributes_to_article_level(article=article)

    _level_up_common_attributes_to_catalog_level(catalog=catalog)

    return catalog


def _level_up_common_attributes_to_article_level(article: Article) -> None:
    """Level up common attributes from variations to the article level.

    Args:
        article (Article): The article to update.
    """
    common = collect_common_attributes(dicts=article.variations)
    article.common_attributes = common

    for variation in article.variations:
        remove_attributes_inplace(target_dict=variation, dict_to_remove=common)


def _level_up_common_attributes_to_catalog_level(catalog: Catalog) -> None:
    """Level up common attributes from articles to the catalog level.

    Args:
        catalog (Catalog): The catalog to update.
    """
    # Collect common attributes across all articles
    common_attributes_from_articles: list[dict] = []
    for article in catalog.articles.values():
        common_attributes_from_articles.append(article.common_attributes)

    common_attributes = collect_common_attributes(common_attributes_from_articles)

    # Remove common attributes from all articles
    for article in catalog.articles.values():
        remove_attributes_inplace(
            target_dict=article.common_attributes, dict_to_remove=common_attributes
        )

    # Set common attributes at the catalog level
    catalog.common_attributes = common_attributes
