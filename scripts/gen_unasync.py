# type: ignore
from pathlib import Path

import unasync

DIRECTORIES = ["src/dj_blacksmith/client/_async"]

for path in DIRECTORIES:
    unasync.unasync_files(
        [str(p) for p in Path(path).iterdir() if p.is_file()],
        rules=[
            unasync.Rule(
                path,
                path.replace("_async", "_sync"),
                additional_replacements={
                    "_async": "_sync",
                },
            ),
        ],
    )


unasync.unasync_files(
    [str(p) for p in Path("tests/unittests/_async").iterdir() if p.is_file()],
    rules=[
        unasync.Rule(
            "tests/unittests/_async",
            "tests/unittests/_sync",
            additional_replacements={
                "_async": "_sync",
                "tests.unittests.fixtures.AsyncDummyTransport": "tests.unittests.fixtures.SyncDummyTransport",
                "dj_blacksmith.AsyncCircuitBreakerMiddlewareBuilder": "dj_blacksmith.SyncCircuitBreakerMiddlewareBuilder",
                "dj_blacksmith.AsyncPrometheusMiddlewareBuilder": "dj_blacksmith.SyncPrometheusMiddlewareBuilder",
                "dummy_async_client_factory": "dummy_sync_client_factory",
            },
        ),
    ],
)
