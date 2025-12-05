"""
TC 1.1: 註冊功能完整測試套件
執行所有註冊相關的測試案例 (TC 1.1.1 - TC 1.1.6)

使用方式：
pytest tests/TC_1_1.py -v --no-cov --tb=no -q
"""

import pytest
import subprocess
import sys
import os
import glob


def test_run_all_registration_tests():
    """執行所有 TC 1.1.x 測試檔案"""
    # 自動讀取並執行所有子檔：TC_1_1_*.py（排除本檔）
    current_dir = os.path.dirname(__file__) or '.'
    pattern = os.path.join(current_dir, 'TC_1_1_*.py')
    test_files = sorted([
        os.path.basename(p) for p in glob.glob(pattern)
        if os.path.basename(p) != os.path.basename(__file__)
    ])
    assert test_files, '未找到任何 TC_1_1_*.py 子測試檔'
    
    # 執行所有測試，不使用 -q 來顯示詳細結果
    result = subprocess.run(
        ['pytest'] + test_files + ['-v', '--no-cov', '--tb=no'],
        capture_output=False,  # 直接輸出到終端
        text=True
    )
    
    # 檢查是否所有測試都通過
    assert result.returncode == 0, "部分測試失敗"
