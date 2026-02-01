"""
Keep It Simple Stupid (KISS) Protocol Functions

Copyright (C) 2026 Batuhan Çulhacıoğlu

Author: Batuhan Çulhacıoğlu
Email: batuhanculhacioglu@gmail.com
GitHub: https://github.com/batuhanculhacioglu
LinkedIn: https://www.linkedin.com/in/batuhanculhacioglu

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

FEND = 0xC0
FESC = 0xDB
TFEND = 0xDC
TFESC = 0xDD

"""
KISS Encoding Rules:

One
FEND -> FESC TFEND
0xC0 -> 0xDB 0xDC

Two
FESC -> FESC TFESC
0xDB -> 0xDB 0xDD
"""

def kiss_encode(data: bytes) -> bytes:
    """Encodes data using KISS protocol.

    Args:
        data (bytes): The raw data to be encoded.

    Returns:
        bytes: The KISS encoded data.
    """
    encoded = bytearray()
    encoded.append(FEND)

    for byte in data:
        if byte == FEND:
            encoded.append(FESC)
            encoded.append(TFEND)
        elif byte == FESC:
            encoded.append(FESC)
            encoded.append(TFESC)
        else:
            encoded.append(byte)

    encoded.append(FEND)
    return bytes(encoded)

def kiss_decode(data: bytes) -> bytes | None:
    """Decodes KISS encoded data.
    
    Args:
        data (bytes): The KISS encoded data.

    Returns:
        bytes | None: The decoded raw data, or None if the frame is invalid.
    """
    if len(data) < 2 or data[0] != FEND or data[-1] != FEND:
        return None

    decoded = bytearray()
    is_fesc = False

    for byte in data[1:-1]:
        if is_fesc:
            if byte == TFEND:
                decoded.append(FEND)
            elif byte == TFESC:
                decoded.append(FESC)
            else:
                return None
            is_fesc = False
        elif byte == FESC:
            is_fesc = True
        else:
            decoded.append(byte)

    if is_fesc:
        return None

    return bytes(decoded)

            

            