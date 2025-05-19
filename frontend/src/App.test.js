import { render, screen, fireEvent } from '@testing-library/svelte'
import App from './App.svelte'
import { beforeEach, expect, test, vi } from 'vitest'

// fetch-mock
beforeEach(() => {
  vi.stubGlobal('fetch', vi.fn((url) => {
    if (url.includes('/api/news')) {
      return Promise.resolve({
        json: () => Promise.resolve([
          { headline: 'Headline', url: 'https://example.com/article', image: 'https://example.com/test.jpg' }
        ])
      })
    }

    if (url.includes('/api/user')) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ sub: 'aaa123', name: 'test user', email: 'user@example.com'})
      })
    }

    if (url.includes('/api/comments')) {
      return Promise.resolve({
        json: () => Promise.resolve([
          { _id: '1', content: 'test', username: 'user', parent_id: null, children: [] }
        ])
      })
    }

    return Promise.reject('Unknown endpoint')
  }))
})
//test headline
test('renders article headline', async () => {
    render(App)
  
    const textElement = await screen.findByText("Headline")
    expect(textElement).toBeTruthy()
})
//test article link
test('renders article link', async () => {
    render(App)

    const link = await screen.findByText('Read more')
    expect(link.getAttribute('href')).toBe('https://example.com/article')
})
//test image
test('renders news image with correct src', async () => {
    render(App)
  
    const imgs = await screen.findAllByRole('img')
    const newsImg = imgs.find(img => img.getAttribute('src') === 'https://example.com/test.jpg')
  
    expect(newsImg).toBeTruthy()
})

// test if log in button appear
test('shows login button when user is not logged in', async () => {
    render(App)

    const loginButtons = screen.getAllByRole('button', { name: 'Log in' })
    expect(loginButtons.length).toBeGreaterThan(0)
})

// test if sidebar correctly open (check if comments show) when clicking comments button
test('opens sidebar on comment button click', async () => {
  render(App)

  const commentButtons = await screen.getAllByText('💬 Comments')
  expect(commentButtons.length).toBeGreaterThan(0)

  await fireEvent.click(commentButtons[0])

  const commentHeader = await screen.findByText('Comments') 
  expect(commentHeader).toBeTruthy()
})

// test if side bar correctly
test('closes sidebar on close button click', async () => {
  render(App)

  const commentButtons = await screen.getAllByText('💬 Comments')
  expect(commentButtons.length).toBeGreaterThan(0)

  await fireEvent.click(commentButtons[0])

  const closeBtn = await screen.findByText('✕') 
  await fireEvent.click(closeBtn)

  expect(screen.queryByText('Comments')).toBeNull()
})
