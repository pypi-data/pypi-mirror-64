import logging

from asyncio import AbstractEventLoop
from collections import ChainMap, UserDict
from functools import wraps
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorClient

from .document_dict import DocumentDict

LOG = logging.getLogger("mdocument")


class OnDeleteAction:
    pass


class DeleteDocument(OnDeleteAction):
    pass


class DeleteField(OnDeleteAction):
    pass


class PopFromArray(OnDeleteAction):
    pass


def check_setup(func):
    """Decorator for checking that document have valid loop and client."""

    async def arg_wrap(cls, *args, **kwargs):
        if not hasattr(cls, "_client_") and "client" not in kwargs:
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
        super().__init__("Client is not provided. Can't connect to database.")


class MetaDocument(type):
    collection: AsyncIOMotorCollection

    @property
    def collection(cls) -> AsyncIOMotorCollection:
        for field in ("_client_", "_database_", "_collection_"):
            if not hasattr(cls, field):
                raise type("{}NotFound".format(field.capitalize()), (DocumentException, ), {})(
                    f"Required attribute {field} is missing."
                )

        return cls._client_[cls._database_][cls._collection_]


class Document(metaclass=MetaDocument):
    _database_: str
    _collection_: str
    _loop_: AbstractEventLoop
    _client_: AsyncIOMotorClient
    _relations_ = {}

    def __init__(self, **kwargs):
        self._document_ = DocumentDict(kwargs)
        self._shadow_copy_ = kwargs.copy()
        self._relations_ = {}

    @classmethod
    async def _async_init(cls, **kwargs):

        document_in_database = await cls.collection.find_one(kwargs)
        if not document_in_database:
            raise DocumentDoesntExist()
        return cls(**document_in_database)

    def __repr__(self):
        return "{0}({1})".format(
            self.__class__.__name__,
            ", ".join(f"{key}={value}" for key, value in self._document_.items())
        )

    @property
    def __dict__(self):
        return self._document_

    def __getattr__(self, item):
        try:
            item = ChainMap(
                super().__getattribute__("__dict__"),
                super().__getattribute__("_document_"))[item]
            if isinstance(item, dict):
                return DocumentDict(item)
            return item
        except KeyError:
            raise AttributeError()

    def __setattr__(self, key, value):
        if key.startswith("_") and key.endswith("_"):
            return super().__setattr__(key, value)
        else:
            self._document_[key] = value

    def __delattr__(self, item):
        del self._document_[item]

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def __getitem__(self, item):
        return self._document_[item]

    def __delitem__(self, key):
        return delattr(self, key)

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return self.__class__.collection

    async def _update_related(self):
        """Force updates related fields in other documents."""

        self_relations = set({v for v in self.__class__.__dict__.values()
                              if isinstance(v, property)})

        relate_properties = set(Document._relations_).intersection(self_relations)

        if not relate_properties:
            return

        property_data = [Document._relations_[relate] for relate in relate_properties]

        for prop in property_data:
            self_field = prop["self_field"]
            other_field = prop["other_field"]
            document = prop["document_func"](self)
            if self[self_field] != self._shadow_copy_[self_field]:
                await document.collection.update_many(
                    {other_field: self._shadow_copy_[self_field]},
                    {"$set": {other_field: self[self_field]}}
                )

    @check_setup
    async def push_update(self):
        """Force update document."""

        await self._update_related()

        return await self.collection.replace_one({"_id": self._id}, self._document_)

    @classmethod
    @check_setup
    async def exists(cls, *args, **kwargs):
        """Checks that document exists."""

        if await cls.collection.find_one(*args, **kwargs):
            return True
        return False

    @classmethod
    @check_setup
    async def one(cls, **kwargs):
        """Finds one document based on kwargs."""

        document = await cls.collection.find_one(kwargs)
        document = document if document else {}
        return await cls._async_init(**document)

    @classmethod
    @check_setup
    async def many(cls, **kwargs) -> list:
        """Finds multiple documents based on kwargs."""

        result_list = []
        cursor = cls.collection.find(kwargs)
        async for doc in cursor:
            result_list.append(await cls._async_init(**doc))
        return result_list

    @classmethod
    @check_setup
    async def create(cls, **kwargs) -> "Document":
        """Create new document."""

        await cls.collection.insert_one(kwargs)
        return await cls._async_init(_id=kwargs["_id"])

    async def _delete_related_pop(self, document, self_field, other_field):
        """Pop self key from other documents Array field."""

        await document.collection.update_many(
            {other_field: self[self_field]},
            {"$pull": {other_field: self[self_field]}})

    async def _delete_other(self, doc, delete_info):

        if delete_info["on_delete"] is DeleteDocument:
            for doc in await doc.many(**{
                delete_info["self_field"]: self[delete_info["other_field"]]
            }):
                await doc.delete()
        elif delete_info["on_delete"] is PopFromArray:
            await self._delete_related_pop(document=doc,
                                           self_field=delete_info["self_field"],
                                           other_field=delete_info["other_field"])

        elif delete_info["on_delete"] is DeleteField:
            await doc.collection.update_many(
                {delete_info["self_field"]: self[delete_info["other_field"]]},
                {"$unset": {delete_info["self_field"]: ""}})

    async def _delete_by_prop(self, relations):

        for prop, delete_info in relations.items():

            property_name = prop.fget.__name__
            document = delete_info["other_document"]()

            if delete_info["on_delete"] is DeleteDocument:
                for doc in await getattr(self, property_name):
                    await doc.delete()

            elif delete_info["on_delete"] is PopFromArray:
                await self._delete_related_pop(document=document,
                                               self_field=delete_info["self_field"],
                                               other_field=delete_info["other_field"])

            elif delete_info["on_delete"] is DeleteField:
                await document.collection.update_many(
                    {delete_info["other_field"]: self[delete_info["self_field"]]},
                    {"$unset": {delete_info["other_field"]: ""}})

    async def _delete_related(self):
        """Deletes related documents or pops field values."""

        self_properties = set({v for v in self.__class__.__dict__.values()
                               if isinstance(v, property)})

        other_properties = {
            k: v for k, v in Document._relations_.items() if v["other_document"]() is
                self.__class__}

        relations = set(Document._relations_).intersection(self_properties)

        await self._delete_by_prop({prop: delete_info for prop, delete_info
            in Document._relations_.items() if prop in relations
        })

        for prop, delete_info in other_properties.copy().items():

            doc = delete_info["self_document"]()

            await self._delete_other(doc, delete_info)

    async def delete(self):
        """Delete current document and related fields or documents base on related."""

        result = await self.collection.delete_one({"_id": self._id})
        await self._delete_related()
        return result

    @staticmethod
    def related(self_path, other_path, multiple=True, on_delete=None):
        """Decorator for related documents.

        :param on_delete: actions to take when document is deleted
        :param self_path: Document.key to self pk
        :param other_path: Document.key to other pk
        :param multiple: return multiple documents or only one
        """

        def func_wrapper(func):

            self_field = ".".join(self_path.split(".")[1:])
            other_field = ".".join(other_path.split(".")[1:])

            def get_self_document():
                for subclass in Document.__subclasses__():
                    if subclass.__name__ == self_path.split(".")[0]:
                        return subclass

            def get_other_document():
                for subclass in Document.__subclasses__():
                    if subclass.__name__ == other_path.split(".")[0]:
                        return subclass

            @wraps(func)
            async def fget(self):
                other_document = get_other_document()

                if multiple:
                    return await other_document.many(**{other_field: self[self_field]})
                else:
                    return await other_document.one(**{other_field: self[self_field]})

            result = property(fget=fget)

            delete_item = {
                "self_field": self_field,
                "other_field": other_field,
                "on_delete": on_delete,
                "self_document": get_self_document,
                "other_document": get_other_document
            }

            Document._relations_[result] = delete_item

            return result
        return func_wrapper
