Member
======

.. http:get:: /member/

   Returns info about all members.

   **Example request**:

   .. sourcecode:: http

      GET /member/?format=json HTTP/1.1

   :query filter: one of ``username``, ``first_name``, ``last_name``, ``email``
   :query offset: offset number. default is 0
   :query limit: limit number. default is 20
   :statuscode 200: Everything is gonna be alright.

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

.. http:get:: /member/(int:member_id)/

   Returns info about member (`member_id`).

   **Example request**:

   .. sourcecode:: http

      GET /member/1337/?format=json HTTP/1.1
      Content-Type: application/json
       
   :statuscode 200: OK!
   :statuscode 404: There's no user with given id.

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
   :statuscode 403: Returned if request contains `"username"` field.
   :statuscode 500: Invalid body.

.. http:delete:: /member/(int:member_id)/

   Deactivates a member.

   .. sourcecode:: http

      DELETE /member/1337/?format=json HTTP/1.1

   :statusc:de 403: 
