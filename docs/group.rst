Group
=====

GET /group/
-----------
.. http:get:: /group/

   Return information about all groups.

   **Example request**:

   .. sourcecode:: http
      
	  GET /group/?format=json HTTP/1.1

   :statuscode 200: OK!

GET /group/(int)/
-----------------
.. http:get:: /group/(int:group_id)/

   Return information about a specific group.

   .. sourcecode:: http

      GET /group/1337/?format=json HTTP/1.1

   :statuscode 200: OK!
   :statuscode 404: Group (`group_id`) was not found.

POST /group/
------------
.. http:post:: /group/

   Create new group.

   .. sourcecode:: http

      POST /group/?format=json HTTP/1.1
      Body:
      {
          "group_name" : "KAK: EDB",
          "posix_name" : "kak-edb"
      }

   :statuscode 201: Created!
   :statuscode 403: You don't have necessary permissions.
   :statuscode 500: Group with this `posix_name` alredy exists or malformed body.

PATCH /group/(int)/
-------------------
.. http:patch:: /group/(int:group_id)/

   Change name of a group.

   .. sourcecode:: http

      PATCH /group/1337/?format=json HTPP/1.1
      Body:
      {
          "group_name" : "Not KAK: EDB",
          "posix_name" : "not-kak-edb"
      }

   :statuscode 202: Changed!
   :statuscode 403: You don't have enough permissions to change this group.
   :statuscode 500: Group (`group_id`) does not exist or malformed body.

DELETE /group/(int)/
--------------------
.. http:delete:: /group/(int:group_id)/

   Delete a group.

   :statuscode 204: Deleted!
