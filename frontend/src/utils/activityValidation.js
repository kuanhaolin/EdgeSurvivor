/**
 * 活動表單驗證函數
 * 從 Activities.vue 的 createActivity 函數提取的驗證邏輯
 */

/**
 * 驗證活動表單必填欄位
 * @param {Object} activityForm - 活動表單資料
 * @param {string} activityForm.title - 活動標題
 * @param {string} activityForm.type - 活動類型
 * @param {string} activityForm.location - 活動地點
 * @param {Array} activityForm.dateRange - 日期範圍 [startDate, endDate]
 * @returns {boolean} 驗證是否通過
 */
export function validateActivityForm(activityForm) {
  // 對應 Activities.vue 第 931-932 行的驗證邏輯
  return !!(
    activityForm.title && 
    activityForm.type && 
    activityForm.location && 
    activityForm.dateRange && 
    activityForm.dateRange.length === 2
  )
}

/**
 * 驗證開始日期必須早於或等於結束日期
 * @param {Date|string} startDate - 開始日期
 * @param {Date|string} endDate - 結束日期
 * @returns {boolean} 驗證是否通過
 */
export function validateDateRange(startDate, endDate) {
  if (!startDate || !endDate) {
    return false
  }
  
  const start = new Date(startDate)
  const end = new Date(endDate)
  
  // 開始日期必須早於或等於結束日期
  return start <= end
}

/**
 * 驗證活動更新表單必填欄位
 * 從 ActivityDetail.vue 的 updateActivity 函數提取的驗證邏輯
 * @param {Object} editForm - 編輯表單資料
 * @param {string} editForm.title - 活動標題
 * @param {string} editForm.category - 活動類型
 * @param {string} editForm.location - 活動地點
 * @param {Array} editForm.dateRange - 日期範圍 [startDate, endDate]
 * @param {number} editForm.max_participants - 最大參與人數
 * @returns {Object} { valid: boolean, error: string }
 */
export function validateActivityUpdateForm(editForm) {
  // 對應 ActivityDetail.vue 第 451-454 行：檢查日期範圍
  if (!editForm.dateRange || editForm.dateRange.length !== 2) {
    return { valid: false, error: '請選擇活動日期' }
  }
  
  // 檢查必填欄位 (對應 el-form-item 的 required 屬性)
  if (!editForm.title || !editForm.title.trim()) {
    return { valid: false, error: '活動名稱不能為空' }
  }
  
  if (!editForm.category || !editForm.category.trim()) {
    return { valid: false, error: '活動類型不能為空' }
  }
  
  if (!editForm.location || !editForm.location.trim()) {
    return { valid: false, error: '地點不能為空' }
  }
  
  // 檢查人數上限 (對應 el-input-number 的 :min="2" :max="50")
  if (!editForm.max_participants || 
      typeof editForm.max_participants !== 'number' || 
      editForm.max_participants < 2) {
    return { valid: false, error: '人數必須含2人以上' }
  }
  
  return { valid: true }
}
