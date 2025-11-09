#!/usr/bin/env python3
"""
Simple test script for generate_random_data_by_service.py
This demonstrates the usage without requiring a full ROS2 environment.
"""

print("""
=============================================================================
ROS2 Service Random Data Generator - Usage Examples
=============================================================================

This tool generates random data conforming to a ROS2 service request format.

INSTALLATION:
-------------
Make sure you have the required dependencies installed:
    pip install hypothesis numpy

BASIC USAGE:
-----------

1. Generate one random example (default):
   python3 -m ros2_fuzzer.generate_random_data_by_service example_interfaces/AddTwoInts

2. Generate multiple examples:
   python3 -m ros2_fuzzer.generate_random_data_by_service example_interfaces/AddTwoInts -n 5

3. Output as JSON format:
   python3 -m ros2_fuzzer.generate_random_data_by_service example_interfaces/AddTwoInts -f json

4. Output as compact JSON (single line):
   python3 -m ros2_fuzzer.generate_random_data_by_service example_interfaces/AddTwoInts -f compact

5. Use a seed for reproducible results:
   python3 -m ros2_fuzzer.generate_random_data_by_service example_interfaces/AddTwoInts -s 42

6. Combine options:
   python3 -m ros2_fuzzer.generate_random_data_by_service example_interfaces/AddTwoInts -n 3 -f json -s 42

COMMAND-LINE OPTIONS:
--------------------
  service_type          ROS2 service type (e.g., "example_interfaces/AddTwoInts")
  -n, --num-examples    Number of random examples to generate (default: 1)
  -f, --format          Output format: pretty, json, or compact (default: pretty)
  -s, --seed            Random seed for reproducible generation (optional)
  -h, --help            Show help message

EXAMPLES WITH DIFFERENT SERVICE TYPES:
-------------------------------------

# Simple service with integer inputs:
python3 -m ros2_fuzzer.generate_random_data_by_service example_interfaces/AddTwoInts

# Service with string input:
python3 -m ros2_fuzzer.generate_random_data_by_service example_interfaces/SetBool

# Complex service with nested messages:
python3 -m ros2_fuzzer.generate_random_data_by_service geometry_msgs/SetPose

OUTPUT FORMATS:
--------------

1. PRETTY format (default) - Human-readable with indentation:
   a: 12345
   b: -67890

2. JSON format - Formatted JSON for parsing:
   {
     "a": 12345,
     "b": -67890
   }

3. COMPACT format - Single-line JSON:
   {"a": 12345, "b": -67890}

USE CASES:
---------
- Testing service handlers with random inputs
- Exploring the structure of service request messages
- Generating test data for fuzzing
- Creating example payloads for documentation
- Debugging service interfaces

=============================================================================
""")
