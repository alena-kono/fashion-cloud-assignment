import abc
import dataclasses
import typing as tp

from src.extractor.reader import Row
from src.transformer.exceptions import (
    MappingError,
    RowDoesNotContainFieldError,
)

# TODO: Validate Row schema or CSV schema


@dataclasses.dataclass(frozen=True)
class MapAttr:
    val: str
    type_: str


@dataclasses.dataclass(frozen=True)
class MappingUnit:
    source: MapAttr
    destination: MapAttr

    @classmethod
    def from_row(cls, row: Row) -> tp.Self:
        return cls(
            source=MapAttr(
                val=row["source"],
                type_=row["source_type"],
            ),
            destination=MapAttr(
                val=row["destination"],
                type_=row["destination_type"],
            ),
        )


# TODO: move building mapping to extractor?
class Mapping:
    """Hash-based class that uses combined key."""

    def __init__(self) -> None:
        self.direct_items: dict[str, MappingUnit] = {}
        self.composite_items: dict[str, MappingUnit] = {}
        self.glob_items: dict[str, MappingUnit] = {}

    def build(self, mapping_rows: tp.Iterable[Row]) -> None:
        if not mapping_rows:
            # TODO: Raise custom error
            raise ValueError("mappings should not be empty or None")

        for row in mapping_rows:
            m = MappingUnit.from_row(row)
            composite_key = self._generate_key(m.source.val, m.source.type_)

            if m.source.val == "*" and m.destination.val == "*":
                self.glob_items[composite_key] = m
            elif "|" in m.source.val:
                self.composite_items[composite_key] = m
            else:
                # TODO: Raise error if source type and source val already exist ?
                self.direct_items[composite_key] = m

    def get(self, source_val: str, source_type: str) -> MappingUnit | None:
        combined_key = self._generate_key(
            source_val=source_val, source_type=source_type
        )
        return self.direct_items.get(combined_key, None)

    @staticmethod
    def _generate_key(source_val: str, source_type: str) -> str:
        return f"{source_val}.{source_type}"


class IDictTransformer(abc.ABC):
    @abc.abstractmethod
    def transform(self, d: dict, src_val: str, src_type: str) -> dict:
        pass


class BaseDictTransformer(IDictTransformer):
    def __init__(self, mapping: Mapping) -> None:
        super().__init__()
        self.mapping = mapping


class DirectTransformer(BaseDictTransformer):
    def transform(self, d: dict, src_val: str, src_type: str) -> dict:
        if mapped := self.mapping.get(source_val=src_val, source_type=src_type):
            d[mapped.destination.type_] = mapped.destination.val
        return d


class UniqueCompositeTransformer(BaseDictTransformer):
    def transform(self, d: dict, src_val: str, src_type: str) -> dict:
        for mapped in self.mapping.composite_items.values():
            src_vals = mapped.source.val.split("|")
            src_types = mapped.source.type_.split("|")

            if len(src_types) != len(src_vals):
                raise MappingError(
                    "Mapping is incorrectly configured. Check mappings file"
                )

            if all([d.get(type_) == val for type_, val in zip(src_types, src_vals)]):
                d[mapped.destination.type_] = mapped.destination.val

        return d


class GlobCompositeTransformer(BaseDictTransformer):
    def transform(self, d: dict, src_val: str, src_type: str) -> dict:
        for mapped in self.mapping.glob_items.values():
            src_cols = mapped.source.type_.split("|")
            dst_col = mapped.destination.type_

            composite_key_parts = []
            for col in src_cols:
                if val := d.get(col):
                    composite_key_parts.append(val)
                else:
                    return d

            d[dst_col] = " ".join(_ for _ in composite_key_parts)

        return d


class DictContext:
    def __init__(self, strategy: IDictTransformer) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: IDictTransformer) -> None:
        self._strategy = strategy

    def apply_transform(self, d: dict[str, str], src_val: str, src_type: str) -> dict:
        return self._strategy.transform(d=d, src_val=src_val, src_type=src_type)


def transform_row(source_row: Row, mapping: Mapping) -> Row:
    updated_row = source_row.copy()

    strategies: tuple[IDictTransformer, ...] = (
        DirectTransformer(mapping=mapping),
        UniqueCompositeTransformer(mapping=mapping),
        GlobCompositeTransformer(mapping=mapping),
    )

    # Set direct strategy by default
    context = DictContext(strategies[0])

    for src_type, src_val in source_row.items():
        for strategy in strategies:
            context.set_strategy(strategy)
            try:
                updated_row = context.apply_transform(
                    d=updated_row, src_val=src_val, src_type=src_type
                )
            except KeyError as err:
                raise RowDoesNotContainFieldError(
                    message=f"Row does not contain field: {err.args[0]}"
                )

    return updated_row
