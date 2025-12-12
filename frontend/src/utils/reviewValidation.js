/**
 * 評價表單驗證函數
 * 從 ActivityReviews.vue 提取，供測試和組件共用
 */

/**
 * 驗證評分
 * 對應 ActivityReviews.vue 第 233-236 行
 */
export function validateRating(rating) {
  if (!rating || rating < 1 || rating > 5) {
    return { valid: false, message: '請選擇 1-5 星評分' }
  }
  return { valid: true }
}

/**
 * 驗證評論內容
 * 對應 ActivityReviews.vue 第 238-241 行
 */
export function validateComment(comment) {
  if (!comment || !comment.trim()) {
    return { valid: false, message: '請填寫評價內容' }
  }
  return { valid: true }
}

/**
 * 驗證評價表單（完整驗證）
 */
export function validateReviewForm(reviewForm) {
  const ratingValidation = validateRating(reviewForm.rating)
  if (!ratingValidation.valid) {
    return ratingValidation
  }
  
  const commentValidation = validateComment(reviewForm.comment)
  if (!commentValidation.valid) {
    return commentValidation
  }
  
  return { valid: true }
}

/**
 * 計算提交按鈕是否應該被禁用
 * 對應 ActivityReviews.vue 第 159 行
 */
export function isSubmitDisabled(reviewForm) {
  return !reviewForm.rating || 
         reviewForm.rating < 1 || 
         !reviewForm.comment || 
         !reviewForm.comment.trim()
}
