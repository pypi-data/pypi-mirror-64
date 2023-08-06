# -*- coding: utf-8 -*-

import pytest

from py_gql.exc import ResolverError
from py_gql.schema import Field, NonNullType, ObjectType, Schema, String


class _obj:
    def __init__(self, **attrs):
        for k, v in attrs.items():
            setattr(self, k, v)


# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio

NullNonNullDataType = ObjectType(
    "DataType",
    [
        Field("scalar", String),
        Field("scalarNonNull", NonNullType(String)),
        Field("nested", lambda: NullNonNullDataType),
        Field("nestedNonNull", lambda: NonNullType(NullNonNullDataType)),
    ],
)  # type: ObjectType

NullAndNonNullSchema = Schema(NullNonNullDataType)


async def test_nulls_nullable_field(assert_execution):
    await assert_execution(
        NullAndNonNullSchema,
        "query Q { scalar }",
        initial_value=dict(scalar=None),
        expected_data={"scalar": None},
    )


async def test_nulls_lazy_nullable_field(assert_execution):
    await assert_execution(
        NullAndNonNullSchema,
        "query Q { scalar }",
        initial_value=_obj(scalar=lambda *_: None),
        expected_data={"scalar": None},
    )


async def test_nulls_and_report_error_on_non_nullable_field(assert_execution):
    await assert_execution(
        NullAndNonNullSchema,
        "query Q { scalarNonNull }",
        initial_value=dict(scalarNonNull=None),
        expected_data={"scalarNonNull": None},
        expected_errors=[
            ('Field "scalarNonNull" is not nullable', (10, 23), "scalarNonNull")
        ],
    )


async def test_nulls_and_report_error_on_lazy_non_nullable_field(
    assert_execution,
):
    await assert_execution(
        NullAndNonNullSchema,
        "query Q { scalarNonNull }",
        initial_value=_obj(scalarNonNull=lambda *_: None),
        expected_data={"scalarNonNull": None},
        expected_errors=[
            ('Field "scalarNonNull" is not nullable', (10, 23), "scalarNonNull")
        ],
    )


async def test_nulls_tree_of_nullable_fields(assert_execution):
    await assert_execution(
        NullAndNonNullSchema,
        """
        query Q {
            nested {
                scalar
                nested {
                    scalar
                    nested {
                        scalar
                    }
                }
            }
        }
        """,
        initial_value={
            "nested": {
                "scalar": None,
                "nested": {"scalar": None, "nested": None},
            }
        },
        expected_data={
            "nested": {
                "nested": {"nested": None, "scalar": None},
                "scalar": None,
            }
        },
        expected_errors=[],
    )


# Depending on scheduling the errors can be in a different order
async def test_nulls_and_report_errors_on_tree_of_non_nullable_fields(
    assert_execution,
):

    await assert_execution(
        NullAndNonNullSchema,
        """
        query Q {
            nested {
                scalarNonNull
                nestedNonNull {
                    scalar
                    nestedNonNull {
                        scalarNonNull
                    }
                }
            }
            nestedNonNull {
                scalarNonNull
            }
        }
        """,
        initial_value={
            "nestedNonNull": None,
            "nested": {"scalarNonNull": None, "nestedNonNull": None},
        },
        expected_data={
            "nested": {"nestedNonNull": None, "scalarNonNull": None},
            "nestedNonNull": None,
        },
        expected_errors=[
            (
                'Field "nested.scalarNonNull" is not nullable',
                (31, 44),
                "nested.scalarNonNull",
            ),
            (
                'Field "nested.nestedNonNull" is not nullable',
                (53, 169),
                "nested.nestedNonNull",
            ),
            (
                'Field "nestedNonNull" is not nullable',
                (180, 223),
                "nestedNonNull",
            ),
        ],
    )


async def test_nulls_out_errored_subtrees(raiser, assert_execution):
    root = _obj(
        sync="sync",
        callable_error=raiser(ResolverError, "callable_error"),
        callable=lambda *_: "callable",
    )

    schema = Schema(
        ObjectType(
            "Query",
            [
                Field("sync", String),
                Field("callable_error", String),
                Field("callable", String),
                Field(
                    "resolver_error",
                    String,
                    resolver=raiser(ResolverError, "resolver_error"),
                ),
                Field("resolver", String, resolver=lambda *_: "resolver"),
            ],
        )
    )

    await assert_execution(
        schema,
        """
        {
            sync,
            callable_error,
            callable,
            resolver_error,
            resolver,
        }
        """,
        initial_value=root,
        expected_data={
            "sync": "sync",
            "callable_error": None,
            "callable": "callable",
            "resolver_error": None,
            "resolver": "resolver",
        },
        expected_errors=[
            ("callable_error", (16, 30), "callable_error"),
            ("resolver_error", (50, 64), "resolver_error"),
        ],
    )
