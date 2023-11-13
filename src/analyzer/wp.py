import os
import tempfile
import subprocess
import tempfile

def exec_wp(annotated_program : str):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".c", mode="w") as tmp_file:
        tmp_file.write(annotated_program)
        tmp_file_name = tmp_file.name
    command = ["frama-c", "-wp", "-wp-rte", "-wp-prover", "Alt-Ergo,Z3", "-wp-timeout", "10", tmp_file_name]
    try:
        return subprocess.run(command, capture_output=True, text=True)
    finally:
        os.remove(tmp_file_name)

def extract_proof_count_score(wp_output : str):
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
    if(prove_line is None):
        return 0 

    _, after = prove_line.split(":", 1)
    proved, goals = after.split("/", 1)
    ratio_proved = int(proved) / int(goals)
    if ratio_proved >= 1:
        return .75
    elif ratio_proved >= .5:
        return .5
    else:
        return .25
    
    

    

