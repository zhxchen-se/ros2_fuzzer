"""
ROS2 Topic Random Data Generator.

This module provides functionality to generate random data that conforms to a given ROS2 topic message format.
Can be used as a standalone command-line tool to inspect generated test data.

:authors: Alias Robotics S.L. Borja Erice, Odei Olalde, Xabi Perez, Gorka Olalde
"""
import logging
import json
from argparse import ArgumentParser
from hypothesis import given, settings, Verbosity, Phase
from ros2_fuzzer.ros_commons import ros_interface_loader_str, map_ros_types


def ros_msg_to_dict(msg):
    """
    Convert a ROS2 message instance to a dictionary for JSON serialization.
    
    :param msg: ROS2 message instance
    :return: Dictionary representation of the message
    """
    import numpy as np
    import array
    result = {}
    slot_types = msg.get_fields_and_field_types()
    
    for field_name in slot_types.keys():
        value = getattr(msg, field_name)
        
        # Handle nested messages
        if hasattr(value, 'get_fields_and_field_types'):
            result[field_name] = ros_msg_to_dict(value)
        # Handle numpy arrays
        elif isinstance(value, np.ndarray):
            result[field_name] = value.tolist()
        # Handle array.array (used for uint8[], etc.)
        elif isinstance(value, array.array):
            result[field_name] = value.tolist()
        # Handle lists/arrays
        elif isinstance(value, list):
            if value and hasattr(value[0], 'get_fields_and_field_types'):
                # List of nested messages
                result[field_name] = [ros_msg_to_dict(item) for item in value]
            else:
                # List of basic types
                result[field_name] = value
        # Handle bytes
        elif isinstance(value, bytes):
            result[field_name] = value.hex()
        # Handle numpy scalar types
        elif hasattr(value, 'item'):
            result[field_name] = value.item()
        # Basic types
        else:
            result[field_name] = value
    
    return result


def generate_random_message_data(msg_type, num_examples=1, seed=None, skip_simple=False):
    """
    Generate random data conforming to a ROS2 message format.
    
    :param msg_type: The ROS2 message type class
    :param num_examples: Number of random examples to generate
    :param seed: Random seed for reproducibility (optional)
    :param skip_simple: If True, generate more examples and skip the simple ones (optional)
    :return: List of generated message instances
    """
    generated_data = []
    
    # Hypothesis generates simple examples first (like 0, empty strings)
    # then progresses to more complex/random values
    # If skip_simple is True, we generate extra examples and skip the initial simple ones
    actual_examples = num_examples
    skip_count = 0
    
    if skip_simple:
        # Generate extra examples to skip the simple ones
        # Hypothesis typically generates simple values in the first 10-20 examples
        skip_count = max(10, num_examples)  # Skip first ~10 simple examples
        actual_examples = num_examples + skip_count
    
    # Configure hypothesis settings
    settings_kwargs = {
        'max_examples': actual_examples,
        'verbosity': Verbosity.quiet,
        'phases': [Phase.generate],  # Only generate, don't shrink
        'print_blob': False,
        'database': None,  # Don't use example database for more randomness
    }
    
    if seed is not None:
        settings_kwargs['derandomize'] = True
        import random
        random.seed(seed)
    
    @settings(**settings_kwargs)
    @given(msg=map_ros_types(msg_type))
    def collect_data(msg):
        generated_data.append(msg)
    
    # Run the generation
    collect_data()
    
    # Skip simple examples if requested
    if skip_simple:
        return generated_data[skip_count:]
    
    return generated_data


def print_message(msg, output_format='pretty', index=None):
    """
    Print a message in the specified format.
    
    :param msg: The message instance
    :param output_format: Output format ('pretty', 'json', or 'compact')
    :param index: Optional index number for the example
    """
    if output_format == 'json':
        data_dict = ros_msg_to_dict(msg)
        print(json.dumps(data_dict, indent=2))
    elif output_format == 'compact':
        data_dict = ros_msg_to_dict(msg)
        print(json.dumps(data_dict))
    else:  # pretty format
        if index is not None:
            print(f"\n{'='*60}")
            print(f"Example #{index + 1}")
            print('='*60)
        
        print_message_pretty(msg, indent=0)


