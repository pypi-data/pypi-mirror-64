# -*- coding: utf-8 -*-
"""
Schema validation utility
"""

import re
from inspect import Parameter, signature
from typing import TYPE_CHECKING, Any, Callable, List, Sequence, Set, Union

from .._string_utils import quoted_options_list
from ..exc import SchemaError, SchemaValidationError
from .introspection import is_introspection_type
from .scalars import SPECIFIED_SCALAR_TYPES
from .types import (
    Argument,
    Directive,
    EnumType,
    EnumValue,
    InputObjectType,
    InterfaceType,
    NonNullType,
    ObjectType,
    UnionType,
    is_input_type,
    is_output_type,
)


if TYPE_CHECKING:  # Fix import cycles of types needed for Mypy checking
    from .schema import Schema

VALID_NAME_RE = re.compile(r"^(?!__)[_a-zA-Z][_a-zA-Z0-9]*$")
RESERVED_NAMES = set(t.name for t in SPECIFIED_SCALAR_TYPES)

VAR_PARAM_KINDS = (Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD)
POSITIONAL_PARAM_KINDS = (
    Parameter.POSITIONAL_ONLY,
    Parameter.POSITIONAL_OR_KEYWORD,
)


def validate_schema(
    schema: "Schema", enable_resolver_validation: bool = True,
) -> bool:
    """
    Validate a GraphQL schema.

    Useful for handling untrusted schemas or during development, but ideally
    you do not need to run this in production when fully controlling the
    schema's origin.

    This assumes the schema was created through `Schema()` and the type map
    has been built.

    Note:
        This is incomplete and could miss some errors. Looking at the
        implementation and searching for ``TODO`` comments should give a good
        idea of what's missing.

    Args:
        schema: Schema to validate.

    Raises:
        SchemaValidationError: if the schema is invalid.

    Returns:
        ``True`` if the schema is valid, else ``False``.

    """
    validator = SchemaValidator(
        schema, enable_resolver_validation=enable_resolver_validation,
    )

    validator()

    if not validator:
        raise SchemaValidationError(validator.errors)

    return True


def _is_valid_name(name: str) -> bool:
    """
    Check if a string is a valid name for GraphQL schema elements.

    >>> _is_valid_name('foo_bar')
    True

    >>> _is_valid_name('fooBar')
    True

    >>> _is_valid_name('FooBar')
    True

    >>> _is_valid_name('_foo_bar')
    True

    >>> _is_valid_name('foo-bar')
    False

    >>> _is_valid_name('__foo_bar')
    False

    >>> _is_valid_name('')
    False

    >>> _is_valid_name('42')
    False
    """
    return bool(VALID_NAME_RE.match(name))


