import pytest

from src.grouper.utils import (
    collect_common_attributes,
    remove_attributes_inplace,
)


@pytest.mark.parametrize(
    ("dicts", "expected"),
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
            {
                "article_number": "a",
            },
        ),
        (
            [
                {
                    "article_number": "xyz",
                    "name": "fancy dream",
                    "colour": "black",
                    "price": "125",
                },
                {
                    "article_number": "a",
                    "name": "t-shirt",
                    "colour": "red",
                    "price": "2",
                },
            ],
            {},
        ),
        (
            [
                {
                    "article_number": "a",
                    "name": "same",
                    "colour": "black",
                    "price": "125",
                },
                {
                    "article_number": "a",
                    "name": "same",
                    "colour": "black",
                    "price": "125",
                },
            ],
            {
                "article_number": "a",
                "name": "same",
                "colour": "black",
                "price": "125",
            },
        ),
        (
            [
                {
                    "article_number": "a",
                    "name": "same",
                },
                {
                    "article_number": "a",
                    "new_name": "same",
                },
            ],
            {
                "article_number": "a",
            },
        ),
        (
            [
                {
                    "article_number": "a",
                    "name": "same",
                },
                {},
            ],
            {},
        ),
        ([{}, {}], {}),
    ],
    ids=[
        "one_common",
        "no_common_diff_values",
        "all_common",
        "no_common_diff_key_name",
        "one_empty_input_dict",
        "two_empty_input_dicts",
    ],
)
def test_collect_common_attributes(dicts: list[dict], expected: dict) -> None:
    assert collect_common_attributes(dicts=dicts) == expected


@pytest.mark.parametrize(
    ("target_dict", "dict_to_remove", "expected"),
    [
        # some attributes are removed
        (
            {
                "article_number": "a",
                "name": "same",
                "colour": "black",
                "price": "125",
            },
            {
                "name": "same",
                "price": "125",
            },
            {
                "article_number": "a",
                "colour": "black",
            },
        ),
        # no attributes to remove
        (
            {
                "article_number": "a",
                "name": "same",
                "colour": "black",
                "price": "125",
            },
            {},
            {
                "article_number": "a",
                "name": "same",
                "colour": "black",
                "price": "125",
            },
        ),
        # all attributes are removed
        (
            {
                "article_number": "a",
                "name": "same",
                "colour": "black",
                "price": "125",
            },
            {
                "article_number": "a",
                "name": "same",
                "colour": "black",
                "price": "125",
            },
            {},
        ),
        # some attributes do not exist
        (
            {
                "article_number": "a",
                "name": "same",
                "colour": "black",
                "price": "125",
            },
            {"name": "same", "price": "125", "non_existent": "value"},
            {
                "article_number": "a",
                "colour": "black",
            },
        ),
        # empty target_dict
        (
            {},
            {
                "name": "same",
                "price": "125",
            },
            {},
        ),
    ],
    ids=[
        "some_attributes_are_removed",
        "no_attributes_to_remove",
        "all_attributes_are_removed",
        "some_attributes_do_not_exist",
        "empty_target_dict",
    ],
)
def test_remove_attributes_inplace(
    target_dict: dict, dict_to_remove: dict, expected: dict
) -> None:
    remove_attributes_inplace(target_dict, dict_to_remove)
    assert target_dict == expected
