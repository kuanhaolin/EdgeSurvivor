"""
TC 1.2: Email 登入測試
執行所有 TC_1.2 相關的登入測試
"""

import subprocess
import sys
import os
import glob

def test_run_all_login_tests():
    """自動讀取並執行所有 TC_1_2_*.py 子測試檔"""
    current_dir = os.path.dirname(__file__) or '.'
    pattern = os.path.join(current_dir, 'TC_1_2_*.py')
    test_files = sorted([
        os.path.basename(p) for p in glob.glob(pattern)
        if os.path.basename(p) != os.path.basename(__file__)
    ])
    assert test_files, '未找到任何 TC_1_2_*.py 子測試檔'

    result = subprocess.run(
        ['pytest'] + test_files + ['-v', '--no-cov', '--tb=no'],
        capture_output=False,
        text=True
    )

    assert result.returncode == 0, '有測試失敗'


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v', '--no-cov'])