# TODO: Most non-lazy attributes could be checked earlier.
# TODO: Can this be made into a SchemaVisitor?
class SchemaValidator:
    def __init__(
        self, schema: "Schema", enable_resolver_validation: bool = True
    ):
        self.schema = schema
        self.errors = []  # type: List[SchemaError]
        self.enable_resolver_validation = enable_resolver_validation

    def __bool__(self) -> bool:
        return not self.errors

    def add_error(self, msg: str) -> None:
        self.errors.append(SchemaError(msg))

    def check_valid_name(self, name: str) -> None:
        if not _is_valid_name(name):
            self.add_error('Invalid name "%s".' % name)

    def __call__(self) -> None:
        self.validate_root_types()

        for type_ in self.schema.types.values():
            if not (
                is_introspection_type(type_)
                or type_ in SPECIFIED_SCALAR_TYPES
                or _is_valid_name(type_.name)
            ):
                self.add_error('Invalid type name "%s"' % type_.name)
                continue

            if isinstance(type_, ObjectType):
                self.validate_fields(type_)
                self.validate_interfaces(type_)
            elif isinstance(type_, InterfaceType):
                self.validate_fields(type_)
            elif isinstance(type_, UnionType):
                self.validate_union_members(type_)
            elif isinstance(type_, EnumType):
                self.validate_enum_values(type_)
            elif isinstance(type_, InputObjectType):
                self.validate_input_fields(type_)

        self.validate_directives()

    def validate_root_types(self) -> None:
        if self.schema.query_type is None:
            self.add_error("Must provide Query type")

        if self.schema.query_type is not None and not isinstance(
            self.schema.query_type, ObjectType
        ):
            self.add_error(
                'Query must be ObjectType but got "%s"' % self.schema.query_type
            )

        if self.schema.mutation_type is not None and not isinstance(
            self.schema.mutation_type, ObjectType
        ):
            self.add_error(
                'Mutation must be ObjectType but got "%s"'
                % self.schema.mutation_type
            )

        if self.schema.subscription_type is not None and not isinstance(
            self.schema.subscription_type, ObjectType
        ):
            self.add_error(
                'Subscription must be ObjectType but got "%s"'
                % self.schema.subscription_type
            )

    def validate_directives(self) -> None:
        for directive in self.schema.directives.values():
            if not isinstance(directive, Directive):
                self.add_error("Expected Directive but got %r" % directive)
                continue

            self.check_valid_name(directive.name)

            # TODO: Ensure proper locations.
            argnames = set()  # type: Set[str]
            for arg in directive.arguments:

                self.check_valid_name(arg.name)

                if arg.name in argnames:
                    self.add_error(
                        'Duplicate argument "%s" on directive "@%s"'
                        % (arg.name, directive.name)
                    )
                    continue

                if not is_input_type(arg.type):
                    self.add_error(
                        'Expected input type for argument "%s" on directive "@%s" but '
                        'got "%s"' % (arg.name, directive.name, arg.type)
                    )

                argnames.add(arg.name)

    def validate_fields(
        self, composite_type: Union[ObjectType, InterfaceType]
    ) -> None:
        # TODO: Ensure resolvers arguments match field arguments.
        if not composite_type.fields:
            self.add_error(
                'Type "%s" must define at least one field' % composite_type
            )

        fieldnames = set()  # type: Set[str]
        for field in composite_type.fields:

            self.check_valid_name(field.name)

            if field.name in fieldnames:
                self.add_error(
                    'Duplicate field "%s" on "%s"'
                    % (field.name, composite_type)
                )
                continue

            if not is_output_type(field.type):
                self.add_error(
                    'Expected output type for field "%s" on "%s" but got "%s"'
                    % (field.name, composite_type, field.type)
                )

            argnames = set()  # type: Set[str]
            path = "%s.%s" % (composite_type, field.name)

            for arg in field.arguments:

                self.check_valid_name(arg.name)

                if arg.name in argnames:
                    self.add_error(
                        'Duplicate argument "%s" on "%s"' % (arg.name, path)
                    )
                    continue

                if not is_input_type(arg.type):
                    self.add_error(
                        'Expected input type for argument "%s" on "%s" but got "%s"'
                        % (arg.name, path, arg.type)
                    )

                argnames.add(arg.name)

            # Check that the resolver won't break when being called by the
            # execution layer.

            # Default resolvers must be compatible with any field they could be
            # used for, which usually this means defining a variable keyword
            # parameter.

            resolver = (
                field.resolver
                or (
                    composite_type.default_resolver
                    if isinstance(composite_type, ObjectType)
                    else None
                )
                or self.schema.default_resolver
            )

            if resolver and self.enable_resolver_validation:
                self._validate_resolver_arguments(
                    path, field.arguments, resolver,
                )

            fieldnames.add(field.name)

    def _validate_resolver_arguments(
        self, path: str, args: Sequence[Argument], resolver: Callable[..., Any],
    ) -> None:
        try:
            sig = signature(resolver)
        except ValueError:
            # In some cases (mostly C Extensions) this can fail, in this case
            # we fallback to the previous behaviour of not validating and
            # assuming correctness.
            # This also seems to affect lambda functions when using Cython
            # (https://github.com/cython/cython/issues/2983)
            return

        params = list(sig.parameters.values())

        accepts_arbitrary_params = any(
            p for p in params if p.kind is Parameter.VAR_POSITIONAL
        )

        accepts_arbitrary_kw_params = any(
            p for p in params if p.kind is Parameter.VAR_KEYWORD
        )

        known_param_names = [arg.python_name for arg in args]

        for arg in args:
            try:
                param = sig.parameters[arg.python_name]
            except KeyError:
                if not accepts_arbitrary_kw_params:
                    self.add_error(
                        'Missing resolver parameter for argument "%s" on "%s"'
                        % (arg.name, path,)
                    )
            else:
                if param.kind is Parameter.POSITIONAL_ONLY:
                    # In practice this is a 3.8+ only concern.
                    self.add_error(
                        'Resolver parameter for argument "%s" on "%s" '
                        "must not be positional only" % (arg.name, path,)
                    )
                elif (
                    param.default is Parameter.empty
                    and (not arg.has_default_value)
                    and (not arg.required)
                ):
                    # Required arguments must provide values at query time and
                    # arguments with default values will fallback, so they'll
                    # both always be provided to the resolver.
                    self.add_error(
                        'Resolver parameter for optional argument "%s" on '
                        '"%s" must have a default' % (arg.name, path,)
                    )

        remaining = [
            p
            for p in params
            if p.name not in known_param_names and p.kind not in VAR_PARAM_KINDS
        ]

        remaining_positional = [
            p for p in remaining if p.kind in POSITIONAL_PARAM_KINDS
        ]

        if not accepts_arbitrary_params and len(remaining_positional) < 3:
            self.add_error(
                'Resolver for "%s" must accept 3 positional parameters, found (%s)'
                % (
                    path,
                    quoted_options_list(
                        [p.name for p in remaining_positional], "and",
                    ),
                )
            )

        for param in remaining[3:]:
            if param.default is Parameter.empty:
                self.add_error(
                    'Required resolver parameter "%s" on "%s" does not match '
                    "any known argument or expected positional parameter"
                    % (param.name, path)
                )

    def validate_interfaces(self, type_: ObjectType) -> None:
        imlemented_types = set()  # type: Set[str]
        for interface in type_.interfaces:
            # TODO: This could be automatically fixed.
            if interface.name in imlemented_types:
                self.add_error(
                    'Type "%s" mut only implement interface "%s" once'
                    % (type_, interface.name)
                )
                continue

            imlemented_types.add(interface.name)
            self.validate_implementation(type_, interface)

    def validate_implementation(
        self, type_: ObjectType, interface: InterfaceType
    ) -> None:
        for field in interface.fields:
            object_field = type_.field_map.get(field.name, None)
            interface_path = "%s.%s" % (interface.name, field.name)
            obj_path = "%s.%s" % (type_, field.name)

            if object_field is None:
                self.add_error(
                    'Interface field "%s" is not implemented by type "%s"'
                    % (interface_path, type_)
                )
                continue

            if not self.schema.is_subtype(object_field.type, field.type):
                self.add_error(
                    'Interface field "%s" expects type "%s" but "%s" is type "%s"'
                    % (interface_path, field.type, obj_path, object_field.type)
                )
                continue

            for arg in field.arguments:
                object_arg = object_field.argument_map.get(arg.name, None)

                if object_arg is None:
                    self.add_error(
                        'Interface field argument "%s.%s" is not provided by "%s"'
                        % (interface_path, arg.name, obj_path)
                    )
                    continue

                # TODO: Should this use is_subtype ?
                if arg.type != object_arg.type:
                    self.add_error(
                        'Interface field argument "%s.%s" expects type "%s" but '
                        '"%s.%s" is type "%s"'
                        % (
                            interface_path,
                            arg.name,
                            arg.type,
                            obj_path,
                            arg.name,
                            object_arg.type,
                        )
                    )

                # TODO: Validate default values

            for arg in object_field.arguments:
                interface_arg = field.argument_map.get(arg.name, None)
                if interface_arg is None:
                    if isinstance(arg.type, NonNullType):
                        self.add_error(
                            'Object field argument "%s.%s" is of required type '
                            '"%s" but is not provided by interface field "%s"'
                            % (obj_path, arg.name, arg.type, interface_path)
                        )

    def validate_union_members(self, union_type: UnionType) -> None:
        if not union_type.types:
            self.add_error(
                'UnionType "%s" must at least define one member' % union_type
            )

        member_type_names = set()  # type: Set[str]
        for member_type in union_type.types:
            if not isinstance(member_type, ObjectType):
                self.add_error(
                    'UnionType "%s" expects object types but got "%s"'
                    % (union_type, member_type)
                )
                continue

            # TODO: This could be automatically fixed.
            if member_type.name in member_type_names:
                self.add_error(
                    'UnionType "%s" can only include type "%s" once'
                    % (union_type, member_type)
                )

            member_type_names.add(member_type.name)

    def validate_enum_values(self, enum_type: EnumType) -> None:
        if not enum_type.values:
            self.add_error(
                'EnumType "%s" must at least define one value' % enum_type
            )

        for enum_value in enum_type.values:
            if not isinstance(enum_value, EnumValue):
                self.add_error(
                    'Enum "%s" expects value to be EnumValue but got "%s"'
                    % (enum_type, enum_value)
                )

            self.check_valid_name(enum_value.name)

    def validate_input_fields(self, input_object: InputObjectType) -> None:
        if not input_object.fields:
            self.add_error(
                'Type "%s" must define at least one field' % input_object
            )

        fieldnames = set()  # type: Set[str]

        for field in input_object.fields:
            if field.name in fieldnames:
                self.add_error(
                    'Duplicate field "%s" on "%s"' % (field.name, input_object)
                )
                continue

            if not is_input_type(field.type):
                self.add_error(
                    'Expected input type for field "%s" on "%s" but got "%s"'
                    % (field.name, input_object, field.type)
                )

            fieldnames.add(field.name)
