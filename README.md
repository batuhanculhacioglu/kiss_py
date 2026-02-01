# Keep It Simple Stupid (KISS) Protocol Functions
![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)
![Python](https://img.shields.io/badge/Python-3.x-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-Cross--Platform-green.svg)

---

## 👨‍💻 Author & Contact

**Batuhan Çulhacıoğlu**

* 📧 **Email:** [batuhanculhacioglu@gmail.com](mailto:batuhanculhacioglu@gmail.com)
* 🐙 **GitHub:** [@batuhanculhacioglu](https://github.com/batuhanculhacioglu)
* 💼 **LinkedIn:** [in/batuhanculhacioglu](https://www.linkedin.com/in/batuhanculhacioglu)

---

## Overview

This module provides a pure Python implementation of the **KISS (Keep It Simple Stupid)** framing protocol. It is designed to be lightweight, dependency-free, and robust, making it ideal for serial communication, amateur radio packet framing, and embedded systems interfacing.

The library handles the low-level "byte stuffing" (escaping) required to transmit binary data transparently over a stream-based medium.



## Features

* **Zero Dependencies:** Relies solely on the Python standard library.
* **Type Hinting:** Fully typed for modern Python development and IDE support.
* **Robust Error Handling:** The `kiss_decode` function detects malformed packets and returns `None` instead of crashing or yielding corrupt data.
* **Standard Compliant:** Correctly implements the SLIP/KISS escape sequences (`FEND`, `FESC`).

## Installation

This library is designed as a standalone module. To use it, simply copy the `kiss.py` file into your project directory or submodule folder.

**File Structure:**
```text
my_project/
├── main.py
├── ...
└── kiss.py  <-- The protocol file

```

## Usage

### 1. Importing the Library

```python
from kiss import kiss_encode, kiss_decode

```

### 2. Encoding Data

Wraps raw bytes into a KISS frame. It automatically handles "byte stuffing" if reserved characters appear in the payload.

```python
payload = b'Hello KISS'

# Encode the packet
encoded_frame = kiss_encode(payload)

print(f"Raw: {list(payload)}")
# Output: [72, 101, 108, 108, 111, 32, 75, 73, 83, 83]

print(f"Encoded: {[hex(b) for b in encoded_frame]}")
# Output: ['0xc0', '0x48', ..., '0xc0']
# Note: 0xC0 (FEND) is added to the start and end.

```

### 3. Decoding Data

Parses a received frame, strips the `FEND` delimiters, and reverses the escape sequences to restore the original data.

```python
# A received frame (Must start and end with 0xC0)
received_frame = b'\xC0Hello KISS\xC0'

decoded_data = kiss_decode(received_frame)

if decoded_data:
    print(f"Decoded Data: {decoded_data}")
else:
    print("Error: Invalid frame structure.")

```

### 4. Handling Special Characters (Escaping)

If your data contains the reserved `FEND` (0xC0) or `FESC` (0xDB) bytes, the library automatically escapes them to ensure frame integrity.

```python
# Payload containing a reserved FEND byte
tricky_data = b'\x01\xC0\x02' 

encoded = kiss_encode(tricky_data)

# The internal 0xC0 is escaped to 0xDB 0xDC
print([hex(b) for b in encoded])
# Result: ['0xc0', '0x1', '0xdb', '0xdc', '0x2', '0xc0']

```

## Protocol Logic

The KISS protocol uses specific byte sequences to distinguish between data and control commands.

| Special Byte | Hex | Description | Encoded As |
| --- | --- | --- | --- |
| **FEND** | `0xC0` | Frame End/Start | `FESC` + `TFEND` (`0xDB`, `0xDC`) |
| **FESC** | `0xDB` | Frame Escape | `FESC` + `TFESC` (`0xDB`, `0xDD`) |

### Error Conditions

The `kiss_decode` function will return `None` (indicating failure) if:

1. The frame length is less than 2 bytes.
2. The frame does not start and end with `FEND` (`0xC0`).
3. An invalid escape sequence is encountered (e.g., `0xDB` followed by a random byte).
4. The frame ends with a dangling `FESC` byte.


---

## License

Keep It Simple Stupid (KISS) Protocol Functions

Copyright (C) 2026 Batuhan Çulhacıoğlu


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