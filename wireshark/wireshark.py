import pyshark


capture = pyshark.LiveCapture(interface='Wi-Fi')
capture.sniff(timeout=50)
print(capture)
print(capture[3])

for packet in capture.sniff_continuously(packet_count=5):
    print('Just arrived:', packet)
