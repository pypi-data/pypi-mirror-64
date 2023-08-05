MDocument
=========

Simple DRM for async mongo motor client

Usage
-----

.. code-block:: python

    import asyncio

    from mdocument import Document, DatabaseClient

    client1 = DatabaseClient(uri="localhost")

    class Comment(Document):
        _collection_ = "comments"
        _database_ = "mdocument"
        _client_ = client1


    class Video(Document):
        _collection_ = "videos"
        _database_ = "mdocument"
        _client_ = client1

        @Document.related(self_field="_id", other_field="video")
        def comments(self):
            return Comment


    loop = asyncio.get_event_loop()
    Document.setup(loop, "localhost", "test_database")

    async def main():
        video = await Video.create(
            title="Test",
        )

        comment1 = await Comment.create(
            video=video._id,
            message="First!",
        )

        comment2 = await Comment.create(
            video=video._id,
            message="Second!"
        )

    loop.run_until_complete(main())

Now we can easily access our comments using our related documents

.. code-block:: python

    print(await video.comments)
    [
        Comment(_id=5e7533d55eb6a8c6d24d3cc7, video=5e7533d55eb6a8c6d24d3cc6, message=First!),
        Comment(_id=5e7533d55eb6a8c6d24d3cc8, video=5e7533d55eb6a8c6d24d3cc6, message=Second!)
    ]

Document methods
================

Here is a list of Document basic methods

@related
--------

Decorator for defining related documents. Made for easily managing deletion of related documents.

.. code-block:: python

    def related(self_field, other_field, multiple=True, on_delete=None):

Example:

.. code-block:: python

    from mdocument import Document, DeleteDocument


    class Artist(Document):
        __collection__ = "artists"

        @Document.related("_id", "album._id", on_delete=DeleteDocument)
        def albums(self):
            return Album

    class Album(Document):
        __collection__ = "messages"

        @Document.related("_id", "album._id", on_delete=DeleteDocument)
        def songs(self):
            return Song


    class Song(Document):
        __collection__ = "songs"

As we set our relations. Now we have next actions:
Album deleted -> all songs related to this album are deleted
Author deleted -> all albums related to author are deleted -> each song related to deleted albums deleted

.create
-------
.. code-block:: python

    async def create(cls, loop=None, update_immediately=False, **kwargs):

If you want to create a new document you can do it easily with .create method.
Example:

.. code-block:: python

    import asyncio

    from mdocument import Document, DatabaseClient


    class Message(Document):
        _collection_ = "messages"
        _database_ = "mdocument"
        _client_ = DatabaseClient(host="localhost")

    Document.setup(loop, "localhost", "test_database")

    loop.run_until_complete(
        Message.create(from_user="admin", text="Test message!")
    )

This will create document in database:

.. code-block:: python

    {
        '_id': ObjectId('5e75373e5eb6a8c6d14d3ccd'),
        'from_user': 'admin',
        'text': "Test message!"
    }

.push_update
------------

Updates document and all @related fields.

.. code-block:: python

    await Message.push_update()

.delete
-------

Deletion of document from database. Based on your set @related rules all related documents will be modified too.

.. code-block:: python

    message = await Message.one(from_user="admin")

    await message.delete()
