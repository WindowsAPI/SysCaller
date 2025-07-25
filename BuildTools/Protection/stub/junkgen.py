import sys
import os
import random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'GUI')))
from settings.utils import get_ini_path
from PyQt5.QtCore import QSettings

def generate_junk_instructions(min_inst=None, max_inst=None, use_advanced=None):
    settings = QSettings(get_ini_path(), QSettings.IniFormat)
    if min_inst is None:
        min_inst = settings.value('obfuscation/min_instructions', 2, int)
    if max_inst is None:
        max_inst = settings.value('obfuscation/max_instructions', 8, int)
    if use_advanced is None:
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
