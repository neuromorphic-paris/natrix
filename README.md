# loris
read and write different file formats from neuromorphic cameras such as [.aedat](https://inivation.com/support/software/fileformat/), **.dat**, [.es](https://github.com/neuromorphic-paris/event_stream) or **.csv** and also [amazing animal](https://giphy.com/search/slow-loris)

### Supported formats
|        | version | read    | write   |
|--------|--------:|:-------:|:-------:|
| .aedat | 3.x     | &#9744; | &#9744; |
| .dat   | n/a     | &#9745; | &#9744; |
| .es    | 2.x     | &#9745; | &#9745; |
| .csv   | -       | &#9745; | &#9744; |

### Install
~~~python
pip install loris
~~~

### How to loris
##### Read a file, for example a .dat file
~~~python
import loris
my_file = loris.read_file("/path/to/my-file.dat")
~~~

##### Loop over all events
~~~python
for event in my_file['events']:
    print("ts:", event['t'], "x:", event['x'], "y:", event['y'], "p:", event['polarity'])
~~~

##### Write events to file using one of the supported formats, for example .es
~~~python
loris.write_events_to_file(my_file, "/path/to/my-file.es")
~~~

![loris](loris.gif "The Loris Banner")
