/**
 * TC 4.7.2 - 活動討論區：參與者發送留言（前端）
 * 測試前端討論區發送訊息的驗證和行為
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import ActivityDiscussion from '@/components/ActivityDiscussion.vue'
import axios from '@/utils/axios'
import { ElMessage } from 'element-plus'

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

describe('TC 4.7.2 - 討論區發送留言', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.setItem('user', JSON.stringify({ user_id: 1, name: '測試用戶' }))
  })

  it('測試發送留言功能', async () => {
    // Mock 初始載入
    axios.get.mockResolvedValue({ data: { discussions: [] } })
    axios.post.mockResolvedValue({
      data: {
        discussion: {
          discussion_id: 1,
          message: '測試留言',
          user_id: 1
        }
      }
    })
    
    const wrapper = mount(ActivityDiscussion, {
      props: {
        activityId: 1,
        creatorId: 1
      },
      global: {
        stubs: {
          'el-card': { template: '<div><slot /></div>' },
          'el-empty': { template: '<div />' },
          'el-input': { 
            template: '<textarea v-model="modelValue" @input="$emit(\'update:modelValue\', $event.target.value)" />',
            props: ['modelValue']
          },
          'el-button': { 
            template: '<button :disabled="disabled"><slot /></button>',
            props: ['disabled', 'loading']
          },
          'el-icon': { template: '<span><slot /></span>' },
          'el-avatar': { template: '<div><slot /></div>' }
        }
      }
    })

    await flushPromises()

    // 測試空訊息時禁用發送按鈕
    expect(wrapper.vm.newMessage).toBe('')
    
    // 測試設定訊息
    wrapper.vm.newMessage = '測試留言'
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.newMessage).toBe('測試留言')
    
    // 測試發送訊息
    await wrapper.vm.sendMessage()
    await flushPromises()
    
    // 驗證 API 被呼叫
    expect(axios.post).toHaveBeenCalledWith('/activities/1/discussions', {
      message: '測試留言',
      message_type: 'text'
    })
    
    // 驗證訊息被清空
    expect(wrapper.vm.newMessage).toBe('')
    
    // 驗證成功訊息
    expect(ElMessage.success).toHaveBeenCalled()
  })
})