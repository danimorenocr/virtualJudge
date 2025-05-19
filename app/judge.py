import tempfile
import subprocess
from .models import TestCase
import os

def evaluate(code: str, language: str, problem_id: int, db):
    test_cases = db.query(TestCase).filter(TestCase.problem_id == problem_id).all()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as source_file:
        source_file.write(code.encode())
        source_file.flush()
        source_path = source_file.name

    results = []
    all_passed = True

    for case in test_cases:
        try:
            result = subprocess.run(
                ["python", source_path],
                input=case.input_data.encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=2
            )
            output = result.stdout.decode().strip()
            expected = case.expected_output.strip()

            passed = (output == expected)
            results.append({
                "input": case.input_data,
                "expected": expected,
                "actual": output,
                "verdict": "Passed" if passed else "Failed"
            })

            if not passed:
                all_passed = False
                # Se detiene la ejecución aquí si falla
                break

        except subprocess.TimeoutExpired:
            results.append({
                "input": case.input_data,
                "expected": case.expected_output.strip(),
                "actual": "",
                "verdict": "Time Limit Exceeded"
            })
            all_passed = False
            break

        except Exception as e:
            results.append({
                "input": case.input_data,
                "expected": case.expected_output.strip(),
                "actual": str(e),
                "verdict": "Runtime Error"
            })
            all_passed = False
            break

    os.remove(source_path)

    return {
        "result": "Accepted" if all_passed else "Wrong Answer",
        "details": results
    }
