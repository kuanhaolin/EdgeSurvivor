"""
整合測試報告生成器
從 pytest HTML 報告中提取測試結果並生成 CSV 報告
"""

import json
import csv
import re
import os
from pathlib import Path
from datetime import datetime
from html.parser import HTMLParser


class TestReportParser(HTMLParser):
    """解析 pytest HTML 報告"""
    
    def __init__(self):
        super().__init__()
        self.json_data = None
        
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for attr, value in attrs:
                if attr == 'data-jsonblob':
                    # 解碼 HTML 實體
                    json_str = value.replace('&#34;', '"').replace('&amp;', '&')
                    self.json_data = json.loads(json_str)


def parse_html_report(html_file):
    """解析 HTML 報告文件"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parser = TestReportParser()
    parser.feed(content)
    return parser.json_data


def extract_test_info(test_id, test_data):
    """從測試數據中提取信息"""
    # 解析測試 ID
    parts = test_id.split('::')
    file_path = parts[0] if len(parts) > 0 else ''
    test_class = parts[1] if len(parts) > 1 else ''
    test_name = parts[2] if len(parts) > 2 else ''
    
    # 獲取測試結果
    result = test_data[0]['result']
    duration = test_data[0]['duration']
    
    # 提取錯誤信息（如果有）
    log = test_data[0].get('log', '')
    error_msg = ''
    if result in ['Failed', 'Error']:
        # 提取最後一行錯誤信息
        lines = log.split('\\n')
        for line in reversed(lines):
            if line.strip() and not line.startswith(' '):
                error_msg = line.strip()
                break
    
    return {
        'file': file_path.replace('test/Intergration/', ''),
        'class': test_class,
        'test': test_name,
        'result': result,
        'duration': duration,
        'error': error_msg
    }


def generate_csv_report(html_file, output_csv):
    """生成 CSV 報告"""
    data = parse_html_report(html_file)
    
    if not data:
        print(f"無法解析 {html_file}")
        return
    
    # 提取測試結果
    tests = []
    for test_id, test_data in data['tests'].items():
        test_info = extract_test_info(test_id, test_data)
        tests.append(test_info)
    
    # 按文件和類別排序
    tests.sort(key=lambda x: (x['file'], x['class'], x['test']))
    
    # 寫入 CSV
    with open(output_csv, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['file', 'class', 'test', 'result', 'duration', 'error'])
        writer.writeheader()
        writer.writerows(tests)
    
    # 生成統計摘要
    summary = {
        'total': len(tests),
        'passed': sum(1 for t in tests if t['result'] == 'Passed'),
        'failed': sum(1 for t in tests if t['result'] == 'Failed'),
        'error': sum(1 for t in tests if t['result'] == 'Error'),
        'skipped': sum(1 for t in tests if t['result'] == 'Skipped'),
    }
    
    return tests, summary


def generate_summary_csv(tests, summary, output_file):
    """生成測試摘要 CSV"""
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['測試摘要'])
        writer.writerow(['項目', '數量'])
        writer.writerow(['總測試數', summary['total']])
        writer.writerow(['通過', summary['passed']])
        writer.writerow(['失敗', summary['failed']])
        writer.writerow(['錯誤', summary['error']])
        writer.writerow(['跳過', summary['skipped']])
        pass_rate = (summary['passed'] / summary['total'] * 100) if summary['total'] > 0 else 0
        writer.writerow(['通過率', f"{pass_rate:.1f}%"])
        writer.writerow([])
        
        # 按模組統計
        writer.writerow(['模組統計'])
        writer.writerow(['模組', '總數', '通過', '失敗', '通過率'])
        
        modules = {}
        for test in tests:
            module = test['file']
            if module not in modules:
                modules[module] = {'total': 0, 'passed': 0, 'failed': 0}
            modules[module]['total'] += 1
            if test['result'] == 'Passed':
                modules[module]['passed'] += 1
            elif test['result'] in ['Failed', 'Error']:
                modules[module]['failed'] += 1
        
        for module, stats in sorted(modules.items()):
            pass_rate = stats['passed'] / stats['total'] * 100 if stats['total'] > 0 else 0
            writer.writerow([
                module,
                stats['total'],
                stats['passed'],
                stats['failed'],
                f"{pass_rate:.1f}%"
            ])


if __name__ == '__main__':
    # 設定文件路徑 (相對於 project root)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "../../"))
    
    # Change CWD to project root
    os.chdir(project_root)
    
    report_dir = Path('test/reports')
    
    # 處理 auth_flow 報告
    auth_html = report_dir / 'auth_flow_report.html'
    auth_csv = report_dir / 'auth_flow_tests.csv'
    auth_summary_csv = report_dir / 'auth_flow_summary.csv'
    
    if auth_html.exists():
        print(f"正在處理 {auth_html}...")
        tests, summary = generate_csv_report(auth_html, auth_csv)
        generate_summary_csv(tests, summary, auth_summary_csv)
        print(f"✓ 詳細報告已生成: {auth_csv}")
        print(f"✓ 摘要報告已生成: {auth_summary_csv}")
        print(f"\n測試結果: {summary['passed']}/{summary['total']} 通過")
    
    # 處理完整整合測試報告（如果存在）
    full_html = report_dir / 'integration_full_report.html'
    full_csv = report_dir / 'integration_tests.csv'
    full_summary_csv = report_dir / 'integration_summary.csv'
    
    if full_html.exists():
        print(f"\n正在處理 {full_html}...")
        tests, summary = generate_csv_report(full_html, full_csv)
        generate_summary_csv(tests, summary, full_summary_csv)
        print(f"✓ 詳細報告已生成: {full_csv}")
        print(f"✓ 摘要報告已生成: {full_summary_csv}")
        print(f"\n測試結果: {summary['passed']}/{summary['total']} 通過")
