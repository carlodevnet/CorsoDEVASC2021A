# Overview

This check connects to all devices defined in the testbed, and parses are interface counters
if an interface has CRC errors, the test case fails. 

## Running

```
# to start with the test use:
pyats run job job.py --testbed-file ../default_testbed.yaml

```