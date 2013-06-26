Institution
======

GET /institution/
------------
.. http:get:: /institution/

   Returns info about all institutions.

   **Example request**:

   .. sourcecode:: http

      GET /institution/?format=json HTTP/1.1

   :query offset: offset number. default is 0
   :query limit: limit number. default is 20
   :statuscode 200: Everything is gonna be alright.
   :statuscode 403: User does not have necessary permissions.

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/javascript

      {
         "meta" : {
            "limit" : 20,
            "next" : null,
            "offset" : 0,
            "previous" : null,
            "total_count" : 2
         },
         "objects" : [
             {
                 "created": "2013-06-26T12:15:52.889701",
                 "id": 1,
                 "name": "Universitetet i Oslo",
                 "resource_uri": "/api/v1/institution/1/",
                 "short_name": "UiO",
                 "updated": "2013-06-26T12:15:52.889785"
             },
             {
                 "created": "2013-06-26T12:16:07.840886",
                 "id": 2,
                 "name": "Høgskolen i Oslo og Akershus",
                 "resource_uri": "/api/v1/institution/2/",
                 "short_name": "HiOA",
                 "updated": "2013-06-26T12:29:38.488712"
             }
         ]
      }
