import dataclasses
import json
import typing as tp


class DataClassJsonEncoder(json.JSONEncoder):
    def default(self, o: tp.Any) -> dict:
        if hasattr(o, "__dataclass_fields__"):
            return dataclasses.asdict(o)
        return super().default(o)
