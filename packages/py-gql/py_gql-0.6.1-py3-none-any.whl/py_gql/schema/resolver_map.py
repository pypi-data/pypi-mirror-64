# -*- coding: utf-8 -*-

from typing import Any, Callable, Dict, Optional, TypeVar


Resolver = Callable[..., Any]
TResolver = TypeVar("TResolver", bound=Resolver)


class ResolverMap:
    """
    Colection of resolver that can be used to define resolvers outside of a schema.

    Multiple resolver maps can be merged using :meth:`merge_resolvers`.

    >>> schema = ResolverMap()
    >>> @schema.resolver("Query.foo")
    ... def resolve_foo(obj, ctx, info):
    ...     return "foo"
    """

    def __init__(self):
        self.resolvers = {}  # type: Dict[str, Dict[str, Resolver]]
        self.subscriptions = {}  # type: Dict[str, Dict[str, Resolver]]
        self.default_resolver = None  # type: Optional[Resolver]
        self.default_resolvers = {}  # type: Dict[str, Resolver]

    def get_resolver(self, typename: str, fieldname: str) -> Optional[Resolver]:
        """
        Extract resolver for a given field and fall back to defaults if possible.
        """
        try:
            return self.resolvers[typename][fieldname]
        except KeyError:
            return self.default_resolvers.get(typename) or self.default_resolver

    def get_subscription(
        self, typename: str, fieldname: str
    ) -> Optional[Resolver]:
        """
        Extract subscription resolver for a given field.
        """
        try:
            return self.subscriptions[typename][fieldname]
        except KeyError:
            return None

    def register_default_resolver(
        self, typename: str, resolver: Resolver, *, allow_override: bool = False
    ) -> None:
        """
        Register a callable as a default resolver for a given type.

        Args:
            typename: Type name
            resolver: Resolver callable
            allow_override: Set this to ``True`` to allow re-definition.

        Raises:
            ValueError: If the resolver has already been defined and
                ``allow_override`` was ``False``.
        """
        if typename in self.default_resolvers and not allow_override:
            raise ValueError(
                'Type "%s" already has a default resolver.' % (typename,)
            )

        self.default_resolvers[typename] = resolver

    def register_resolver(
        self,
        typename: str,
        fieldname: str,
        resolver: Resolver,
        *,
        allow_override: bool = False
    ) -> None:
        """
        Register a function as a resolver.

        Args:
            typename: Type name
            fieldname: Field name
            resolver: Resolver callable
            allow_override: Set this to ``True`` to allow re-definition.

        Raises:
            ValueError: If the resolver has already been defined and
                ``allow_override`` was ``False``.
        """
        parent = self.resolvers[typename] = self.resolvers.get(typename, {})

        if fieldname == "*":
            self.register_default_resolver(typename, resolver)
        else:
            if fieldname in parent and not allow_override:
                raise ValueError(
                    'Field "%s" of type "%s" already has a resolver.'
                    % (fieldname, typename)
                )

            parent[fieldname] = resolver

    def resolver(
        self, field: str, *, allow_override: bool = False
    ) -> Callable[[TResolver], TResolver]:
        """
        Decorate a function to register it as a resolver.

        Args:
            field: Field path in the form ``{Typename}.{Fieldname}``.
            allow_override: Set this to ``True`` to allow re-definition.

        Raises:
            ValueError: If the ``field`` value cannot be parsed.

        Returns:
            Decorator.
        """
        try:
            typename, fieldname = field.split(".")[:2]
        except (ValueError, IndexError):
            raise ValueError(
                'Invalid field path "%s". Field path must of the form '
                '"{Typename}.{Fieldname}"' % field
            )

        def decorator(func: TResolver) -> TResolver:
            self.register_resolver(
                typename, fieldname, func, allow_override=allow_override
            )
            return func

        return decorator

    def register_subscription(
        self,
        typename: str,
        fieldname: str,
        resolver: Resolver,
        *,
        allow_override: bool = False
    ) -> None:
        """
        Register a function as a subscription resolver.

        Args:
            typename: Type name
            fieldname: Field name
            resolver: Resolver callable
            allow_override: Set this to ``True`` to allow re-definition.

        Raises:
            ValueError: If the resolver has already been defined and
                ``allow_override`` was ``False``.
        """
        parent = self.subscriptions[typename] = self.subscriptions.get(
            typename, {}
        )

        if fieldname in parent and not allow_override:
            raise ValueError(
                'Field "%s" of type "%s" already has a subscription.'
                % (fieldname, typename)
            )

        parent[fieldname] = resolver

    def subscription(
        self, field: str, *, allow_override: bool = False
    ) -> Callable[[TResolver], TResolver]:
        """
        Decorate a function to register it as a subscription resolver.

        Args:
            field: Field path in the form ``{Typename}.{Fieldname}``.
            allow_override: Set this to ``True`` to allow re-definition.

        Raises:
            ValueError: If the ``field`` value cannot be parsed.

        Returns:
            Decorator.
        """
        try:
            typename, fieldname = field.split(".")[:2]
        except (ValueError, IndexError):
            raise ValueError(
                'Invalid field path "%s". Field path must of the form '
                '"{Typename}.{Fieldname}"' % field
            )

        def decorator(func: TResolver) -> TResolver:
            self.register_subscription(
                typename, fieldname, func, allow_override=allow_override
            )
            return func

        return decorator

    def merge_resolvers(
        self, other: "ResolverMap", *, allow_override: bool = False
    ) -> None:
        """
        Combine 2 collections by merging the target into the current instance.
        """
        for typename, field_resolvers in other.resolvers.items():
            for fieldname, resolver in field_resolvers.items():
                self.register_resolver(
                    typename, fieldname, resolver, allow_override=allow_override
                )

        for typename, field_subscriptions in other.subscriptions.items():
            for fieldname, subscription in field_subscriptions.items():
                self.register_subscription(
                    typename,
                    fieldname,
                    subscription,
                    allow_override=allow_override,
                )
