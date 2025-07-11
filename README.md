# flipper-hisense-ac-unit

A side project to create a Flipper Zero IR remote for a Hisense AC unit.

The Hisense AC unit's remote is stateful. It has it's own notion of what state the AC unit should be in, and every time a button is pressed the entire desired state is transmitted to the AC unit.

This makes it interesting. While the raw IR capture capability of the Flipper allows retransmitting a captured state, this does not allow you to set individual parameters like temperature, mode, fan speed.

Currently in an initial research phase. I have captured raw IR data and am working to decode it.

## Example

```console
% python3 main.py
=== Chunks ===
[{'type': 'header', 'raw': [8998, 4469]},
 {'type': 'packet',
  'raw': [567, 1703, 534, 1712, 535, 565, 548, 532, 571, 537, 566, 545, 568,
          544, 569, 1680, 567, 551, 541, 1705, 542, 1708, 539, 537, 576, 536,
          567, 542, 571, 542, 571, 531, 572, 521, 571, 525, 567, 532, 571, 533,
          570, 537, 566, 544, 569, 544, 569, 533, 570, 523, 569, 1674, 563, 537,
          576, 531, 572, 534, 569, 541, 572, 541, 572, 530, 573, 520, 572, 524,
          568, 531, 572, 532, 571, 536, 567, 543, 570, 543, 570, 532, 571, 522,
          570, 526, 566, 533, 570, 534, 569, 538, 565, 545, 568, 545, 568,
          521],
  'packet_num': 0,
  'packet_bytes': [131, 6, 0, 2, 0, 0],
  'packet_bits': ['0b10000011', '0b00000110', '0b00000000', '0b00000010',
                  '0b00000000', '0b00000000'],
  'packet_data': {'mode': 2,
                  'temp_celsius_addend': 0,
                  'temp_celsius': 16,
                  'temp_fahrenheit': 61}},
 {'type': 'packet_stop', 'raw': [571]}, {'type': 'packet_gap', 'raw': [7965]},
 {'type': 'packet',
  'raw': [568, 552, 540, 557, 546, 533, 570, 532, 571, 535, 568, 542, 571, 1690,
          568, 1710, 538, 555, 548, 528, 564, 534, 569, 533, 570, 537, 566, 545,
          568, 545, 568, 534, 569, 524, 568, 528, 564, 535, 568, 535, 568, 539,
          564, 546, 567, 546, 567, 535, 568, 525, 567, 529, 563, 536, 567, 536,
          567, 540, 563, 547, 566, 548, 565, 536, 567, 526, 566, 530, 573, 527,
          565, 538, 565, 542, 571, 539, 564, 550, 563, 538, 565, 528, 564, 532,
          571, 529, 563, 540, 563, 543, 570, 540, 573, 541, 572, 529, 563, 530,
          562, 534, 569, 531, 572, 531, 572, 535, 568, 542, 571, 543, 570, 532,
          571, 521, 571, 1698, 539, 535, 568, 540, 563, 541, 572, 538, 565,
          1722, 536, 1704],
  'packet_num': 1,
  'packet_bytes': [192, 0, 0, 0, 0, 0, 0, 194],
  'packet_bits': ['0b11000000', '0b00000000', '0b00000000', '0b00000000',
                  '0b00000000', '0b00000000', '0b00000000', '0b11000010'],
  'packet_data': {'checksum': 194}},
 {'type': 'packet_stop', 'raw': [543]}, {'type': 'packet_gap', 'raw': [7970]},
 {'type': 'packet',
  'raw': [563, 557, 535, 562, 541, 537, 566, 537, 566, 540, 563, 547, 566, 548,
          565, 536, 567, 526, 566, 1677, 570, 530, 573, 535, 568, 536, 567, 544,
          569, 545, 568, 534, 569, 524, 568, 527, 565, 535, 568, 535, 568, 539,
          564, 547, 566, 547, 566, 536, 567, 526, 566, 530, 562, 537, 566, 537,
          566, 541, 572, 538, 565, 549, 564, 538, 565, 528, 564, 532, 571, 528,
          564, 1712, 535, 546, 567, 548, 565, 545, 568, 535, 568, 526, 566, 529,
          563, 536, 567, 537, 566, 541, 572, 538, 565, 549, 564, 537, 566, 527,
          565, 1704, 543, 530, 573, 1706, 541, 540, 573, 542, 571, 539, 564,
          527],
  'packet_num': 2,
  'packet_bytes': [0, 2, 0, 0, 8, 0, 10],
  'packet_bits': ['0b00000000', '0b00000010', '0b00000000', '0b00000000',
                  '0b00001000', '0b00000000', '0b00001010']},
 {'type': 'packet_stop', 'raw': [565]}]

=== Data ===
{'mode': 2,
 'temp_celsius_addend': 0,
 'temp_celsius': 16,
 'temp_fahrenheit': 61,
 'checksum': 194}
```
