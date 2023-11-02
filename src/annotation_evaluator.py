from sanitize import extract_c_program, extract_classification_count
from wp import exec_wp, extract_proof_count_score
from langchain.evaluation.schema import StringEvaluator
from typing import Any, Optional


class AnnotationEvaluator(StringEvaluator):
    """
    Evaluate the output of the annotation chain
    """

    def _evaluate_strings(
        self,
        *,
        prediction: str,
        reference: Optional[str] = None,
        input: Optional[str] = None,
        **kwargs: Any
    ) -> dict:
        score = rank(prediction)

        return {
            "program": prediction,
            "rank": score,
        }


def rank(llm_output: str) -> float:
    """
    ranks an annotated program with a value from 0 to 1
    scoring is based on the following criteria:

    Main goals:
    all annotations proved -> +0.75
    half annotations proved -> +0.55
    correct syntax -> +0.25


    Extras:
    requires -> +0.02
    assigns -> +0.015
    loop invariant -> +0.01
    ensures -> +0.01
    other -> +0.005

    """
    try:
        program = extract_c_program(llm_output)
        wp_result = exec_wp(program)
        if(wp_result.returncode != 0):
            wp_score = 0
        else:
           wp_score = extract_proof_count_score(wp_result.stdout)

        classication_counts = extract_classification_count(llm_output)
        classification_score = get_classifications_score(classication_counts)

        return wp_score + classification_score
    except:
        return 0

def get_classifications_score(classification_counts):
    classification_values = {"requires": 0.02, "assigns": 0.015, "loop invariant": 0.01, "ensures": 0.01}
    return sum(classification_counts[key] * classification_values.get(key, 0.005) for key in classification_counts)

