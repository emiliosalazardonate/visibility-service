import datetime

import os
from astropy.io.votable.tree import VOTableFile, Resource, Table, Field, Info
from django.http import HttpResponse

def visibility(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now

    # Create a new VOTable file...
    votable = VOTableFile()
    # ...with one resource...
    resource = Resource()
    votable.resources.append(resource)

    # ... with one table
    table = Table(votable)
    resource.tables.append(table)


    resource.description ="European Space Astronomy Centre. INTEGRAL SOC - " \
                          "Object Visibility Simple Access Protocol (ObjVisSAP)"
    resource.infos.append(Info(name = "QUERY_STATUS", value = "OK"))

    resource.infos.append(Info(name = "SERVICE PROTOCOL", value = "1.0"))
    resource.infos.append(Info(name = "REQUEST", value = "queryData"))
    resource.infos.append(Info(name = "s_ra", value = "%s"%request.GET.get("s_ra")))
    resource.infos.append(Info(name = "s_dec", value = "%s"%request.GET.get("s_dec")))
    resource.infos.append(Info(name = "t_min", value = "%s"%request.GET.get("t_min")))
    resource.infos.append(Info(name = "t_max", value = "%s"%request.GET.get("t_max")))


    # Define some fields
    # table.fields.extend([
    #     Field(votable, name="filename", datatype="char", arraysize="*"),
    #     Field(votable, name="matrix", datatype="double", arraysize="2x2")])

    table.fields.extend([
        Field(votable, name="t_start", datatype="double", ucd="time.start",
              utype="Char.TimeAxis.Coverage.Bounds.Limits.StartTime"),
        Field(votable, name="t_stop", datatype="double", ucd="time.start",
              utype="Char.TimeAxis.Coverage.Bounds.Limits.StartTime"),
        Field(votable, name="t_visibility", datatype="double", ucd="time.start",
              utype="Char.TimeAxis.Coverage.Bounds.Limits.StartTime"),

    ])
    results = getVisibilityIntervals(request.GET.get("s_ra"), request.GET.get("s_dec"),request.GET.get("t_min"), request.GET.get("t_max") )

    number_of_intervals = len(results)
    table.create_arrays(number_of_intervals)
    for i in range(0, number_of_intervals):
        table.array[i] = (results[i][0], results[i][1], results[i][2])


    # Now write the whole thing to a file to be streamed
    # Note, we have to use the top-level votable file object

    xml_now = "/tmp/new_votable_%s.xml" % now
    votable.to_xml(xml_now)
    stream = open(xml_now).read()
    os.remove(xml_now)
    return HttpResponse(stream, content_type='text/xml')


def getVisibilityIntervals(ra, dec, start, end):
    #These are mock data.
    #This is telescope-related. The values are [t_start (in MJD), t_stop (in MJD), t_visibility (in seconds) ].
    # Each observatory should provide with this values.


    results = [[58986.01767361111, 58987.993101851855, 170677],
         [58988.01767361111, 58989.993101851855, 170637],
         [58990.01767361111, 58997.993101851855, 170647],
         [58992.01767361111, 59997.993101851855, 170647]]


    return results

