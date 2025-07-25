import sys
import os
import random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'GUI')))
from settings.utils import get_ini_path
from PyQt5.QtCore import QSettings

def get_encryption_method():
    settings = QSettings(get_ini_path(), QSettings.IniFormat)
    return settings.value('obfuscation/encryption_method', 1, int)

def encrypt_offset(real_offset, method=1):
    if method == 1:
        # Basic XOR (original method)
        key = random.randint(0x11, 0xFF)
        encrypted_offset = real_offset ^ key
        return encrypted_offset, {"key": key}
    elif method == 2:
        # Multi-key XOR (two keys applied sequentially)
        key1 = random.randint(0x11, 0xFF)
        key2 = random.randint(0x11, 0xFF)
        encrypted_offset = (real_offset ^ key1) ^ key2
        return encrypted_offset, {"key1": key1, "key2": key2}
    elif method == 3:
        # Add + XOR combination
        add_val = random.randint(0x100, 0xFFF)
        xor_key = random.randint(0x11, 0xFF)
        encrypted_offset = (real_offset + add_val) ^ xor_key
        return encrypted_offset, {"add_val": add_val, "xor_key": xor_key}
    elif method == 4:
        # Enhanced XOR (Strong) - Uses a larger key range for better obfuscation
        xor_key = random.randint(0x1000, 0xFFFF)  # Use a larger key range
        encrypted_offset = real_offset ^ xor_key
        return encrypted_offset, {"xor_key": xor_key}
    elif method == 5:
        # Offset Shifting (Strong) - Simple addition to mask the real offset
        mask = random.randint(0x100, 0xFFF)
        encrypted_offset = (real_offset + mask) & 0xFFFFFFFF
        return encrypted_offset, {"mask": mask}
    # Default to basic XOR if invalid method
    key = random.randint(0x11, 0xFF)
    encrypted_offset = real_offset ^ key
    return encrypted_offset, {"key": key}

def generate_decryption_sequence(offset_name, encryption_data, method=1):
    if method == 1:
        # Basic XOR (original method)
        return [
            f"    mov eax, dword ptr [{offset_name}]\n",
            f"    mov ebx, 0{encryption_data['key']:X}h\n",
            f"    xor eax, ebx\n"
        ]
    elif method == 2:
        # Multi-key XOR (two keys applied sequentially)
        return [
            f"    mov eax, dword ptr [{offset_name}]\n",
            f"    mov ebx, 0{encryption_data['key1']:X}h\n",
            f"    xor eax, ebx\n",
            f"    mov ebx, 0{encryption_data['key2']:X}h\n",
            f"    xor eax, ebx\n"
        ]
    elif method == 3:
        # Add + XOR combination
        return [
            f"    mov eax, dword ptr [{offset_name}]\n",
            f"    mov ebx, 0{encryption_data['xor_key']:X}h\n",
            f"    xor eax, ebx\n",
            f"    sub eax, 0{encryption_data['add_val']:X}h\n"
        ]
    elif method == 4:
        # Enhanced XOR (Strong) - Uses a larger key range for better obfuscation
        xor_key = encryption_data['xor_key']
        return [
            f"    mov eax, dword ptr [{offset_name}]\n",
            f"    mov ebx, 0{xor_key:X}h\n",
            f"    xor eax, ebx\n"
        ]
    elif method == 5:
        # Offset Shifting (Strong) - Simple subtraction to recover the real offset
        mask = encryption_data['mask']
        return [
            f"    mov eax, dword ptr [{offset_name}]\n",
            f"    sub eax, 0{mask:X}h\n"
        ]
    # Default to basic XOR if invalid method
    return [
        f"    mov eax, dword ptr [{offset_name}]\n",
        f"    mov ebx, 0{encryption_data['key']:X}h\n",
        f"    xor eax, ebx\n"
    ] 
