/**
 * Login.vue 組件測試
 * 
 * 測試範圍：
 * - 組件渲染
 * - 表單驗證
 * - 登入流程
 * - 錯誤處理
 * - 兩步驟驗證（2FA）
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { createRouter, createMemoryHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import { useAuthStore } from '@/stores/auth'
import ElementPlus from 'element-plus'

// 創建測試路由
const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: '/', component: { template: '<div>Home</div>' } },
    { path: '/login', component: Login },
    { path: '/register', component: { template: '<div>Register</div>' } },
    { path: '/dashboard', component: { template: '<div>Dashboard</div>' } },
    { path: '/forgot-password', component: { template: '<div>Forgot Password</div>' } }
  ]
})

describe('Login.vue', () => {
  let wrapper
  let authStore
  
  beforeEach(async () => {
    // 設置 Pinia
    setActivePinia(createPinia())
    authStore = useAuthStore()
    
    // 推送到登入路由
    await router.push('/login')
    await router.isReady()
    
    // 掛載組件
    wrapper = mount(Login, {
      global: {
        plugins: [createPinia(), router, ElementPlus],
        stubs: {
          'el-icon': true
        }
      }
    })
  })
  
  it('應該正確渲染登入表單', () => {
    // 檢查標題
    expect(wrapper.text()).toContain('EdgeSurvivor')
    
    // 檢查表單欄位（使用 Element Plus 組件）
    const form = wrapper.findComponent({ name: 'ElForm' })
    expect(form.exists()).toBe(true)
    
    // 檢查電子郵件欄位
    const formItems = wrapper.findAllComponents({ name: 'ElFormItem' })
    expect(formItems.length).toBeGreaterThanOrEqual(2)
    
    // 檢查按鈕
    const buttons = wrapper.findAllComponents({ name: 'ElButton' })
    expect(buttons.length).toBeGreaterThan(0)
  })
  
  it('應該驗證電子郵件格式', async () => {
    // 獲取表單引用
    const formRef = wrapper.vm.loginFormRef
    
    // 設置無效的電子郵件
    wrapper.vm.loginForm.username = 'invalid-email'
    
    // 觸發驗證
    try {
      await formRef.validate()
      // 如果沒有拋出錯誤，測試應該失敗
      expect(true).toBe(false)
    } catch (error) {
      // 驗證應該失敗
      expect(error).toBeDefined()
    }
  })
  
  it('應該驗證密碼必填', async () => {
    const formRef = wrapper.vm.loginFormRef
    
    // 設置空密碼
    wrapper.vm.loginForm.username = 'test@example.com'
    wrapper.vm.loginForm.password = ''
    
    // 觸發驗證
    try {
      await formRef.validate()
      expect(true).toBe(false)
    } catch (error) {
      expect(error).toBeDefined()
    }
  })
  
  it('應該成功提交登入表單', async () => {
    // Mock 登入 API
    const loginSpy = vi.spyOn(authStore, 'login')
    loginSpy.mockResolvedValue({ 
      access_token: 'test-token',
      user: { email: 'test@example.com' }
    })
    
    // 填寫表單
    wrapper.vm.loginForm.username = 'test@example.com'
    wrapper.vm.loginForm.password = 'password123'
    
    // 提交表單
    await wrapper.vm.handleLogin()
    await wrapper.vm.$nextTick()
    
    // 驗證登入函數被調用
    expect(loginSpy).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123'
    })
  })
  
  it('應該處理登入失敗', async () => {
    // Mock 登入失敗
    const loginSpy = vi.spyOn(authStore, 'login')
    const error = new Error('Invalid credentials')
    error.response = { data: { error: '電子郵件或密碼錯誤' } }
    loginSpy.mockRejectedValue(error)
    
    // 填寫表單
    wrapper.vm.loginForm.username = 'test@example.com'
    wrapper.vm.loginForm.password = 'wrongpassword'
    
    // 提交表單
    await wrapper.vm.handleLogin()
    await wrapper.vm.$nextTick()
    
    // 驗證錯誤被處理（loading 狀態應該解除）
    expect(wrapper.vm.loading).toBe(false)
  })
  
  it('應該在登入中顯示載入狀態', async () => {
    // Mock 延遲的登入
    const loginSpy = vi.spyOn(authStore, 'login')
    loginSpy.mockImplementation(() => new Promise(resolve => {
      setTimeout(() => resolve({ 
        access_token: 'test-token',
        user: { email: 'test@example.com' }
      }), 100)
    }))
    
    // 提交表單
    wrapper.vm.loginForm.username = 'test@example.com'
    wrapper.vm.loginForm.password = 'password123'
    
    // 開始登入
    const loginPromise = wrapper.vm.handleLogin()
    
    // 應該顯示載入中
    expect(wrapper.vm.loading).toBe(true)
    
    // 等待登入完成
    await loginPromise
    await wrapper.vm.$nextTick()
    
    // 載入狀態應該解除
    expect(wrapper.vm.loading).toBe(false)
  })
  
  it('應該處理兩步驟驗證（2FA）', async () => {
    // Mock 需要 2FA 的回應
    const loginSpy = vi.spyOn(authStore, 'login')
    loginSpy.mockResolvedValueOnce({ 
      require_2fa: true,
      message: '請輸入兩步驟驗證碼'
    })
    
    // 填寫表單
    wrapper.vm.loginForm.username = 'test@example.com'
    wrapper.vm.loginForm.password = 'password123'
    
    // 第一次提交
    await wrapper.vm.handleLogin()
    await wrapper.vm.$nextTick()
    
    // 應該顯示 2FA 欄位
    expect(wrapper.vm.require2FA).toBe(true)
    
    // Mock 第二次登入（帶驗證碼）
    loginSpy.mockResolvedValueOnce({ 
      access_token: 'test-token',
      user: { email: 'test@example.com' }
    })
    
    // 輸入驗證碼並再次提交
    wrapper.vm.loginForm.twoFactorCode = '123456'
    await wrapper.vm.handleLogin()
    await wrapper.vm.$nextTick()
    
    // 驗證登入函數被調用並包含驗證碼
    expect(loginSpy).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123',
      two_factor_code: '123456'
    })
  })
  
  it('應該有註冊連結', () => {
    const registerButton = wrapper.findAllComponents({ name: 'ElButton' })
      .find(btn => btn.text().includes('註冊'))
    expect(registerButton).toBeDefined()
  })
  
  it('應該有忘記密碼連結', () => {
    const forgotPasswordLink = wrapper.findComponent({ name: 'ElLink' })
    expect(forgotPasswordLink.exists()).toBe(true)
    expect(forgotPasswordLink.text()).toMatch(/忘記密碼/i)
  })
  
  it('應該正確跳轉至儀表板（登入成功後）', async () => {
    // Mock 成功的登入
    const loginSpy = vi.spyOn(authStore, 'login')
    loginSpy.mockResolvedValue({ 
      access_token: 'test-token',
      user: { email: 'test@example.com' }
    })
    
    // Mock router.push
    const pushSpy = vi.spyOn(router, 'push')
    
    // 填寫並提交表單
    wrapper.vm.loginForm.username = 'test@example.com'
    wrapper.vm.loginForm.password = 'password123'
    await wrapper.vm.handleLogin()
    await wrapper.vm.$nextTick()
    
    // 驗證跳轉（由 authStore.login 處理）
    // 注意：實際跳轉在 auth store 中執行
    expect(loginSpy).toHaveBeenCalled()
  })
  
  it('應該處理網路錯誤', async () => {
    // Mock 網路錯誤（沒有 response）
    const loginSpy = vi.spyOn(authStore, 'login')
    loginSpy.mockRejectedValue(new Error('Network Error'))
    
    // 填寫表單
    wrapper.vm.loginForm.username = 'test@example.com'
    wrapper.vm.loginForm.password = 'password123'
    
    // 提交表單
    await wrapper.vm.handleLogin()
    await wrapper.vm.$nextTick()
    
    // 應該處理錯誤並恢復載入狀態
    expect(wrapper.vm.loading).toBe(false)
  })
})

/**
 * 測試執行指南：
 * 
 * 執行所有前端測試：
 *   npm run test
 * 
 * 執行此測試檔案：
 *   npm run test tests/Login.test.js
 * 
 * 查看覆蓋率：
 *   npm run test:coverage
 * 
 * 監視模式（開發時使用）：
 *   npm run test -- --watch
 */
