import os
import subprocess
import json
import re
import shutil
from .temp import setup_wp_tmp


def exec_wp(annotated_program: str, headers_path: str, main_method: str):
    temp_file_path, temp_dir = setup_wp_tmp(
        headers_dir=headers_path, program_str=annotated_program
    )
    report_path = os.path.join(temp_dir, "report.json")
    command = [
        "frama-c",
        "-wp",
        "-wp-rte",
        "-wp-prover",
        "Alt-Ergo,Z3",
        "-no-cpp-frama-c-compliant",
        "-lib-entry",
        "-wp-timeout",
        "5",
        "-main",
        main_method,
        "-wp-report-json",
        report_path,
        temp_file_path,
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            with open(report_path, "r") as f:
                report_str = f.read()
                fixed_report_str = fix_json_number_format(report_str)
                report = json.loads(fixed_report_str)
        else:
            report = None

        return result, report
    finally:
        shutil.rmtree(temp_dir)

# wp has a bug in their json output
def fix_json_number_format(json_string):
    # Pattern to find numbers that end with a dot and are not followed by any digits
    pattern = re.compile(r'(\d+)\.(?!\d)')
    # Replace such numbers with the number itself (removing the dot)
    return pattern.sub(r'\1', json_string)

# def analyze_report(report):
#     out = {
#         "obligations": len(report),
#         "proved": 0,
#         "qed": 0,
#         "alt_ergo": 0,
#         "z3": 0,
#         "ensures": 0,
#         "ensures_proved": 0,
#         "loop_assigns": 0,
#         "loop_assigns_proved": 0,
#         "loop_invariant": 0,
#         "loop_invariant": 0,
#         "loop_variant": 0,
#         "rte_mem":
#     }
#     for obligation in report:
#         continue


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
