MDocument
=========

Simple DRM for async mongo motor client

Usage
-----

.. code-block:: python

    import asyncio

    from MDocument import Document

    class Comment(Document):
        __collection__ = "comments"


    class Video(Document):
        __collection__ = "videos"

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

Play from console
-----------------

If you want changes made from console immediately you can use `update_immediately` argument

.. code-block:: python

    run = loop.run_until_complete

    video = run(Video.create(update_immediately=True,
        title="Test"))
    video.length = "1:10"

Now we can find that original document was changed

.. code-block:: python

    print(run(Video.collection.find_one({"length": "1:10"})))
    {'_id': ObjectId('5e75373e5eb6a8c6d24d3cce'), 'title': 'Test', 'length': '1:10'}


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

    from MDocument import Document


    class Message(Document):
        __collection__ = "messages"

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

.delete
-------

Deletion of document from database. Based on your set @related rules all related documents will be modified too.

.. code-block:: python

    message = await Message.one(from_user="admin")

    await message.delete()

