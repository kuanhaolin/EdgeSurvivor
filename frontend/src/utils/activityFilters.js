/**
 * 活動篩選工具函數
 * 從 Activities.vue 抽取，供前端和測試共用
 */

// 字串正規化（轉小寫）
export const normalized = (s) => (s || '').toString().toLowerCase()

// 狀態匹配
export const statusMatches = (status, filterStatus) => {
  if (!filterStatus) return true
  // 將「招募中」視為 recruiting/active/open 的統稱
  if (filterStatus === 'recruiting') {
    return ['recruiting', 'active', 'open'].includes(status)
  }
  return status === filterStatus
}

// 類型匹配
export const typeMatches = (type, filterType) => {
  if (!filterType) return true
  return type === filterType
}

// 文字搜尋匹配
export const textMatches = (activity, searchQuery) => {
  if (!searchQuery) return true
  const q = normalized(searchQuery)
  return [activity.title, activity.location, activity.description, activity.creatorName]
    .some((f) => normalized(f).includes(q))
}

// 完整篩選邏輯
export const filterList = (list, { searchQuery, filterType, filterStatus }) => {
  return list.filter((a) => 
    statusMatches(a.status, filterStatus) && 
    typeMatches(a.type, filterType) && 
    textMatches(a, searchQuery)
  )
}
