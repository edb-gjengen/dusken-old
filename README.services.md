# Service design

ApiHook-model with the following attributes:
* event
* callback-URL
* member
* (active)

Our own Tastypie BaseResource which triggers events based on:
* resource_name / type of object
* method used.

Add logic to our Django Basemodel 

Use a queue for service tasks:
* rq (python library with redis backend)

Take a look at signals
* pre_save
* post_save
