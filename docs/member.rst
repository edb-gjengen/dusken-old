Member
======

GET /member/
------------
.. http:get:: /member/

   Returns info about all members.

   **Example request**:

   .. sourcecode:: http

      GET /member/?format=json HTTP/1.1

   :query filter: one of ``username``, ``first_name``, ``last_name``, ``email``
   :query offset: offset number. default is 0
   :query limit: limit number. default is 20
   :statuscode 200: Everything is gonna be alright.

GET /member/(int)/
------------------
.. http:get:: /member/(int:member_id)/

   Returns info about member (`member_id`).

   **Example request**:

   .. sourcecode:: http

      GET /member/1337/?format=json HTTP/1.1
      Content-Type: application/json
       
   :statuscode 200: OK!
   :statuscode 403: No permissions, mate.
   :statuscode 404: There's no user with given id.

GET /member/(int)/group/
------------------------
.. http:get:: /member/(int:member_id)/group/

   Gets all groups member (`member_id`) is a member of.

   .. sourcecode:: http

      GET /member/1337/group/?format=json HTTP/1.1

   :statuscode 200: OK!
   :statuscode 403: You don't have enough permissions.

GET /member/(int)/group/(int)/
------------------------------
.. http:get:: /member/(int:member_id)/group/(int:group_id)/

   Checks if member (`member_id`) is a member of group (`group_id`).

   .. sourcecode:: http

      GET /member/1337/group/42/?format=json HTTP/1.1

   :statuscode 200: OK!
   :statuscode 403: No go, brother :(

POST /member/
-------------
.. http:post:: /member/

   Creates a new member with data given in body (json)

   **Example request**:

   .. sourcecode:: http
      
      POST /member/ HTTP/1.1
      Body:
      {
        "username": "robertko",
        "email": "robert.kolner@gmail.com",
        "password": "uCantHaxThis"
      }

   :statuscode 201: User created.
   :statuscode 500: Invalid body or username already exists.

POST /member/(int)/group/(int)/
-------------------------------
.. http:post:: /member/(int:member_id)/group/(int:group_id)/

   Adds member (`member_id`) to group (`group_id`).

   :statuscode 201: User added!
   :statuscode 403: Yeah...no.

PATCH /member/(int)/
--------------------
.. http:patch:: /member/(int:member_id)/

   Updates fields of a member (`member_id`). Can't update username.

   **Example request**:

   .. sourcecode:: http
      
      PATCH /member/1337/?format=json HTTP/1.1
      Body:
      {
        "email": "robert.kolner@gmail.com",
        "password": "uCantHaxThis"
      }

   :statuscode 202: User changed.
   :statuscode 403: Returned if request contains `"username"` field or you're missing necessary permissions.
   :statuscode 500: Invalid body.

DELETE /member/(int)/
---------------------
.. http:delete:: /member/(int:member_id)/

   Deactivates a member.

   .. sourcecode:: http

      DELETE /member/1337/?format=json HTTP/1.1

   :statuscode 204: User deactivated.
   :statuscode 403: You don't have enough permissions to deactivate users.

DELETE /member/(int)/group/(int)/
---------------------------------

.. http:delete:: /member/(int:member_id)/group/(group_id)/

   Removes a member from a group.

   :statuscode 204: User removed from group.
   :statuscode 403: I can't let you do that, Dave.