def print_message_pretty(msg, indent=0):
    """
    Pretty print a ROS2 message with proper indentation.
    
    :param msg: ROS2 message instance
    :param indent: Current indentation level
    """
    slot_types = msg.get_fields_and_field_types()
    indent_str = "  " * indent
    
    for field_name, field_type in slot_types.items():
        value = getattr(msg, field_name)
        
        # Handle nested messages
        if hasattr(value, 'get_fields_and_field_types'):
            print(f"{indent_str}{field_name} ({field_type}):")
            print_message_pretty(value, indent + 1)
        # Handle lists/arrays
        elif isinstance(value, list):
            if not value:
                print(f"{indent_str}{field_name}: []")
            elif value and hasattr(value[0], 'get_fields_and_field_types'):
                # List of nested messages
                print(f"{indent_str}{field_name} ({field_type}): [")
                for i, item in enumerate(value):
                    print(f"{indent_str}  [{i}]:")
                    print_message_pretty(item, indent + 2)
                print(f"{indent_str}]")
            else:
                # List of basic types
                if len(value) <= 10:
                    print(f"{indent_str}{field_name}: {value}")
                else:
                    print(f"{indent_str}{field_name}: [{value[0]}, {value[1]}, ..., {value[-1]}] (length: {len(value)})")
        # Handle bytes
        elif isinstance(value, bytes):
            if len(value) <= 20:
                print(f"{indent_str}{field_name}: {value.hex()}")
            else:
                print(f"{indent_str}{field_name}: {value[:10].hex()}... (length: {len(value)} bytes)")
        # Basic types
        else:
            print(f"{indent_str}{field_name}: {value}")


def main():
    """
    Main entry point for the command-line tool.
    Generates and prints random data for a given ROS2 message type.
    """
    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger(__name__)
    
    parser = ArgumentParser(
        description='Generate random data conforming to a ROS2 topic message format',
        epilog='Example: python -m ros2_fuzzer.generate_random_data_by_topic std_msgs/String'
    )
    
    parser.add_argument(
        'message_type',
        help='ROS2 message type. Supports both formats: "package/Type" or "package/msg/Type" (from ros2 topic list -t)'
    )
    
    parser.add_argument(
        '-n', '--num-examples',
        type=int,
        default=1,
        help='Number of random examples to generate (default: 1)'
    )
    
    parser.add_argument(
        '-f', '--format',
        choices=['pretty', 'json', 'compact'],
        default='pretty',
        help='Output format: pretty (human-readable), json (formatted JSON), or compact (single-line JSON)'
    )
    
    parser.add_argument(
        '-s', '--seed',
        type=int,
        default=None,
        help='Random seed for reproducible generation (optional)'
    )
    
    parser.add_argument(
        '--random',
        action='store_true',
        help='Skip simple examples (0, empty strings) and generate more random values'
    )
    
    args = parser.parse_args()
    
    try:
        # Load the message type
        logger.info(f"Loading message type: {args.message_type}")
        msg_type = ros_interface_loader_str(args.message_type, 'message')
        
        # Generate random data
        logger.info(f"Generating {args.num_examples} random example(s)...")
        generated_messages = generate_random_message_data(
            msg_type,
            num_examples=args.num_examples,
            seed=args.seed,
            skip_simple=args.random
        )
        
        # Print the generated data
        if args.format == 'pretty' and args.num_examples > 1:
            print(f"\nGenerated {len(generated_messages)} random message(s) for: {args.message_type}")
        
        for i, message in enumerate(generated_messages):
            print_message(
                message,
                output_format=args.format,
                index=i if args.format == 'pretty' and args.num_examples > 1 else None
            )
            
            # Add separator between JSON outputs if multiple examples
            if args.format in ['json', 'compact'] and i < len(generated_messages) - 1:
                print()
        
        if args.format == 'pretty':
            print()
            
    except ImportError as e:
        logger.error(f"Failed to load message type '{args.message_type}': {e}")
        print(f"Error: Could not load message type '{args.message_type}'")
        print("Make sure the package is installed and sourced.")
        return 1
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
