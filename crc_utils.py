def crc16_ccitt(data: bytes, poly=0x1021, init_value=0x0) -> int:
    """
    Calculate CRC-16-CCITT using the polynomial 0x1021.
    
    :param data: Data to calculate CRC over
    :param poly: CRC polynomial
    :param init_value: Initialization value
    :return: Calculated CRC value
    """
    crc = init_value
    for byte in data:
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ poly
            else:
                crc <<= 1
            crc &= 0xFFFF  # Keep CRC within 16 bits
    return crc

def calculate_crc(data: bytes) -> bytes:
    """
    Calculate CRC for given data and return it as 2 bytes.
    
    :param data: Data to calculate CRC over
    :return: CRC as 2-byte representation
    """
    crc_value = crc16_ccitt(data)
    return crc_value.to_bytes(2, byteorder='big')
