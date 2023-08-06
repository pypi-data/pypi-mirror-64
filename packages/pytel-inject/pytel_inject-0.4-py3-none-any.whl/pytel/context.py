import contextlib
import inspect
import logging
import typing

log = logging.getLogger(__name__)

T = typing.TypeVar('T')
FactoryType = typing.Union[T, typing.Callable[..., T]]


class ObjectDescriptor(typing.Generic[T]):
    def __init__(self, factory: typing.Optional[FactoryType],
                 name: str,
                 _type: typing.Type[T],
                 deps: typing.Dict[str, typing.Type]
                 ):
        self._factory = factory
        self._name = name
        self._type = _type
        self._deps = deps
        self._resolved_deps = None
        self._instance: typing.Optional[T] = None
        self._exit_stack: typing.Optional[contextlib.ExitStack] = None

    def _resolve(self) -> T:
        assert self._instance is None, 'Called factory on resolved object'

        deps = {name: descr.instance for name, descr in self._resolved_deps.items()}
        instance = self._factory(**deps)
        if instance is None:
            raise ValueError(self._name, f"Factory for '{self._name}' returned None")

        if is_context_manager(instance):
            instance = self._exit_stack.enter_context(instance)
        self._instance = instance
        return instance

    def resolve_dependencies(
            self,
            resolver: typing.Callable[[str, typing.Type], 'ObjectDescriptor'],
            exit_stack: contextlib.ExitStack,
    ):
        self._resolved_deps = {name: resolver(name, typ) for name, typ in self._deps.items()}
        self._exit_stack = exit_stack

    @classmethod
    def from_(cls, name, obj) -> 'ObjectDescriptor':
        if obj is None:
            raise ValueError(None)
        elif isinstance(obj, type) or callable(obj):
            return ObjectDescriptor.from_callable(name, obj)
        else:
            return ObjectDescriptor.from_object(name, obj)

    @classmethod
    def from_callable(cls, name, factory: FactoryType) -> 'ObjectDescriptor':
        assert factory is not None
        signature = inspect.signature(factory)
        if isinstance(factory, type):
            t = factory
        else:
            if signature.return_annotation is not inspect.Signature.empty:
                t = signature.return_annotation
                if t is None:
                    raise TypeError(name, 'Callable type hint is None', factory)
            else:
                raise TypeError(name, 'No return type annotation')

        deps = spec_to_types(signature)

        log.debug("Dependencies for %s: %s", factory.__qualname__, deps)
        return ObjectDescriptor(factory, name, t, deps)

    @classmethod
    def from_object(cls, name, value: object) -> 'ObjectDescriptor':
        assert value is not None, f'{name} is None'
        result = ObjectDescriptor(None, name, type(value), {})
        result._instance = value
        return result

    def __repr__(self):
        return f'<{self.__class__.__name__}> {self._name}: {self._type.__name__}'

    def __eq__(self, other):
        if isinstance(other, ObjectDescriptor):
            return self._factory == other._factory and \
                   self._type == other._type and \
                   self._deps == other._deps
        else:
            return NotImplemented

    @property
    def object_type(self) -> typing.Type[T]:
        return self._type

    @property
    def dependencies(self):
        return self._deps

    @property
    def instance(self) -> T:
        return self._instance \
            if self._instance is not None \
            else self._resolve()

    @property
    def name(self):
        return self._name


def spec_to_types(spec: inspect.Signature) -> typing.Dict[str, typing.Type]:
    return {
        key: _assert_param_not_empty(key, param.annotation)
        for key, param in spec.parameters.items()
        if key != 'self'
    }


def _assert_param_not_empty(name, obj):
    if obj is inspect.Signature.empty:
        raise TypeError(name, inspect.Signature.empty)
    else:
        return obj


def is_context_manager(obj: object) -> bool:
    d = dir(obj)
    return '__enter__' in d and '__exit__' in d


class _DependencyChecker:
    def __init__(self, objects: typing.Dict[str, ObjectDescriptor]):
        self._map = objects
        self._clean = []

    def check(self):
        for name, descr in self._map.items():
            self.check_defs(name, descr)

        for name in self._map.keys():
            self.check_cycles(name, [])

    def check_defs(self, name: str, descr: ObjectDescriptor):
        for dep_name, dep_type in descr.dependencies.items():
            if dep_name not in self._map.keys():
                raise ValueError(f'Unresolved dependency of {name} => {dep_name}: {dep_type}')
            if not issubclass(self._map[dep_name].object_type, dep_type):
                raise ValueError(
                    f'{descr.name}: {descr.object_type.__name__} has dependency {dep_name}: {dep_type.__name__},'
                    f' but {dep_name} is type {self._map[dep_name].object_type.__name__}')

    def check_cycles(self, name: str, stack: typing.List[str]) -> None:
        """
        :param name:
        :param stack: reverse dependencies excluding the current one
        """
        if name in stack:
            raise ValueError(f'{name} depends on itself. Dependency path: {stack + [name]}')

        for dep_name in self._map[name].dependencies:
            self.check_cycles(dep_name, stack + [name])


def _is_under(name: str) -> bool:
    return name.startswith('_')


def to_factory_map(configurer) -> typing.Mapping[str, object]:
    if isinstance(configurer, typing.Mapping):
        return configurer
    else:
        return services_from_object(configurer)


def services_from_object(configurer: object) -> typing.Dict[str, object]:
    return {name: getattr(configurer, name)
            for name in dir(configurer)
            if not _is_under(name)
            }
