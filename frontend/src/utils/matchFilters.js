/**
 * 配對篩選邏輯
 * 從 Matches.vue 的 filteredRecommendedMatches 提取的篩選邏輯
 */

/**
 * 應用所有篩選條件到配對列表
 * @param {Array} matches - 推薦配對列表
 * @param {Object} filters - 篩選條件
 * @param {string} filters.gender - 性別篩選 ('male', 'female', 'other', '')
 * @param {Array} filters.ageRange - 年齡範圍 [minAge, maxAge]
 * @param {string} filters.location - 地區關鍵字
 * @param {Array} filters.interests - 興趣標籤陣列
 * @param {boolean} filters.verifiedOnly - 是否只顯示已驗證用戶
 * @returns {Array} 篩選後的配對列表
 */
export const applyMatchFilters = (matches, filters) => {
  const gender = filters.gender
  const [minAge, maxAge] = filters.ageRange || [18, 65]
  const location = (filters.location || '').toLowerCase()
  const interests = filters.interests || []
  const verifiedOnly = !!filters.verifiedOnly

  return matches.filter((m) => {
    // 性別篩選
    if (gender && m.gender !== gender) return false
    
    // 年齡範圍篩選
    if (typeof m.age === 'number') {
      if (m.age < minAge || m.age > maxAge) return false
    }
    
    // 地區篩選（模糊搜尋）
    if (location && !(m.location || '').toLowerCase().includes(location)) return false
    
    // 已驗證篩選
    if (verifiedOnly && !m.verified) return false
    
    // 興趣篩選（至少符合一個興趣）
    if (interests.length > 0) {
      const userInterests = new Set((m.interests || []).map(String))
      const hasAnyInterest = interests.some((i) => userInterests.has(String(i)))
      if (!hasAnyInterest) return false
    }
    
    return true
  })
}

/**
 * 重置篩選條件到預設值
 * @returns {Object} 預設的篩選條件物件
 */
export const getDefaultFilters = () => ({
  gender: '',
  ageRange: [20, 40],
  location: '',
  interests: [],
  verifiedOnly: false
})
