/**
 * ActivityCard.vue 組件測試
 * 
 * 測試範圍：
 * - Props 傳遞與渲染
 * - 事件觸發
 * - 條件渲染
 * - 日期格式化
 */

import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import ActivityCard from '@/components/ActivityCard.vue'

describe('ActivityCard.vue', () => {
  const mockActivity = {
    activity_id: 1,
    title: '陽明山一日遊',
    date: '2025-12-25',
    location: '陽明山國家公園',
    description: '一起去爬山吧！享受大自然的美好',
    category: 'outdoor',
    max_participants: 10,
    current_participants: 5,
    cost: 300,
    creator: {
      user_id: 1,
      username: 'john_doe',
      avatar: 'https://example.com/avatar.jpg'
    },
    status: 'open'
  }
  
  it('應該正確渲染活動資訊', () => {
    const wrapper = mount(ActivityCard, {
      props: {
        activity: mockActivity
      }
    })
    
    // 檢查標題
    expect(wrapper.text()).toContain(mockActivity.title)
    
    // 檢查地點
    expect(wrapper.text()).toContain(mockActivity.location)
    
    // 檢查日期
    expect(wrapper.text()).toContain('2025-12-25')
    
    // 檢查描述
    expect(wrapper.text()).toContain(mockActivity.description)
  })
  
  it('應該顯示參與人數', () => {
    const wrapper = mount(ActivityCard, {
      props: {
        activity: mockActivity
      }
    })
    
    const text = wrapper.text()
    expect(text).toContain('5')
    expect(text).toContain('10')
  })
  
  it('應該顯示費用資訊', () => {
    const wrapper = mount(ActivityCard, {
      props: {
        activity: mockActivity
      }
    })
    
    expect(wrapper.text()).toContain('300')
  })
  
  it('應該處理免費活動（費用為 0）', () => {
    const freeActivity = {
      ...mockActivity,
      cost: 0
    }
    
    const wrapper = mount(ActivityCard, {
      props: {
        activity: freeActivity
      }
    })
    
    const text = wrapper.text()
    expect(text).toMatch(/免費|Free/i)
  })
  
  it('應該顯示活動類別標籤', () => {
    const wrapper = mount(ActivityCard, {
      props: {
        activity: mockActivity
      }
    })
    
    // 檢查是否有類別相關的元素
    const categoryElement = wrapper.find('.category, .tag, [class*="category"]')
    expect(categoryElement.exists()).toBe(true)
  })
  
  it('應該在點擊時觸發 click 事件', async () => {
    const wrapper = mount(ActivityCard, {
      props: {
        activity: mockActivity
      }
    })
    
    // 點擊卡片
    await wrapper.trigger('click')
    
    // 檢查是否觸發事件
    expect(wrapper.emitted()).toHaveProperty('click')
    expect(wrapper.emitted('click')[0]).toEqual([mockActivity])
  })
  
  it('應該顯示「已滿」狀態', () => {
    const fullActivity = {
      ...mockActivity,
      current_participants: 10,
      max_participants: 10
    }
    
    const wrapper = mount(ActivityCard, {
      props: {
        activity: fullActivity
      }
    })
    
    const text = wrapper.text()
    expect(text).toMatch(/已滿|Full|滿員/i)
  })
  
  it('應該顯示「即將額滿」狀態', () => {
    const almostFullActivity = {
      ...mockActivity,
      current_participants: 9,
      max_participants: 10
    }
    
    const wrapper = mount(ActivityCard, {
      props: {
        activity: almostFullActivity
      }
    })
    
    // 檢查是否有警告樣式或提示
    const warningElement = wrapper.find('[class*="warning"], [class*="almost"]')
    expect(warningElement.exists()).toBe(true)
  })
  
  it('應該顯示創建者資訊', () => {
    const wrapper = mount(ActivityCard, {
      props: {
        activity: mockActivity
      }
    })
    
    expect(wrapper.text()).toContain(mockActivity.creator.username)
  })
  
  it('應該顯示創建者頭像', () => {
    const wrapper = mount(ActivityCard, {
      props: {
        activity: mockActivity
      }
    })
    
    const avatar = wrapper.find('img[src*="avatar"]')
    expect(avatar.exists()).toBe(true)
    expect(avatar.attributes('src')).toBe(mockActivity.creator.avatar)
  })
  
  it('應該處理已取消的活動', () => {
    const cancelledActivity = {
      ...mockActivity,
      status: 'cancelled'
    }
    
    const wrapper = mount(ActivityCard, {
      props: {
        activity: cancelledActivity
      }
    })
    
    // 應該有視覺提示顯示已取消
    const text = wrapper.text()
    expect(text).toMatch(/已取消|Cancelled|取消/i)
  })
  
  it('應該處理已結束的活動', () => {
    const pastActivity = {
      ...mockActivity,
      date: '2020-01-01',
      status: 'completed'
    }
    
    const wrapper = mount(ActivityCard, {
      props: {
        activity: pastActivity
      }
    })
    
    const text = wrapper.text()
    expect(text).toMatch(/已結束|Completed|結束/i)
  })
  
  it('應該有加入/查看詳情按鈕', () => {
    const wrapper = mount(ActivityCard, {
      props: {
        activity: mockActivity
      }
    })
    
    const button = wrapper.find('button, .button, [class*="join-btn"]')
    expect(button.exists()).toBe(true)
  })
  
  it('應該觸發加入活動事件', async () => {
    const wrapper = mount(ActivityCard, {
      props: {
        activity: mockActivity
      }
    })
    
    // 找到加入按鈕並點擊
    const joinButton = wrapper.find('button')
    await joinButton.trigger('click')
    
    // 檢查事件（可能是 join 或 click）
    const emitted = wrapper.emitted()
    expect(
      emitted.hasOwnProperty('join') || emitted.hasOwnProperty('click')
    ).toBe(true)
  })
  
  it('應該截斷過長的描述', () => {
    const longDescActivity = {
      ...mockActivity,
      description: 'A'.repeat(200)
    }
    
    const wrapper = mount(ActivityCard, {
      props: {
        activity: longDescActivity,
        maxDescriptionLength: 100
      }
    })
    
    const description = wrapper.find('.description, [class*="desc"]')
    expect(description.text().length).toBeLessThanOrEqual(120) // 包含 "..."
  })
  
  it('應該格式化日期顯示', () => {
    const wrapper = mount(ActivityCard, {
      props: {
        activity: mockActivity
      }
    })
    
    // 檢查日期是否被格式化（可能是 "12/25" 或 "12月25日" 等格式）
    const dateText = wrapper.text()
    expect(dateText).toMatch(/12[月/-]25|2025/)
  })
})

/**
 * 測試執行指南：
 * 
 * 執行此測試：
 *   npm run test tests/ActivityCard.test.js
 * 
 * 監視模式（開發時）：
 *   npm run test tests/ActivityCard.test.js -- --watch
 * 
 * 查看覆蓋率：
 *   npm run test:coverage -- tests/ActivityCard.test.js
 */
