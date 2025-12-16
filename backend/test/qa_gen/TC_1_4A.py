"""
TC 1.4A - 啟用雙因素認證 (2FA) 測試套件
自動執行所有 TC_1_4A_*.py 測試
"""

import subprocess
import os
import glob

def test_run_all_2fa_enable_tests():
    """執行所有 2FA 啟用測試"""
    current_dir = os.path.dirname(__file__) or '.'
    pattern = os.path.join(current_dir, 'TC_1_4A_*.py')
    test_files = sorted([
        os.path.basename(p) for p in glob.glob(pattern)
        if os.path.basename(p) != os.path.basename(__file__)
    ])
    assert test_files, '未找到任何 TC_1_4A_*.py 子測試檔'

    result = subprocess.run(
        ['pytest'] + test_files + ['-v', '--no-cov', '--tb=no'],
        capture_output=False,
        text=True
    )

    assert result.returncode == 0, '有測試失敗'


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v', '--no-cov'])
