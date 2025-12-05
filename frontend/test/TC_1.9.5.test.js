import { describe, it, expect } from 'vitest'

describe('TC_1.9.5 - 顯示連結', () => {
  const testCases = [
    {
      name: '有資料，顯示有值的連結',
      instagram: 'https://instagram.com/user01',
      facebook: '',
      line: 'user01',
      twitter: '',
      expected: true
    },
    {
      name: '無資料，顯示未公開/未綁定社群帳號',
      instagram: '',
      facebook: '',
      line: '',
      twitter: '',
      expected: false
    }
  ]

  it.each(testCases)('$name', ({ instagram, facebook, line, twitter, expected }) => {
    const socialLinks = {
      instagram,
      facebook,
      line,
      twitter
    }

    const hasAnyLink = !!(
      socialLinks.instagram ||
      socialLinks.facebook ||
      socialLinks.line ||
      socialLinks.twitter
    )

    expect(hasAnyLink).toBe(expected)
  })
})
