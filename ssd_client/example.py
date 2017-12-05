import sys
from ssd_client import SsdZmqClient

if __name__ == '__main__':
    ssd = SsdZmqClient('tcp://gvbrainlan.vhomo.cn:12600')
    print ssd.detect(sys.argv[1])
    



