/**
 * 費用表單驗證函數
 * 從 ExpenseManager.vue 提取，供測試和組件共用
 */

/**
 * 驗證費用項目（description）
 * 對應 ExpenseManager.vue 第 436 行
 */
export function validateDescription(description) {
  if (!description || !description.trim()) {
    return { valid: false, message: '請填寫費用項目' }
  }
  return { valid: true }
}

/**
 * 驗證費用金額（amount）
 * 對應 ExpenseManager.vue 第 436 行
 */
export function validateAmount(amount) {
  if (!amount || amount <= 0) {
    return { valid: false, message: '請輸入有效金額' }
  }
  return { valid: true }
}

/**
 * 驗證費用類別（category）
 * 對應 ExpenseManager.vue 第 436 行
 */
export function validateCategory(category) {
  const validCategories = ['transport', 'accommodation', 'food', 'ticket', 'other']
  
  if (!category || !validCategories.includes(category)) {
    return { valid: false, message: '請選擇有效的類別' }
  }
  
  return { valid: true }
}

/**
 * 驗證代墊人（payer_id）
 */
export function validatePayerId(payerId) {
  if (!payerId) {
    return { valid: false, message: '請選擇代墊人' }
  }
  return { valid: true }
}

/**
 * 驗證分攤方式（split_type）
 */
export function validateSplitType(splitType) {
  const validTypes = ['all', 'selected', 'borrow']
  
  if (!splitType || !validTypes.includes(splitType)) {
    return { valid: false, message: '請選擇有效的分攤方式' }
  }
  
  return { valid: true }
}

/**
 * 驗證分攤參與者（split_participants）
 * @param {Array} participants - 分攤參與者 ID 陣列
 * @param {string} splitType - 分攤方式
 * @param {number} payerId - 代墊人 ID
 */
export function validateSplitParticipants(participants, splitType, payerId) {
  // 如果是 selected 模式，必須選擇至少一位參與者
  if (splitType === 'selected') {
    if (!participants || !Array.isArray(participants) || participants.length === 0) {
      return { valid: false, message: '請選擇至少一位參與分攤的人' }
    }
    
    // 代墊人必須參與分攤
    if (payerId && !participants.includes(payerId)) {
      return { valid: false, message: '代墊人必須參與分攤' }
    }
  }
  
  return { valid: true }
}

/**
 * 驗證借款人（borrower_id）
 * @param {number} borrowerId - 借款人 ID
 * @param {string} splitType - 分攤方式
 */
export function validateBorrowerId(borrowerId, splitType) {
  // 如果是 borrow 模式，必須選擇借款人
  if (splitType === 'borrow') {
    if (!borrowerId) {
      return { valid: false, message: '請選擇借款人' }
    }
  }
  
  return { valid: true }
}

/**
 * 驗證費用表單（完整驗證）
 */
export function validateExpenseForm(expenseForm) {
  const descValidation = validateDescription(expenseForm.description)
  if (!descValidation.valid) {
    return descValidation
  }
  
  const amountValidation = validateAmount(expenseForm.amount)
  if (!amountValidation.valid) {
    return amountValidation
  }
  
  const categoryValidation = validateCategory(expenseForm.category)
  if (!categoryValidation.valid) {
    return categoryValidation
  }
  
  const payerValidation = validatePayerId(expenseForm.payer_id)
  if (!payerValidation.valid) {
    return payerValidation
  }
  
  return { valid: true }
}
