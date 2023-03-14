# cgxSetMTU
set MTU to IONs

use `--list` to create a list of elements
element list file need to have one element name per line. use `#` at the begining of the line to comment skip that element
## example for a run
python cgxSetMTU.py --elements elements.txt --mtu 1472
