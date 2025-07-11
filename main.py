from captures import raw_61deg, raw_66deg, raw_70deg

HISENSE_BIT_MARK = 520
HISENSE_BIT_ZERO_SPACE = 630
HISENSE_BIT_ONE_SPACE = 1700

HISENSE_LEADING_MARK = 9060
HISENSE_LEADING_SPACE = 4550
HISENSE_PACKET_GAP = 8140

ENCODED_BIT_LEN = 2
ENCODED_BYTE_LEN = ENCODED_BIT_LEN * 8
ENCODED_MSG_LEN = 343

DECODE_JITTER = 200

class BitDecodeError(Exception):
    """Raised when decoding a bit fails."""
    pass

def encode_bit(bit):
    """Pulse duration encode a single bit."""
    if bit:
        return (HISENSE_BIT_MARK, HISENSE_BIT_ONE_SPACE)
    else:
        return (HISENSE_BIT_MARK, HISENSE_BIT_ZERO_SPACE)

def encode_byte(byte):
    """Pulse duration encode a byte, least significant bit first."""
    return [
        bit_part
        for bit_num in range(7)
        for bit_part in encode_bit(byte & (1 << bit_num))
    ]

def decode_bit(encoded_bit):
    """Pulse duration decode a bit, accepting a fixed amount of jitter."""
    assert len(encoded_bit) == ENCODED_BIT_LEN 

    bit_mark, bit_space = encoded_bit

    def jitter(value):
        return range(value - DECODE_JITTER, value + DECODE_JITTER)

    if bit_mark not in jitter(HISENSE_BIT_MARK):
        raise BitDecodeError("invalid bit mark duration")

    if bit_space in jitter(HISENSE_BIT_ZERO_SPACE):
        return 0

    if bit_space in jitter(HISENSE_BIT_ONE_SPACE):
        return 1

    raise BitDecodeError("invalid bit space duration")

def decode_byte(encoded_byte):
    """Pulse duration decode a byte, least significant bit first."""
    assert len(encoded_byte) == ENCODED_BYTE_LEN

    bits = (
        decode_bit(encoded_byte[n:n+ENCODED_BIT_LEN])
        for n in range(0, ENCODED_BYTE_LEN, ENCODED_BIT_LEN)
    )

    byte = 0
    for (shift, bit) in enumerate(bits):
        byte |= (bit << shift)
    return byte

def decode_packet(encoded_packet):
    """Pulse duration decode a packet, returning a list of bytes."""
    assert len(encoded_packet) % ENCODED_BYTE_LEN == 0

    return [
        decode_byte(encoded_packet[n:n+ENCODED_BYTE_LEN])
        for n in range(0, len(encoded_packet), ENCODED_BYTE_LEN)
    ]

def chunk_raw(raw_data):
    """Chunk raw data into parts."""
    assert len(raw_data) == ENCODED_MSG_LEN

    def interpret(chunk):
        match chunk["type"]:
            case "packet":
                return interpret_packet(chunk)
            case _:
                return chunk

    def interpret_packet(chunk):
        assert chunk["type"] == "packet"

        packet_bytes = decode_packet(chunk["raw"])

        chunk["packet_bytes"] = packet_bytes
        chunk["packet_bits"] = [format_byte(byte) for byte in packet_bytes]

        match chunk["packet_num"]:
            case 0:
                temp_celsius_addend = (packet_bytes[3] & 0b11110000) >> 4
                temp_celsius = 16 + temp_celsius_addend
                chunk["packet_data"] = {
                    "mode": packet_bytes[3] & 0b00000011,
                    "temp_celsius_addend": temp_celsius_addend,
                    "temp_celsius": temp_celsius,
                    "temp_fahrenheit": round(temp_celsius * 9/5 + 32),
                }

            case 1:
                chunk["packet_data"] = {
                    "checksum": packet_bytes[7],
                }

        return chunk

    return [interpret(chunk) for chunk in [
        { "type": "header", "raw": raw_data[0:2] },
        { "type": "packet", "raw": raw_data[2:98], "packet_num": 0 },
        { "type": "packet_stop", "raw": raw_data[98:99] },
        { "type": "packet_gap", "raw": raw_data[99:100] },
        { "type": "packet", "raw": raw_data[100:228], "packet_num": 1 },
        { "type": "packet_stop", "raw": raw_data[228:229] },
        { "type": "packet_gap", "raw": raw_data[229:230] },
        { "type": "packet", "raw": raw_data[230:342], "packet_num": 2 },
        { "type": "packet_stop", "raw": raw_data[342:343] },
    ]]

def checksum(bytes):
    """Compute an XOR checksum over the given bytes."""
    sum = 0
    for byte in bytes:
        sum ^= byte
    return sum

def format_byte(byte):
    """Return a byte as a zero-padded binary string."""
    return format(byte, "#010b")

if __name__ == "__main__":
    import pprint

    print("=== Chunks ===")
    chunks = chunk_raw(raw_61deg)
    pprint.pp(chunks, compact=True)
    print()

    print("=== Data ===")
    data = {}
    for chunk in chunks:
        data.update(chunk.get("packet_data", {}))
    pprint.pp(data, compact=True)
    print()
