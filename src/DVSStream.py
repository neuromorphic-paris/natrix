import numpy as np
import os
from .EventStream import EventStream
from .config import VERSION, TYPE

DVStype = [('x', np.uint16), ('y', np.uint16),
           ('is_increase', np.bool_), ('ts', np.uint64)]


class DVSStream(EventStream):
    """
    """
    def __init__(self, _width, _height, _events, _version=VERSION):
        super().__init__(_events, DVStype, _version)
        self.width = np.uint16(_width)
        self.height = np.uint16(_height)

    def read(event_data, version):
        width = (event_data[17] << 8) + event_data[16]
        height = (event_data[19] << 8) + event_data[18]
        file_cursor = 20
        end = len(event_data)
        events = []
        current_time = 0
        while(file_cursor < end):
            byte = event_data[file_cursor]
            if byte & 0xfe == 0xfe:
                if byte == 0xfe:  # Reset event
                    pass
                else:  # Overflow event
                    current_time += 127
            else:
                file_cursor += 1
                byte1 = event_data[file_cursor]
                file_cursor += 1
                byte2 = event_data[file_cursor]
                file_cursor += 1
                byte3 = event_data[file_cursor]
                file_cursor += 1
                byte4 = event_data[file_cursor]
                current_time += (byte >> 1)
                x = ((byte2 << 8) | byte1)
                y = ((byte4 << 8) | byte3)
                is_increase = (byte & 0x01)
                events.append((x, y, is_increase, current_time))
            file_cursor += 1
        return DVSStream(width, height, events, version)

    def write(self, filename):
        """
        """
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        to_write = bytearray('Event Stream', 'ascii')
        to_write.append(int(self.version.split('.')[0]))
        to_write.append(int(self.version.split('.')[1]))
        to_write.append(int(self.version.split('.')[2]))
        to_write.append(TYPE['DVS'])
        to_write.append(np.uint8(self.width))
        to_write.append(np.uint8(self.width >> 8))
        to_write.append(np.uint8(self.height))
        to_write.append(np.uint8(self.height >> 8))
        previous_ts = 0
        for datum in self.data:
            relative_ts = datum.ts - previous_ts
            if relative_ts >= 127:
                number_of_overflows = int(relative_ts / 127)
                for i in range(number_of_overflows):
                    to_write.append(0xff)
                relative_ts -= number_of_overflows * 127
            to_write.append(np.uint8((np.uint8(relative_ts) << 1)
                            | (datum.is_increase & 0x01)))
            to_write.append(np.uint8(datum.x))
            to_write.append(np.uint8(datum.x >> 8))
            to_write.append(np.uint8(datum.y))
            to_write.append(np.uint8(datum.y >> 8))
            previous_ts = datum.ts
        file = open(filename, 'wb')
        file.write(to_write)
        file.close()
