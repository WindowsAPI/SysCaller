import random
import string
import os
import re
try:
    from PyQt5.QtCore import QSettings
except ImportError:
    class QSettings:
        def __init__(self, *args):
            self.settings = {}
        def value(self, key, default, type):
            return default

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def generate_random_name(used_names):
    settings = QSettings('SysCaller', 'BuildTools')
    prefix_length = settings.value('obfuscation/syscall_prefix_length', 8, type=int)
    number_length = settings.value('obfuscation/syscall_number_length', 6, type=int)
    while True:
        prefix = generate_random_string(prefix_length)
        number = str(random.randint(10**(number_length-1), (10**number_length)-1))
        name = f'{prefix}_{number}'
        if name not in used_names:
            used_names.add(name)
            return name

def generate_random_offset_name(used_names):
    settings = QSettings('SysCaller', 'BuildTools')
    name_length = settings.value('obfuscation/offset_name_length', 8, type=int)
    while True:
        name = generate_random_string(name_length)
        if name not in used_names:
            used_names.add(name)
            return name

def generate_random_offset(used_offsets):
    while True:
        offset = random.randint(0x1000, 0xFFFF)
        if offset not in used_offsets:
            used_offsets.add(offset)
            return offset

def extract_syscall_offset(line):
    offset_part = line.split('mov eax,')[1].split(';')[0].strip()
    return int(offset_part[:-1], 16)

def generate_masked_sequence(offset_name, encryption_key=None):
    settings = QSettings('SysCaller', 'BuildTools')
    enable_encryption = settings.value('obfuscation/enable_encryption', True, bool)
    mov_r10_rcx_variants = [
        "    lea r10, [rcx]\n",
        "    push rcx\n    pop r10\n",
        "    mov r11, rcx\n    xchg r10, r11\n"
    ]
    if enable_encryption and encryption_key is not None:
        mov_eax_offset_variants = [
            f"    mov eax, dword ptr [{offset_name}]\n"
            f"    mov ebx, 0{encryption_key:X}h\n"
            f"    xor eax, ebx\n"
        ]
    else:
        mov_eax_offset_variants = [
            f"    xor eax, eax\n    add eax, dword ptr [{offset_name}]\n",
            f"    mov ebx, dword ptr [{offset_name}]\n    xchg eax, ebx\n"
        ]
    syscall_variants = [
        "    syscall\n",
    ]
    sequence = [
        random.choice(mov_r10_rcx_variants),
        generate_junk_instructions(),
        mov_eax_offset_variants[0],
        generate_junk_instructions(),
        random.choice(syscall_variants),
        "    ret\n"
    ]
    return ''.join(sequence)

