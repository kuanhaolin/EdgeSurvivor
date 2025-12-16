import pytest
import sys
import os

if __name__ == "__main__":
    # Define files relative to the project root (backend/)
    # Assuming this script is run from backend/ or backend/test/Intergration/
    # If run from backend/test/Intergration/, we need to adjust paths or CWD.
    # To keep it simple, let's assume we want to run it from backend/ root.
    
    # However, if the file is in test/Intergration/, the user might run it from there.
    # Let's make it robust to CWD.
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "../../"))
    
    # Change CWD to project root so imports work correctly
    os.chdir(project_root)
    sys.path.insert(0, project_root)
    
    files = [
        "test/Intergration/test_auth_flow.py",
        "test/Intergration/test_match_flow.py",
        "test/Intergration/test_e2e_scenarios.py",
        "test/Intergration/test_activity_flow.py"
    ]
    
    # Ensure report directory exists
    os.makedirs("test/reports", exist_ok=True)
    
    print(f"Running tests from {project_root}...")
    print("Running all tests and generating report...")
    
    args = ["-v", "--tb=short", "--html=test/reports/integration_full_report.html", "--self-contained-html"] + files
    ret = pytest.main(args)
    
    if ret == 0:
        print("All tests PASSED")
    else:
        print(f"Tests FAILED with code {ret}")
