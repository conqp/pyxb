from __future__ import print_function
import pyxb.bundles.opengis.oseo_1_0 as oseo
import pyxb.utils.utility
import sys
import traceback

# Import to define bindings for namespaces that appear in instance documents
import pyxb.bundles.wssplat.wsnt

for f in sys.argv[1:]:
    print("------------------ %s" % (f,))
    xmld = pyxb.utils.utility.DataFromURI(f)
    try:
        instance = oseo.CreateFromDocument(xmld)
        # print xmld
        print(instance.toxml("utf-8"))
    except Exception as e:
        print("%s failed: %s" % (f, e))
        traceback.print_exception(*sys.exc_info())
        sys.exit(1)
