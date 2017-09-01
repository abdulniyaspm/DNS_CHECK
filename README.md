# DNS_CHECK

Check forward DNS, backward DNS and ping response of a server using python

###Prerequisite

Python should be installed in your local machine.
If not you can download and install from [here](https://www.python.org/)

### Usage

```
from DNS import *

# test.txt contains the servers list
a = DNS("test.txt")
a.execute()

```

###Output

```
Enter 1 ---> Forward DNS
Enter 2 ----> Reverse DNS
Enter 3 ---> Ping Response
Enter Your Input 1

google.com ---------> ********
gmail.com ---------> **********
stackoverflow.com ---------> ************
www.facebook.com ---------> ***********
www.instagram.com ---------> ************

```
