/**
 * TC 1.1 - 註冊功能完整測試（整合）
 * 
 * 此檔案整合執行所有 TC 1.1.x 測試案例
 * 
 * 子測試案例：
 * - TC_1.1.1.test.js: 用戶欄位驗證 (3 tests)
 * - TC_1.1.2.test.js: 信箱欄位驗證 (3 tests)
 * - TC_1.1.3.test.js: 密碼欄位驗證 (3 tests)
 * - TC_1.1.4.test.js: 確認密碼欄位驗證 (5 tests)
 * - TC_1.1.5.test.js: 重複信箱註冊失敗 (1 test)
 * - TC_1.1.6.test.js: 成功註冊 (1 test)
 * 
 * 執行方式：
 * npx vitest run test/TC_1.1.test.js      # 執行整合測試（所有 16 個測試）
 * npx vitest run test/TC_1.1.1.test.js    # 執行單一子測試
 */

// 匯入所有子測試，它們會自動執行
import './TC_1.1.1.test.js'
import './TC_1.1.2.test.js'
import './TC_1.1.3.test.js'
import './TC_1.1.4.test.js'
