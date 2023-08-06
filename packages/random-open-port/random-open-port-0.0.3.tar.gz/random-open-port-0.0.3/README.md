# random-open-port

The random open port provides some helpful functionality for getting a random port that isn't
tracked identified as a known port in <https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers#Registered_ports>.

## Installation

```pip3 install random-open-port```

### Requirements

Python 3+


## Using from the command line.

Simply run

```console
foo@bar:~$ random-port
Random Port: 36952
```

## Examples

### Getting a random port.

```
from random_open_port import random_port
port = random_port()
```

### Getting the affiliated ports.

```
from random_open_port import get_taken_ports
taken_ports = get_taken_ports() 
```

### Getting the ports directly from Wikipedia.

```
from random_open_port import get_wiki_ports
wiki_ports = get_wiki_ports()
```

### Getting the ports from the cached file.

```
from random_open_port import read_ports_file
cached_ports = read_ports_file()
```



