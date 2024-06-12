import json
import typing as tp


def encode_to_json(obj: tp.Any, encoder_cls: type[json.JSONEncoder]) -> str:
    return json.dumps(
        obj=obj,
        cls=encoder_cls,
        indent=2,
        ensure_ascii=False,
        sort_keys=False,
    )
