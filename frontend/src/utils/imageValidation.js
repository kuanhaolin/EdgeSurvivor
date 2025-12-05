/**
 * 圖片上傳驗證規則
 */

export const IMAGE_MAX_SIZE = 2 * 1024 * 1024 // 2MB

/**
 * 驗證是否為圖片文件
 * @param {File} file - 要驗證的文件
 * @returns {boolean} 是否為圖片
 */
export function isImageFile(file) {
  return file && file.type.startsWith('image/')
}

/**
 * 驗證圖片大小是否符合限制
 * @param {File} file - 要驗證的文件
 * @param {number} maxSize - 最大檔案大小（bytes），預設 2MB
 * @returns {boolean} 大小是否符合
 */
export function isValidImageSize(file, maxSize = IMAGE_MAX_SIZE) {
  return file && file.size <= maxSize
}

/**
 * 驗證圖片文件（類型和大小）
 * @param {File} file - 要驗證的文件
 * @returns {Object} { valid: boolean, error: string }
 */
export function validateImageFile(file) {
  if (!file) {
    return { valid: false, error: '請選擇文件' }
  }

  if (!isImageFile(file)) {
    return { valid: false, error: '請選擇圖片檔案' }
  }

  if (!isValidImageSize(file)) {
    return { valid: false, error: '圖片大小不能超過 2MB' }
  }

  return { valid: true, error: null }
}
