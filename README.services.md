# Service design

ServiceHook-model with the following attributes [DONE]:

* event
* callback-URL
* member
* (active)

Our own Tastypie BaseResource which triggers events based on:

* resource_name / type of object
* method used.

Use a queue for service tasks, f.ex rq (python library with redis backend)

Add logic to our Django Basemodel 

Take a look at Django signals:

* pre_save
* post_save
