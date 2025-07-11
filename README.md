# flipper-hisense-ac-unit

A side project to create a Flipper Zero IR remote for a Hisense AC unit.

The Hisense AC unit's remote is stateful. It has it's own notion of what state the AC unit should be in, and every time a button is pressed the entire desired state is transmitted to the AC unit.

This makes it interesting. While the raw IR capture capability of the Flipper allows retransmitting a captured state, this does not allow you to set individual parameters like temperature, mode, fan speed.

Currently in an initial research phase. I have captured raw IR data and am working to decode it.
