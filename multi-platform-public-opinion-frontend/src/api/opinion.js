import request from './request'

// 搜索舆情数据
export function searchOpinions(params) {
  return request({
    url: '/opinion/search',
    method: 'get',
    params
  })
}

// 获取舆情统计数据
export function getOpinionStats() {
  return request({
    url: '/opinion/stats',
    method: 'get'
  })
}

// 导出舆情数据
export function exportOpinions(params) {
  return request({
    url: '/opinion/export',
    method: 'get',
    params,
    responseType: 'blob'
  })
}

// 获取舆情详情
export function getOpinionDetail(id) {
  return request({
    url: `/opinion/${id}`,
    method: 'get'
  })
}

// 获取舆情趋势数据
export function getOpinionTrend(params) {
  return request({
    url: '/opinion/trend',
    method: 'get',
    params
  })
}

// 获取舆情词云数据
export function getOpinionWordCloud(params) {
  return request({
    url: '/opinion/wordcloud',
    method: 'get',
    params
  })
} 