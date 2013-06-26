Membership
==========

GET /membership/
----------------
.. http:get:: /membership/

   Returns info about all memberships.

   **Example request**:

   .. sourcecode:: http

      GET /membership/?format=json HTTP/1.1

   :query filter: one of ``valid``, ``can_vote``
   :query offset: offset number. default is 0
   :query limit: limit number. default is 20
   :statuscode 200: Thumbs up!
   :statuscode 403: Ur not authorized – don't cheat!

   **Example response**:

   .. sourcecode:: http

      {
         "meta" : {
            "limit" : 20,
            "next" : null,
            "offset" : 0,
            "previous" : null,
            "total_count" : 1
            },
         "objects" : {
            "created" : "2012-08-23T01:30:14",
            "end_date" : "2013-08-01T00:00:00",
            "id" : 1,
            "member" : 1,
            "membership_type" : 1,
            "payment" : 86,
            "start_date" : "2012-08-23T01:30:14",
            "updated" : "2013-08-01T00:00:00",
            }

         }

GET /membership/(int)/
----------------------
.. http:get:: /membership/(int:membership_id)/

   Returns info about membership (`membership_id`).

   **Example request**:

   .. sourcecode:: http
       
      GET /membership/13371337/?format=json HTTP/1.1
      Content-Type: application/json

   :statuscode 200: Thumbs up!
   :statuscode 403: You'll need to get authorized first, buddy.
   :statuscode 404: This is not the membership you're looking for.

   **Example response**:
   
   .. sourcecode:: http
      
      {
         "membership" : {
            "created" : "2012-08-23T01:30:14",
            "end_date" : "2013-08-01T00:00:00",
            "id" : 1,
            "member" : 1,
            "membership_type" : 1,
            "payment" : 86,
            "start_date" : "2012-08-23T01:30:14",
            "updated" : "2013-08-01T00:00:00",
            }

         }

POST /membership/
-----------------
.. http:post:: /membership/
   
   Creates a new membership with data given in body (json).

   **Example request**:

   .. sourcecode:: http
      
      POST /membership/ HTTP/1.1
      Body:
      {
         "member": 1337,
         "membership_type": 1,
         "payment": 16811,
      }
   
   :statuscode 201: You just created a brand new membership!
   :statuscode 403: Don't fake it – get authorized!
   :statuscode 500: You messed up and made a pile of poo. Check body, make sure values are correct.
