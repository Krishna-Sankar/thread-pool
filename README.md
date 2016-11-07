# Multithreaded Server

This is the 2st assignment for CS4032 (Distributed Systems). The goal was to develop the skeleton for a multithreaded server supporting dynamic thread pooling and responding to a few simple messages over TCP sockets.

My information:

|Name             |Student ID|Status|
|-----------------|:--------:|:--------:|
|Benoit Chabod    |16336617  |Erasmus  |

## Usage

Like the previous assignment, I've tested this application on SCSS OpenNebula with two nodes.

 * A Debian node called master hosted the server
 * I launched test clients on boot2docker nodes

You need python to run this application. If you don't have it, use apt-get, brew, etc. It can be installed easily on a boot2docker node using:

```bash
tce-load -w -i python.tcz
```

### Running server

Just clone the repository anywhere, and run this:

```bash
./start.sh PORT
```
The compile.sh script does nothing and was just needed for the automated grading tools.
Please use CTRL-C to kill the server properly, or send him a *KILL_SERVICE* message.

### Running client

Just clone the repository anywhere, and run this (the IP address entered here needs to be the server one, and same goes for the port):

```bash
python client.py H|K IP PORT
```

H corresponds to a simple *HELO* message, and K corresponds to the *KILL_SERVICE* message.
Please see the subject for more details.

## Implementation

There are 3 variables to control the thread pool:
* MIN_THREADS, the minimum number of workers at any point
* MAX_THREADS, the maximum number of workers that can be alive to handle a huge volume of clients
* TOLERANCE, the minimum difference between the number of clients and the number of workers that needs to be reached before a resizing operation is done. This corresponds to the system's "inertia", and we want this to prevent a constant resizing that would be expensive in terms of performance.

A resizing decision may be taken every time a new client request arrives in the server's queue.
There's a lock on the requests queue to prevent race conditions. See code for more details.