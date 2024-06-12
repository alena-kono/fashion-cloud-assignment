import pytest

from src.transformer.transformer import Mapping


@pytest.fixture()
def mock_mapping() -> Mapping:
    mapping = Mapping()
    mapping.build(
        [
            {
                "source": "color",
                "source_type": "attribute",
                "destination": "colour",
                "destination_type": "attribute",
            },
            {
                "source": "size",
                "source_type": "attribute",
                "destination": "size",
                "destination_type": "dimension",
            },
            {
                "source": "*",
                "source_type": "*",
                "destination": "combined",
                "destination_type": "composite",
            },
            {
                "source": "color|size",
                "source_type": "attribute|attribute",
                "destination": "color_size",
                "destination_type": "composite",
            },
        ]
    )
    return mapping
