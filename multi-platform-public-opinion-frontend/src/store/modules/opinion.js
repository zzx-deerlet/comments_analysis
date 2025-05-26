import { searchOpinions, getOpinionStats, exportOpinions } from '@/api/opinion'

const state = {
  opinionList: [],
  totalCount: 0,
  loading: false,
  stats: {
    sentimentDistribution: [],
    platformDistribution: [],
    trendData: []
  },
  exportHistory: [],
  exportLoading: false
}

const mutations = {
  SET_OPINION_LIST: (state, list) => {
    state.opinionList = list
  },
  SET_TOTAL_COUNT: (state, count) => {
    state.totalCount = count
  },
  SET_LOADING: (state, status) => {
    state.loading = status
  },
  SET_STATS: (state, stats) => {
    state.stats = stats
  },
  SET_EXPORT_HISTORY(state, history) {
    state.exportHistory = history
  },
  SET_EXPORT_LOADING(state, loading) {
    state.exportLoading = loading
  }
}

const actions = {
  // 搜索舆情数据
  searchOpinions({ commit }, params) {
    commit('SET_LOADING', true)
    return new Promise((resolve, reject) => {
      searchOpinions(params)
        .then(response => {
          const { data } = response
          commit('SET_OPINION_LIST', data.list)
          commit('SET_TOTAL_COUNT', data.total)
          commit('SET_LOADING', false)
          resolve(data)
        })
        .catch(error => {
          commit('SET_LOADING', false)
          reject(error)
        })
    })
  },

  // 获取舆情统计数据
  getOpinionStats({ commit }) {
    return new Promise((resolve, reject) => {
      getOpinionStats()
        .then(response => {
          const { data } = response
          commit('SET_STATS', data)
          resolve(data)
        })
        .catch(error => {
          reject(error)
        })
    })
  },

  // 获取导出历史
  async getExportHistory({ commit }) {
    commit('SET_EXPORT_LOADING', true)
    try {
      const response = await api.get('/opinion/export/history')
      commit('SET_EXPORT_HISTORY', response.data)
      return response.data
    } finally {
      commit('SET_EXPORT_LOADING', false)
    }
  },

  // 导出数据
  async exportOpinions({ commit }, params) {
    commit('SET_EXPORT_LOADING', true)
    try {
      const response = await api.post('/opinion/export', params)
      return response.data
    } finally {
      commit('SET_EXPORT_LOADING', false)
    }
  },

  // 下载导出文件
  async downloadExportFile({ commit }, fileName) {
    try {
      const response = await api.get(`/opinion/export/download/${fileName}`, {
        responseType: 'blob'
      })
      
      // 创建下载链接
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', fileName)
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    } catch (error) {
      throw error
    }
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
} 