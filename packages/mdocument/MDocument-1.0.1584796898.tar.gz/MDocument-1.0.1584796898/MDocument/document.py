import logging
import asyncio

from asyncio import AbstractEventLoop
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorClient

LOG = logging.getLogger("mongo")


def check_setup(func):
    """Decorator for checking that document have valid loop and client."""

    async def arg_wrap(cls, *args, **kwargs):
        if not hasattr(cls, "__loop__") and "loop" not in kwargs:
            raise LoopNotFound()
        elif not hasattr(cls, "__client__") and "client" not in kwargs:
            raise ClientNotFound()
        return await func(cls, *args, **kwargs)
    return arg_wrap


class DocumentException(Exception):
    def __init__(self, message):
        self.message = message


class DocumentDoesntExist(DocumentException):
    def __init__(self):
        super().__init__("Document not found")


class ClientNotFound(DocumentException):
    def __init__(self):
        super().__init__("Client is not provided. Please use Document.setup().")


class LoopNotFound(DocumentException):
    def __init__(self):
        super().__init__("Loop is not provided. Please use Document.setup().")


class DocumentField:

    def __init__(self, parent_dict: dict, update_immediately, update_func):
        self.__parent_dict = parent_dict
        self.__update_immediately = update_immediately
        self.__update_func = update_func
        self.__index = 0

    def __getattr__(self, item):
        if not isinstance(item, str):
            raise AttributeError(f"{item} doesnt exist.")
        if item.startswith("_DocumentField__"):
            return super().__getattribute__(item)
        try:
            value = self.__parent_dict[item]
        except KeyError:
            raise AttributeError(item)

        if isinstance(value, dict):
            return type(item, (DocumentField,), value)(self.__parent_dict[item],
                                                       self.__update_immediately,
                                                       self.__update_func)
        elif isinstance(value, list):
            return type(item, (DocumentArrayField,), {"value": value})(self.__parent_dict[item],
                                                                       self.__update_immediately,
                                                                       self.__update_func)
        return value

    def __getitem__(self, item):
        try:
            return getattr(self, item)
        except AttributeError:
            raise KeyError(f"{item} doesnt exist.")

    def __repr__(self):
        return str(self.__dict__)

    def __setattr__(self, key, value):
        if key.startswith("_DocumentField__"):
            super().__setattr__(key, value)
        else:
            self.__parent_dict.update({key: value})
            if self.__update_immediately:
                self.__update_func()

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def __delattr__(self, item):
        if item.startswith("_Document__"):
            raise AttributeError(f"Cannot delete {item}")
        else:
            del self.__parent_dict[item]
            if self.__update_immediately:
                self.__update_func()

    def __delitem__(self, key):
        return delattr(self, key)

    @property
    def __dict__(self):
        return self.__parent_dict

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        try:
            result = list(self.__parent_dict.keys())[self.__index]
            self.__index += 1
            return result
        except IndexError:
            raise StopIteration()

    def keys(self):
        return self.__parent_dict.keys()

    def items(self):
        result = {}
        for key in self.__parent_dict:
            result[key] = self[key]
        return result

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default


class DocumentArrayField:

    def __init__(self, parent_list: list, update_immediately, update_func):
        self.__parent_list = parent_list
        self.__update_immediately = update_immediately
        self.__update_func = update_func
        self.__index = 0

    def append(self, item):
        self.__parent_list.append(item)
        if self.__update_immediately:
            self.__update_func()

    def remove(self, item):
        self.__parent_list.remove(item)
        if self.__update_immediately:
            self.__update_func()

    def pop(self, item=None):
        self.__parent_list.pop(item) if item else self.__parent_list.pop()
        if self.__update_immediately:
            self.__update_func()

    def extend(self, iterable):
        self.__parent_list.extend(iterable)
        if self.__update_immediately:
            self.__update_func()

    def clear(self):
        self.__parent_list.clear()
        if self.__update_immediately:
            self.__update_func()

    def reverse(self):
        self.__parent_list.clear()
        if self.__update_immediately:
            self.__update_func()

    def insert(self, index, item):
        self.__parent_list.insert(index, item)
        if self.__update_immediately:
            self.__update_func()

    def __getattr__(self, item):
        raise NotImplemented()

    def __delattr__(self, item):
        raise NotImplemented

    def __repr__(self):
        return str(self.__parent_list)

    def __getitem__(self, item):
        if isinstance(self.__parent_list[item], dict):
            return DocumentField(
                self.__parent_list[item], self.__update_immediately, self.__update_func)
        else:
            return self.__parent_list[item]

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        try:
            result = self[self.__index]
            self.__index += 1
            return result
        except IndexError:
            raise StopIteration()


