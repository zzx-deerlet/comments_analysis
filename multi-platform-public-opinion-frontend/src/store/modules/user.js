import { login, logout, getInfo } from '@/api/user'

const state = {
  token: localStorage.getItem('token'),
  username: localStorage.getItem('username'),
  role: localStorage.getItem('userRole'),
  avatar: localStorage.getItem('avatar')
}

const mutations = {
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_USERNAME: (state, username) => {
    state.username = username
  },
  SET_ROLE: (state, role) => {
    state.role = role
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  }
}

const actions = {
  // 用户登录
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: password })
        .then(response => {
          const { data } = response
          commit('SET_TOKEN', data.token)
          commit('SET_USERNAME', data.username)
          commit('SET_ROLE', data.role)
          commit('SET_AVATAR', data.avatar)
          
          localStorage.setItem('token', data.token)
          localStorage.setItem('username', data.username)
          localStorage.setItem('userRole', data.role)
          localStorage.setItem('avatar', data.avatar)
          
          resolve()
        })
        .catch(error => {
          reject(error)
        })
    })
  },

  // 获取用户信息
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getInfo(state.token)
        .then(response => {
          const { data } = response
          if (!data) {
            reject('验证失败，请重新登录')
          }
          
          const { username, role, avatar } = data
          commit('SET_USERNAME', username)
          commit('SET_ROLE', role)
          commit('SET_AVATAR', avatar)
          
          resolve(data)
        })
        .catch(error => {
          reject(error)
        })
    })
  },

  // 用户登出
  logout({ commit }) {
    return new Promise((resolve, reject) => {
      logout()
        .then(() => {
          commit('SET_TOKEN', '')
          commit('SET_USERNAME', '')
          commit('SET_ROLE', '')
          commit('SET_AVATAR', '')
          
          localStorage.removeItem('token')
          localStorage.removeItem('username')
          localStorage.removeItem('userRole')
          localStorage.removeItem('avatar')
          
          resolve()
        })
        .catch(error => {
          reject(error)
        })
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
} 