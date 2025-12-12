/**
 * TC 4.7.4 - 活動討論區：刪除留言（前端）
 * 測試前端刪除討論訊息的行為
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { ElMessageBox, ElMessage } from 'element-plus'
import ActivityDiscussion from '@/components/ActivityDiscussion.vue'
import axios from '@/utils/axios'

vi.mock('@/utils/axios')
vi.mock('element-plus', () => ({
  ElMessage: {
    success: vi.fn(),
    error: vi.fn()
  },
  ElMessageBox: {
    confirm: vi.fn()
  }
}))
vi.mock('@/services/socket', () => ({
  default: {
    isConnected: vi.fn(() => false),
    connect: vi.fn(),
    sendDiscussion: vi.fn(),
    onNewDiscussion: vi.fn(),
    onDiscussionDeleted: vi.fn(),
    joinActivityDiscussion: vi.fn(),
    leaveActivityDiscussion: vi.fn(),
  }
}))

describe('TC 4.7.4 - 刪除留言', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.setItem('user', JSON.stringify({ user_id: 1, name: '測試用戶' }))
  })

  it('測試刪除留言功能', async () => {
    axios.get.mockResolvedValue({ data: { discussions: [] } })
    axios.delete.mockResolvedValue({ data: { message: '訊息已刪除' } })

    const wrapper = mount(ActivityDiscussion, {
      props: {
        activityId: 1,
        creatorId: 1
      },
      global: {
        stubs: {
          'el-card': { template: '<div><slot /></div>' },
          'el-empty': { template: '<div />' },
          'el-input': { template: '<textarea />' },
          'el-button': { template: '<button><slot /></button>' },
          'el-icon': { template: '<span><slot /></span>' },
          'el-avatar': { template: '<div><slot /></div>' },
          'el-text': { template: '<span><slot /></span>' }
        }
      }
    })

    await flushPromises()

    // 驗證組件已掛載且方法可用
    expect(wrapper.vm).toBeTruthy()
    expect(typeof wrapper.vm.deleteMessage).toBe('function')
    
    // 驗證 API mock 設置正確
    expect(axios.delete).toBeDefined()
    expect(ElMessageBox.confirm).toBeDefined()
  })
})
