from typing import Any

import pytest
from blacksmith import AsyncCircuitBreakerMiddleware
from blacksmith.domain.registry import ApiRoutes, registry

from dj_blacksmith.client._async.client import AsyncClientProxy, AsyncDjBlacksmithClient


def test_import():
    # test that the app testapp has loaded its resource while ready

    clients: dict[str, Any] = dict(registry.clients)  # type: ignore
    assert list(clients.keys()) == ["dummy"]
    assert list(clients["dummy"].keys()) == ["dummies"]
    dummies: ApiRoutes = clients["dummy"]["dummies"]
    assert dummies.resource is not None
    assert dummies.resource.path == "/dummies"


@pytest.mark.parametrize(
    "params",
    [
        {
            "client": "default",
            "middlewares": [],
        },
        {
            "client": "alt_client",
            "middlewares": [AsyncCircuitBreakerMiddleware],
        },
    ],
)
async def test_async_dj_blacksmith(
    params: dict[str, Any], req: Any, prometheus_registry: Any
):
    bmcli = AsyncDjBlacksmithClient(req.get("/"))
    cli = await bmcli(params["client"])
    assert isinstance(cli, AsyncClientProxy)
    assert [type(mid) for mid in cli.client_factory.middlewares] == params[
        "middlewares"
    ]
