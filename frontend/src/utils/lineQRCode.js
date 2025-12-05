/**
 * LINE QR Code 生成工具
 */

/**
 * 生成 LINE QR Code
 * @param {string} lineId - LINE ID
 * @param {HTMLElement} container - 容器元素
 * @returns {Object} { success: boolean, lineUrl?: string, qrCodeUrl?: string, error?: string }
 */
export function generateLineQRCode(lineId, container) {
  if (!lineId) {
    return { success: false, error: '請先輸入 LINE ID' }
  }

  if (!container) {
    return { success: false, error: '找不到容器元素' }
  }
  
  // 清空容器
  container.innerHTML = ''
  
  // 使用 LINE 官方的 QR Code URL
  const lineUrl = `https://line.me/ti/p/${encodeURIComponent(lineId)}`
  
  // 使用第三方 QR Code 生成服務
  const qrCodeUrl = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(lineUrl)}`
  
  const img = document.createElement('img')
  img.src = qrCodeUrl
  img.alt = 'LINE QR Code'
  img.style.maxWidth = '100%'
  
  container.appendChild(img)
  
  return {
    success: true,
    lineUrl,
    qrCodeUrl
  }
}
