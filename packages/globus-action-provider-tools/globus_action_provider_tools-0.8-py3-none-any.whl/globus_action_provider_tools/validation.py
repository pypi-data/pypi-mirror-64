from pathlib import Path

import yaml
from openapi_core.schema.specs.models import Spec
from openapi_core.shortcuts import RequestValidator, ResponseValidator, create_spec

HERE: Path = Path(__file__).parent
SPECFILE: str = "actions_spec.openapi.yaml"

with open(HERE / SPECFILE, "r") as specfile:
    spec: Spec = create_spec(yaml.safe_load(specfile))

request_validator: RequestValidator = RequestValidator(spec)
response_validator: ResponseValidator = ResponseValidator(spec)