def generate_junk_instructions():
    settings = QSettings('SysCaller', 'BuildTools')
    min_inst = settings.value('obfuscation/min_instructions', 2, int)
    max_inst = settings.value('obfuscation/max_instructions', 8, int)
    use_advanced = settings.value('obfuscation/use_advanced_junk', False, bool)
    junk_instructions = [
        "    nop\n",
        "    xchg r8, r8\n",
        "    xchg r9, r9\n",
        "    xchg r10, r10\n",
        "    xchg r11, r11\n",
        "    xchg r12, r12\n",
        "    xchg r13, r13\n",
        "    xchg r14, r14\n",
        "    xchg r15, r15\n",
        "    xchg rax, rax\n",
        "    xchg rbx, rbx\n",
        "    xchg rcx, rcx\n",
        "    xchg rdx, rdx\n",
        "    xchg rsi, rsi\n",
        "    xchg rdi, rdi\n",
        "    push r8\n    pop r8\n",
        "    push r9\n    pop r9\n",
        "    push r10\n    pop r10\n",
        "    push r11\n    pop r11\n",
        "    push r12\n    pop r12\n",
        "    push r13\n    pop r13\n",
        "    push r14\n    pop r14\n",
        "    push r15\n    pop r15\n",
        "    pushfq\n    popfq\n",
        "    test r8, r8\n",
        "    test r9, r9\n",
        "    test r10, r10\n",
        "    test r11, r11\n",
        "    test r12, r12\n",
        "    test r13, r13\n",
        "    test r14, r14\n",
        "    test r15, r15\n",
        "    lea r8, [r8]\n",
        "    lea r9, [r9]\n",
        "    lea r10, [r10]\n",
        "    lea r11, [r11]\n",
        "    lea r12, [r12]\n",
        "    lea r13, [r13]\n",
        "    lea r14, [r14]\n",
        "    lea r15, [r15]\n",
        "    mov r8, r8\n",
        "    mov r9, r9\n",
        "    mov r10, r10\n",
        "    mov r11, r11\n",
        "    mov r12, r12\n",
        "    mov r13, r13\n",
        "    mov r14, r14\n",
        "    mov r15, r15\n",
    ]
    if use_advanced:
        advanced_junk = [
            "    pause\n",
            "    fnop\n",
            "    cld\n",
            "    std\n    cld\n",
            "    clc\n",
            "    stc\n    clc\n",
            "    cmc\n    cmc\n",
            "    xor r8d, 0\n",
            "    xor r9d, 0\n",
            "    and r10d, -1\n",
            "    and r11d, -1\n",
            "    or r12d, 0\n",
            "    or r13d, 0\n",
            "    add r14d, 0\n",
            "    add r15d, 0\n",
            "    sub rax, 0\n",
            "    sub rbx, 0\n",
            "    db 66h\n    nop\n",
            "    db 0Fh, 1Fh, 00h\n",
            "    db 0Fh, 1Fh, 40h, 00h\n",
            "    db 0Fh, 1Fh, 44h, 00h, 00h\n",
            "    db 66h, 0Fh, 1Fh, 44h, 00h, 00h\n",
            "    shl r8, 0\n",
            "    shr r9, 0\n",
            "    ror r10, 0\n",
            "    rol r11, 0\n",
            "    bswap rax\n    bswap rax\n",
            "    not r12\n    not r12\n",
            "    neg r13\n    neg r13\n",
            "    inc r14\n    dec r14\n",
            "    dec r15\n    inc r15\n",
            "    lahf\n    sahf\n",
            "    prefetchnta [rsp]\n",
            "    lfence\n",
            "    sfence\n",
            "    mfence\n",
            "    movq xmm0, xmm0\n",
            "    movq xmm1, xmm1\n",
        ]
        junk_instructions.extend(random.choices(advanced_junk, k=random.randint(2, 8)))
    return ''.join(random.choices(junk_instructions, k=random.randint(min_inst, max_inst)))

def generate_random_label():
    return generate_random_string(8)

def generate_chunked_sequence(offset_name, encryption_key=None):
    settings = QSettings('SysCaller', 'BuildTools')
    enable_chunking = settings.value('obfuscation/enable_chunking', True, bool)
    enable_encryption = settings.value('obfuscation/enable_encryption', True, bool)
    if not enable_chunking:
        return generate_masked_sequence(offset_name, encryption_key)
    entry_label = generate_random_label()
    middle_label = generate_random_label()
    exit_label = generate_random_label()
    if enable_encryption and encryption_key is not None:
        syscall_sequence = [
            f"    mov eax, dword ptr [{offset_name}]\n",
            f"    mov ebx, 0{encryption_key:X}h\n",
            f"    xor eax, ebx\n"
        ]
    else:
        syscall_sequence = [
            f"    xor eax, eax\n    add eax, dword ptr [{offset_name}]\n"
        ]
    chunks = [
        f"{entry_label}:\n"
        f"    mov r10, rcx\n"
        f"    {generate_junk_instructions()}\n"
        f"    jmp {middle_label}\n",
        
        f"{middle_label}:\n"
        f"    {''.join(syscall_sequence)}"
        f"    {generate_junk_instructions()}\n"
        f"    jmp {exit_label}\n",
        
        f"{exit_label}:\n"
        f"    syscall\n"
        f"    {generate_junk_instructions()}\n"
        f"    ret\n"
    ]
    entry = chunks[0]
    rest = chunks[1:]
    random.shuffle(rest)
    chunks = [entry] + rest
    return ''.join(chunks)

def generate_align_padding():
    align_size = random.choice([4, 8, 16])
    padding = []
    for _ in range(random.randint(1, 3)):
        padding.append(generate_junk_instructions())
    padding.append(f"ALIGN {align_size}\n")
    return ''.join(padding)

