from cmu_112_graphics import *
from datetime import *

from ics_parsing2 import *
from graphics2 import *

if __name__ == "__main__":

    #testing with fake

    concepts = event("15-151 Discrete Mathematics", \
        datetime(2021, 11, 11, 13, 25, tzinfo=timezone.utc), \
            datetime(2021, 11, 11, 16, 15, tzinfo=timezone.utc))

    linear_algebra = event("21-241 Linear Algebra", \
        datetime(2021, 11, 11, 17, 5, tzinfo=timezone.utc), \
            datetime(2021, 11, 11, 19, 55, tzinfo=timezone.utc))

    runApp(width=1000, height=800)