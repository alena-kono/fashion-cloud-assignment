def collect_common_attributes(dicts: list[dict]) -> dict:
    if not dicts:
        return {}

    common_items = set(dicts[0].items())

    for d in dicts[1:]:
        common_items = common_items & d.items()

    return dict(common_items)


def remove_attributes_inplace(target_dict: dict, dict_to_remove: dict) -> None:
    for key in dict_to_remove:
        target_dict.pop(key, None)
