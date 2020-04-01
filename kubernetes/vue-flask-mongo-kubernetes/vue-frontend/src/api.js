import axios from 'axios'

const flaskApi = axios.create({
  baseURL: 'http://app-boilerplate/api/'
})

export default {
  ping: () => flaskApi.get('/ping'),
  getAllPosts: () => flaskApi.get('/posts'),
  getPost: (id) => flaskApi.get(`/posts/${id}`),
  createPost: (body) => flaskApi.post('/posts', body),
  editPost: (id, body) => flaskApi.put(`/posts/${id}`, body),
  deletePost: (id) => flaskApi.delete(`/posts/${id}`)
}