def generate_exports():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    asm_path = os.path.join(project_root, 'Wrapper', 'src', 'syscaller.asm')
    header_path = os.path.join(project_root, 'Wrapper', 'include', 'Sys', 'sysFunctions.h')
    settings = QSettings('SysCaller', 'BuildTools')
    selected_syscalls = settings.value('integrity/selected_syscalls', [], type=list)
    use_all_syscalls = len(selected_syscalls) == 0
    syscall_mode = settings.value('general/syscall_mode', 'Nt', str)
    syscall_prefix = "Sys" if syscall_mode == "Nt" else "SysK"
    used_names = set()
    used_offsets = set()
    used_offset_names = set()
    offset_name_map = {}  # Maps fake offset to random name
    syscall_map = {}  # Maps original syscall to random name
    syscall_offsets = {}  # Maps original syscall to its offset
    real_to_fake_offset = {}  # Maps real offset to fake offset
    syscall_stubs = []
    current_stub = []
    with open(asm_path, 'r') as f:
        content = f.readlines()
        in_stub = False
        current_syscall = None
        for line in content:
            proc_match = re.search(r"((?:SC|Sys|SysK)\w+)\s+PROC", line)
            if proc_match:
                current_syscall = proc_match.group(1)
                if current_syscall.startswith("SC"):
                    current_syscall = syscall_prefix + current_syscall[2:]
                in_stub = True
                current_stub = [line]
                if use_all_syscalls or current_syscall in selected_syscalls:
                    if current_syscall not in syscall_map:
                        syscall_map[current_syscall] = generate_random_name(used_names)
            elif in_stub:
                current_stub.append(line)
                if 'mov eax,' in line and current_syscall:
                    try:
                        real_offset = extract_syscall_offset(line)
                        syscall_offsets[current_syscall] = real_offset
                        if real_offset not in real_to_fake_offset:
                            real_to_fake_offset[real_offset] = generate_random_offset(used_offsets)
                    except ValueError as e:
                        print(f"Error parsing offset for {current_syscall}: {e}")
                elif ' ENDP' in line:
                    in_stub = False
                    if use_all_syscalls or current_syscall in selected_syscalls:
                        syscall_stubs.append((current_syscall, current_stub))
    settings = QSettings('SysCaller', 'BuildTools')
    shuffle_sequence = settings.value('obfuscation/shuffle_sequence', True, bool)
    if shuffle_sequence:
        random.shuffle(syscall_stubs)
    publics = []
    aliases = []
    for original, random_name in syscall_map.items():
        publics.append(f'PUBLIC {random_name}')
        aliases.append(f'ALIAS <{original}> = <{random_name}>')
    new_content = []
    data_section = ['.data\n']
    data_section.append('ALIGN 8\n')
    settings = QSettings('SysCaller', 'BuildTools')
    enable_encryption = settings.value('obfuscation/enable_encryption', True, bool)
    enable_interleaved = settings.value('obfuscation/enable_interleaved', True, bool)
    encryption_keys = {}
    for real_offset, fake_offset in real_to_fake_offset.items():
        offset_name = generate_random_offset_name(used_offset_names)
        offset_name_map[fake_offset] = offset_name
        if enable_encryption:
            encryption_key = random.randint(0x11, 0xFF)
            encryption_keys[offset_name] = encryption_key
            encrypted_offset = real_offset ^ encryption_key
            data_section.append(f'{offset_name} dd 0{encrypted_offset:X}h  ; Encrypted syscall ID\n')
        else:
            data_section.append(f'{offset_name} dd 0{real_offset:X}h\n')
    new_content.append('.code\n\n')
    new_content.append('; Public declarations\n' + '\n'.join(publics) + '\n\n')
    new_content.append('; Export aliases\n' + '\n'.join(aliases) + '\n\n')
    for original_syscall, stub_lines in syscall_stubs:
        if enable_interleaved:
            new_content.append(generate_align_padding())
        for line in stub_lines:
            if ' PROC' in line or ' ENDP' in line:
                syscall_match = re.search(r"((?:SC|Sys|SysK)\w+)\s+(?:PROC|ENDP)", line)
                if syscall_match:
                    syscall = syscall_match.group(1)
                    if syscall.startswith("SC"):
                        syscall = syscall_prefix + syscall[2:]
                    if syscall in syscall_map:
                        line = re.sub(r"(SC|Sys|SysK)(\w+)\s+(PROC|ENDP)", 
                                     lambda m: f"{syscall_map[syscall]} {m.group(3)}", 
                                     line)
            elif 'mov eax,' in line and 'syscall' in ''.join(stub_lines):
                for syscall, offset in syscall_offsets.items():
                    if syscall == original_syscall:
                        fake_offset = real_to_fake_offset[offset]
                        offset_name = offset_name_map[fake_offset]
                        encryption_key = encryption_keys.get(offset_name) if enable_encryption else None
                        line = generate_chunked_sequence(offset_name, encryption_key)
                        break
            new_content.append(line)
        if enable_interleaved:
            new_content.append(generate_align_padding())
    new_content.append('\nend\n')
    for i, line in enumerate(new_content):
        if '.code' in line:
            new_content[i:i] = data_section
            break
    with open(asm_path, 'w') as f:
        f.writelines(new_content)
    all_syscalls = []
    all_header_lines = []
    current_block = []
    in_block = False
    current_syscall = None
    with open(header_path, 'r') as f:
        header_content = f.readlines()
    new_header_content = []
    skip_block = False
    ending_lines = []
    for i in range(len(header_content)-1, -1, -1):
        line = header_content[i].strip()
        if line == "#endif" or line.startswith("#endif "):
            ending_lines.insert(0, header_content[i])
            j = i - 1
            while j >= 0 and (header_content[j].strip() == "" or header_content[j].strip().startswith("//")):
                ending_lines.insert(0, header_content[j])
                j -= 1
            break
    header_part_ended = False
    for i, line in enumerate(header_content):
        if any(line == end_line for end_line in ending_lines):
            continue
        if not header_part_ended and (
            f'extern "C" NTSTATUS {syscall_prefix}' in line or 
            f'extern "C" ULONG {syscall_prefix}' in line or
            'extern "C" NTSTATUS SC' in line or
            'extern "C" ULONG SC' in line
        ):
            header_part_ended = True
        if not header_part_ended:
            if "_WIN64" in line and "#ifdef" in line:
                new_header_content.append(line)
                new_header_content.append("\n")
                continue
            new_header_content.append(line)
            continue
        if (
            'extern "C" NTSTATUS SC' in line or 
            'extern "C" ULONG SC' in line or
            f'extern "C" NTSTATUS {syscall_prefix}' in line or
            f'extern "C" ULONG {syscall_prefix}' in line
        ):
            match = re.search(rf'extern "C" (?:NTSTATUS|ULONG) ((?:SC|{syscall_prefix})\w+)\(', line)
            if match:
                original_name = match.group(1)
                if original_name.startswith("SC"):
                    current_syscall = syscall_prefix + original_name[2:]
                else:
                    current_syscall = original_name
                if use_all_syscalls or current_syscall in selected_syscalls:
                    skip_block = False
                    if current_syscall in syscall_map:
                        line = line.replace(original_name, syscall_map[current_syscall])
                    new_header_content.append(line)
                else:
                    skip_block = True
                continue
        if not skip_block:
            if "SC" in line:
                updated_line = re.sub(r'\bSC(\w+)\b', fr'{syscall_prefix}\1', line)
                new_header_content.append(updated_line)
            else:
                new_header_content.append(line)
        elif line.strip() == ");":
            skip_block = False
    new_header_content.append("\n// Syscall name mappings\n")
    for original, random_name in syscall_map.items():
        new_header_content.append(f"#define {original} {random_name}\n")
    cleaned_header_content = []
    prev_empty = False
    for line in new_header_content:
        if line.strip() == "":
            if not prev_empty:
                cleaned_header_content.append(line)
                prev_empty = True
        else:
            cleaned_header_content.append(line)
            prev_empty = False
    if ending_lines:
        if cleaned_header_content and cleaned_header_content[-1].strip() != "":
            cleaned_header_content.append("\n")
        non_empty_ending_found = False
        filtered_ending_lines = []
        for line in ending_lines:
            if line.strip() != "" or non_empty_ending_found:
                filtered_ending_lines.append(line)
                non_empty_ending_found = True
            else:
                continue
        cleaned_header_content.extend(filtered_ending_lines)
    if cleaned_header_content and not cleaned_header_content[-1].endswith('\n'):
        cleaned_header_content[-1] += '\n'
    with open(header_path, 'w') as f:
        f.writelines(cleaned_header_content)
    print(f"Generated {len(syscall_map)} unique syscalls with obfuscated names, offsets, and junk instructions")
    if shuffle_sequence:
        print("Syscall sequence has been randomized")

if __name__ == "__main__":
    generate_exports()
