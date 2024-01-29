import os
import subprocess
import tempfile
from .temp import setup_wp_tmp


def exec_wp(annotated_program: str, headers_path: str):
    temp_file_path, temp_dir = setup_wp_tmp(headers_dir=headers_path, program_str=annotated_program)
    command = [
        "frama-c",
        "-wp",
        "-wp-rte",
        "-wp-prover",
        "Alt-Ergo,Z3",
        "-no-cpp-frama-c-compliant",
        "-cpp-command",
        "-wp-timeout",
        "10",
        temp_file_path,
    ]
    try:
        return subprocess.run(command, capture_output=True, text=True)
    finally:
        os.remove(temp_dir)


def extract_proofs_and_goals(wp_output: str):
    """
    extracts the number of proved annotations from the wp output which looks like this:

    [kernel] Parsing /var/folders/gd/zlz1_ptj22lbpxsxbb02t1h40000gn/T/tmpyf1nn0c7.c (with preprocessing)
    [wp] Running WP plugin...
    [wp] Warning: Missing RTE guards
    [wp] /var/folders/gd/zlz1_ptj22lbpxsxbb02t1h40000gn/T/tmpyf1nn0c7.c:19: Warning:
      Missing assigns clause (assigns 'everything' instead)
    [wp] 18 goals scheduled
    [wp] [Timeout] typed_main_requires_2 (Z3)
    [wp] [Timeout] typed_main_requires (Z3)
    [wp] [Timeout] typed_main_ensures (Qed 13ms) (Z3)
    [wp] [Timeout] typed_main_loop_invariant_preserved (Qed 15ms) (Z3)
    [wp] [Timeout] typed_main_assert (Qed 4ms) (Z3)
    [wp] [Timeout] typed_main_loop_invariant_3_established (Qed 2ms) (Z3)
    [wp] [Timeout] typed_main_assigns_part4 (Qed 1ms) (Alt-Ergo)
    [wp] Proved goals:   11 / 18
    Qed:             8
    Alt-Ergo :       2 (16ms-18ms)
    Z3 4.12.2:       1 (20ms)
    Timeout:         7
    """
    lines = wp_output.split("\n")
    maybe_proved = filter(lambda line: "Proved goals" in line, lines)
    prove_line = next(maybe_proved, None)
    if prove_line is None:
        return -1, -1

    _, after = prove_line.split(":", 1)
    return after.split("/", 1)
