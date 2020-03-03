# visibility-service
This is a basic web service (REST) complaint with the Object Visibility Simple Access Protocol:

http://www.ivoa.net/documents/ObjVisSAP/index.html

The REST service needs python 3.6 and uses two libraries django and astropy:

Django==3.0.3
astropy==3.0.4

To run the server:

/path/to/python3/bin/python manage.py runserver


Starting development server at http://127.0.0.1:8000/

http://localhost:8000/visibility?s_ra=166&s_dec=-19&t_min=58910.43263888889&t_max=59094.39097222222

The part which is telescope-related is in the views.py file:

getVisibilityIntervals(ra, dec, start, end) in which each observatory must implement their calculation of the visibility 
intervals for a particular period of time in a specific part of the sky.
  

