import struct
import types

class FileLikeError(Exception): pass
class BitstreamError(Exception): pass

class WebPSegment(types.SimpleNamespace):
    """
    A segment is part of the WebP bitstream, a segment contains
    information related to the bitstream, sometimes essential and
    sometimes ancillary. Name of a chunk is restricted to only 4
    bytes, names consisting English letters or spaces is preffered.

    The data payload has no-restrictions at all until it is restricted
    to the unit of octets which a computer can store in the RAM or disk.
    """
    def __init__(self, name, data=b''):
        self.name = bytes(name)[:4]
        self.data = bytes(data)
        self.size = len(data)

class WebPParser(struct.Struct):
    """
    Given a readable stream, this object reads IFF chunks from the
    stream and yields an iterator of `WebPSegment`s.

    ```
    in_ = open('rat.webp', 'rb')
    wp = WebPParser(in_)

    for seg in wp:
        print(seg.name)
    ```
    """
    def __init__(self, fs):
        super().__init__('<4sI')

        if not hasattr(fs, 'read') or fs.read(0) != b'':
            raise FileLikeError('file is unreadable or does not yield bytes')
        self.fs = fs

        magic = fs.read(12)
        if not (magic[:4] == b'RIFF' and magic[8:12] == b'WEBP'):
            raise BitstreamError('WebP magic code did not match')
        
    def __iter__(self):
        while True:
            try:
                chunk = self.unpack(self.fs.read(8))
            except struct.error:
                break

            yield WebPSegment(chunk[0], self.fs.read(chunk[1]))

class WebPUnparser(struct.Struct):
    """
    Given a writable and seekable stream, this object writes IFF chunk
    data into the stream and updates its size as data is recieved.

    ```py
    out = open('rat.webp', 'wb')
    wu = WebPUnparser(out)
    data_payload = b"Hello World"

    wu << WebPSegment(b'NSWC', len(data_payload), data_payload)
    ```
    """
    def __init__(self, fs):
        super().__init__('<4sI')

        if not hasattr(fs, 'write') or not hasattr(fs, 'tell') or not hasattr(fs, 'seek'):
            raise FileLikeError('file is unwritable/unseekable')
        self.fs = fs

        # write out the magic code, except keep the size
        # field inaccurate for reasons.
        fs.write(b'RIFF' + b'\x04\x00\x00\x00' + b'WEBP')

        self._size = 4 # inital size is always 4.

    def update_iff_size(self):
        previous_position = self.fs.tell()

        self.fs.seek(4)
        self.fs.write(struct.pack('<I', self._size))
        self.fs.seek(previous_position)

    def __lshift__(self, chunk):
        if not isinstance(chunk, WebPSegment):
            raise TypeError('not a WebP segment')

        self.fs.write(self.pack(chunk.name, chunk.size) + chunk.data)
        
        self._size+= chunk.size + 8
        self.update_iff_size()