class MetaDocument(type):
    collection: AsyncIOMotorCollection

    @property
    def collection(cls) -> AsyncIOMotorCollection:
        if not getattr(cls, "__client__", None):
            raise ClientNotFound()
        return cls.__client__[cls.__database__][cls.__collection__]


class Document(metaclass=MetaDocument):
    __database__ = "database"
    __collection__ = "collection"
    __loop__: AbstractEventLoop
    __client__: AsyncIOMotorClient

    def __init__(self, loop=None, update_immediately=False, sync_load=False, **kwargs):
        self.__update_immediately = update_immediately
        self.__loop__ = loop if loop else self.__class__.__loop__
        self.__properties = {}
        if sync_load:
            self.__loop__.run_until_complete(self._coro_init(kwargs))
        elif not asyncio._get_running_loop():
            LOG.warning("Loop is not running. Consider using sync mode.")

    @classmethod
    async def _async_init(cls, loop=None, update_immediately=False, **kwargs):
        if not kwargs:
            raise DocumentDoesntExist()

        document = cls(loop=loop if loop else cls.__loop__,
                       update_immediately=update_immediately,
                       sync_load=False)

        await document._coro_init(kwargs)
        return document

    async def _coro_init(self, kwargs):
        self.__values = await self.find_one(kwargs)
        if not self.__values:
            raise DocumentDoesntExist()

    def __repr__(self):
        return "{0}({1})".format(
            self.__class__.__name__,
            ", ".join(f"{key}={value}" for key, value in self.__dict__.items())
        )

    def __getattr__(self, item):
        if item.startswith("_Document__"):
            return super(Document, self).__getattribute__(item)
        elif item == "collection":
            return super(Document, self).__getattribute__(item)
        if isinstance(self.__values[item], dict):
            return type(item, (DocumentField,), self.__values[item])(self.__values[item],
                                                                     self.__update_immediately,
                                                                     self.update_inner_fields)
        elif isinstance(self.__values[item], list):
            return type(item, (DocumentArrayField,), {})\
                (self.__values[item], self.__update_immediately, self.update_inner_fields)
        try:
            return self.__values[item]
        except KeyError:
            raise AttributeError(item)

    def __getitem__(self, item):
        if item.startswith("_Document__"):
            raise KeyError(item)
        return getattr(self, item)

    def __setattr__(self, key, value):
        if key.startswith("_Document__"):
            return super().__setattr__(key, value)
        elif key.startswith("__") and key.endswith("__"):
            return super().__setattr__(key, value)
        elif key == "_id":
            raise AttributeError("_id cannot be edited")
        self.__values[key] = value
        if self.__update_immediately:
            self.run_in_loop(self.push_update())

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def __delattr__(self, item):
        if item.startswith("_Document__"):
            raise AttributeError(f"Cannot delete {item}")
        else:
            del self.__values[item]
            if self.__update_immediately:
                self.run_in_loop(self.push_update())

    def __delitem__(self, key):
        return delattr(self, key)

    def update_inner_fields(self):
        self.run_in_loop(self.push_update())

    def run_in_loop(self, coro):
        if self.__loop__.is_running():
            self.__loop__.create_task(coro)
        else:
            return self.__loop__.run_until_complete(coro)

    @property
    def __dict__(self):
        return {key: value for key, value in self.__values.items() if key != "_Document__values"}

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return self.__class__.collection

    @classmethod
    @check_setup
    async def find_one(cls, query, *args, **kwargs):
        """Proxy method for mongo find_one method."""

        result = await cls.collection.find_one(query, *args, **kwargs)

        if not result:
            raise DocumentDoesntExist()
        return result

    @classmethod
    @check_setup
    async def find(cls, query, *args, **kwargs):
        """Proxy for mongo find_one method."""

        return cls.collection.find(query, *args, **kwargs)

    @classmethod
    @check_setup
    async def update(cls, find_query, update_query, *args, **kwargs):
        """Proxy method for pymongo."""

        return await cls.collection.update(find_query, update_query, *args, **kwargs)

    @check_setup
    async def push_update(self):
        """Force update document."""

        return await self.collection.replace_one({"_id": self._id}, self.__values)

    @classmethod
    @check_setup
    async def update_one(cls, find_query, update_query, *args, **kwargs):

        return await cls.collection.update_open(find_query, update_query, *args, **kwargs)

    @classmethod
    @check_setup
    async def delete_one(cls, query, *args, **kwargs):
        """Proxy for mongo delete_one method."""

        return await cls.collection.delete_one(query, *args, **kwargs)

    @classmethod
    @check_setup
    async def delete_many(cls, query, *args, **kwargs):
        """Proxy for mongo delete_many method."""

        return await cls.collection.delete_many(query, *args, **kwargs)

    @classmethod
    @check_setup
    async def insert_one(cls, query, *args, **kwargs):
        """Proxy for mongo insert_one method."""

        return await cls.collection.insert_one(query, *args, **kwargs)

    @classmethod
    @check_setup
    async def insert(cls, query, *args, **kwargs):
        """Proxy for mongo insert method."""

        return await cls.collection.insert(query, *args, **kwargs)

    @classmethod
    @check_setup
    async def exists(cls, *args, **kwargs):
        """Checks that document exists."""

        if await cls.collection.find_one(*args, **kwargs):
            return True
        return False

    @classmethod
    @check_setup
    async def aggregate(cls, *args, **kwargs):
        """Proxy for mongo aggregate method."""

        return cls.collection.aggregate(*args, **kwargs)

    @classmethod
    def setup(cls, loop, database_uri, default_database="database") -> None:
        """Setup main Document class for all of its children."""

        cls.__loop__ = loop
        cls.__client__ = AsyncIOMotorClient(database_uri)
        cls.__database__ = default_database

    @classmethod
    async def one(cls, loop=None, update_immediately=False, **kwargs):
        """Finds one document based on kwargs."""

        document = await cls.find_one(kwargs)
        return await cls._async_init(loop, update_immediately, **document)

    @classmethod
    async def many(cls, loop=None, update_immediately=False, **kwargs) -> list:
        """Finds multiple documents based on kwargs."""

        result_list = []
        cursor = cls.collection.find(kwargs)
        async for doc in cursor:
            result_list.append(await cls._async_init(loop, update_immediately, **doc))
        return result_list

    @classmethod
    async def create(cls, loop=None, update_immediately=False, **kwargs):
        """Create new document."""

        await cls.insert_one(kwargs)
        return await cls._async_init(loop, update_immediately, _id=kwargs["_id"])

    async def delete(self):
        """Delete current document."""

        return await self.delete_one({"_id": self._id})

    @staticmethod
    def lazy_property(self_field, other_field, multiple=True):
        """Lazy property decorator.

        :param self_field: primary key field of current document
        :param other_field: search field of searched document
        :param multiple: return multiple documents or only one
        """

        def func_wrapper(func):
            async def fget(self):
                if multiple:
                    return await func(self).many(self.__loop__,
                                                 self.__update_immediately,
                                                 **{other_field: self[self_field]})
                else:
                    return await func(self).one(self.__loop__,
                                                self.__update_immediately,
                                                **{other_field: self[self_field]})
            return property(fget=fget)
        return func_wrapper
