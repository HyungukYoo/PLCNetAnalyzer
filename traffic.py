import plotly
import plotly.plotly as py
import plotly.graph_objs as go

import pyshark
import sys, os
import time

plotly.tools.set_credentials_file(username='hyunguk', api_key='WpiuW3ZzLxVJe0oRr0eH')

modbus_data = []

frame = []
length = []

frame_cnt = 0

def get_modbus_pkts(pkt):
    global frame_cnt
    frame_cnt += 1
#    print frame_cnt
#    time.sleep(0.1)
    try:
        if int(pkt.layers[2].srcport) == 502 or int(pkt.layers[2].dstport) == 502:
#            modbus_data.append((frame_cnt, str(pkt.layers[4].data), int(pkt.layers[3].len)-2))
            frame.append(frame_cnt)
            length.append(int(pkt.layers[3].len)-2)
#    except IndexError as e:
#        pass
    except:
#        print sys.exc_info()[0]
        pass

class extractor():
    def __init__(self):
        pass
    def extract_from_pcap(self, captureFile):
        cap = pyshark.FileCapture(captureFile)
        cap.apply_on_packets(get_modbus_pkts, timeout=1000)

        trace = go.Scatter(
            x = frame,
            y = length,
            mode = 'markers'
        )
        data = [trace]
        py.plot(data, filename='basic-line')

def main():
    if len(sys.argv) < 2:
        print "Usage: python traffic.py capturefile"
        sys.exit()
    else:
        captureFile = str(os.path.abspath(sys.argv[1]))
        ext = extractor()
        ext.extract_from_pcap(captureFile) 
        


if __name__ == '__main__':
    main()
