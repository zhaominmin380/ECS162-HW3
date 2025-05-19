import { render, screen, fireEvent } from '@testing-library/svelte'
import App from './lib/CommentBox.svelte'
import { beforeEach, expect, test, vi } from 'vitest'

test('submits comment when Send is clicked', async () => {
  const mockPost = vi.fn((url, options) => {
    if (url === '/api/comments' && options?.method === 'POST') {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({})
      })
    }

    if (url.startsWith('/api/comments')) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve([])
      })
    }

    return Promise.resolve({ ok: true, json: () => Promise.resolve({}) })
  })

  vi.stubGlobal('fetch', mockPost)

  render(App, {
    props: {
      article: { headline: 'Test Article', url: 'https://example.com/article' },
      onClose: () => {}
    }
  })

  const input = await screen.findByPlaceholderText('Share your thoughts...')
  await fireEvent.input(input, { target: { value: 'my comment' } })

  const send = screen.getByText('Send')
  await fireEvent.click(send)

  expect(mockPost).toHaveBeenCalledWith(
    '/api/comments',
    expect.objectContaining({
      method: 'POST',
      body: expect.stringContaining('my comment')
    })
  )
})

// test if show alert when 
test('shows alert on failed comment submission', async () => {
  window.alert = vi.fn()

  // mock data
  vi.stubGlobal('fetch', vi.fn((url, options) => {
    // 'POST', api/comments
    if (url === '/api/comments' && options?.method === 'POST') {
      return Promise.resolve({
        ok: false,
        json: () => Promise.resolve({ error: 'Please login first' })
      })
    }

    // 'GET' api// comments
    if (url.startsWith('/api/comments')) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve([
          { _id: '1', content: 'test', username: 'user', parent_id: null, children: [] }
        ])
      })
    }

    return Promise.resolve({
      ok: true,
      json: () => Promise.resolve({})
    })
  }))

  render(App, {
    props: {
      article: { headline: 'Test Article', url: 'https://example.com/article' },
      onClose: () => {}
    }
  })

  const inputs = await screen.findAllByPlaceholderText('Share your thoughts...')
  await fireEvent.input(inputs[0], { target: { value: 'error test' } })

  const sendButtons = screen.getAllByText('Send')
  await fireEvent.click(sendButtons[0])

  expect(window.alert).toHaveBeenCalledWith('Please login first')
})
