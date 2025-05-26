<template>
  <div class="analysis-container">
    <!-- 筛选条件 -->
    <el-card class="filter-card">
      <el-form :model="filterForm" :inline="true">
        <el-form-item label="时间范围">
          <el-date-picker
            v-model="filterForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
            @change="handleFilterChange"
          />
        </el-form-item>
        
        <el-form-item label="平台">
          <el-select
            v-model="filterForm.platform"
            placeholder="请选择平台"
            clearable
            @change="handleFilterChange"
          >
            <el-option
              v-for="item in platformOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 图表展示 -->
    <el-row :gutter="20" class="chart-row">
      <!-- 情感分布 -->
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>情感分布</span>
            </div>
          </template>
          <div class="chart" ref="sentimentChart"></div>
        </el-card>
      </el-col>
      
      <!-- 平台分布 -->
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>平台分布</span>
            </div>
          </template>
          <div class="chart" ref="platformChart"></div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" class="chart-row">
      <!-- 舆情趋势 -->
      <el-col :span="24">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>舆情趋势</span>
              <el-radio-group v-model="trendType" size="small" @change="handleTrendTypeChange">
                <el-radio-button label="day">日</el-radio-button>
                <el-radio-button label="week">周</el-radio-button>
                <el-radio-button label="month">月</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div class="chart" ref="trendChart"></div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" class="chart-row">
      <!-- 词云图 -->
      <el-col :span="24">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>热点词云</span>
            </div>
          </template>
          <div class="chart" ref="wordCloudChart"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { useStore } from 'vuex'
import * as echarts from 'echarts'
import 'echarts-wordcloud'

const store = useStore()
const sentimentChart = ref(null)
const platformChart = ref(null)
const trendChart = ref(null)
const wordCloudChart = ref(null)

// 筛选表单
const filterForm = reactive({
  dateRange: [],
  platform: ''
})

// 趋势图类型
const trendType = ref('day')

// 平台选项
const platformOptions = [
  { label: '微博', value: 'weibo' },
  { label: '微信', value: 'wechat' },
  { label: '知乎', value: 'zhihu' },
  { label: 'B站', value: 'bilibili' }
]

// 初始化情感分布图
const initSentimentChart = (data) => {
  const chart = echarts.init(sentimentChart.value)
  const option = {
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '情感分布',
        type: 'pie',
        radius: '50%',
        data: [
          { value: data.positive || 0, name: '正面' },
          { value: data.neutral || 0, name: '中性' },
          { value: data.negative || 0, name: '负面' }
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
  chart.setOption(option)
}

// 初始化平台分布图
const initPlatformChart = (data) => {
  const chart = echarts.init(platformChart.value)
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    xAxis: {
      type: 'category',
      data: data.map(item => item.platform)
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '数据量',
        type: 'bar',
        data: data.map(item => item.count)
      }
    ]
  }
  chart.setOption(option)
}

// 初始化趋势图
const initTrendChart = (data) => {
  const chart = echarts.init(trendChart.value)
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['舆情总量', '正面', '负面']
    },
    xAxis: {
      type: 'category',
      data: data.map(item => item.date)
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '舆情总量',
        type: 'line',
        data: data.map(item => item.total)
      },
      {
        name: '正面',
        type: 'line',
        data: data.map(item => item.positive)
      },
      {
        name: '负面',
        type: 'line',
        data: data.map(item => item.negative)
      }
    ]
  }
  chart.setOption(option)
}

// 初始化词云图
const initWordCloudChart = (data) => {
  const chart = echarts.init(wordCloudChart.value)
  const option = {
    tooltip: {
      show: true
    },
    series: [
      {
        type: 'wordCloud',
        shape: 'circle',
        left: 'center',
        top: 'center',
        width: '70%',
        height: '80%',
        right: null,
        bottom: null,
        sizeRange: [12, 60],
        rotationRange: [-90, 90],
        rotationStep: 45,
        gridSize: 8,
        drawOutOfBound: false,
        textStyle: {
          fontFamily: 'sans-serif',
          fontWeight: 'bold',
          color: function () {
            return 'rgb(' + [
              Math.round(Math.random() * 160),
              Math.round(Math.random() * 160),
              Math.round(Math.random() * 160)
            ].join(',') + ')'
          }
        },
        emphasis: {
          focus: 'self',
          textStyle: {
            shadowBlur: 10,
            shadowColor: '#333'
          }
        },
        data: data.map(item => ({
          name: item.word,
          value: item.count
        }))
      }
    ]
  }
  chart.setOption(option)
}

// 获取分析数据
const fetchAnalysisData = async () => {
  try {
    const params = {
      startDate: filterForm.dateRange?.[0],
      endDate: filterForm.dateRange?.[1],
      platform: filterForm.platform,
      trendType: trendType.value
    }
    
    const data = await store.dispatch('opinion/getOpinionStats', params)
    
    // 更新图表
    initSentimentChart(data.sentimentDistribution)
    initPlatformChart(data.platformDistribution)
    initTrendChart(data.trendData)
    initWordCloudChart(data.wordCloudData)
  } catch (error) {
    console.error('获取分析数据失败:', error)
  }
}

// 筛选条件变化
const handleFilterChange = () => {
  fetchAnalysisData()
}

// 趋势图类型变化
const handleTrendTypeChange = () => {
  fetchAnalysisData()
}

onMounted(() => {
  fetchAnalysisData()
  
  // 监听窗口大小变化，重绘图表
  window.addEventListener('resize', () => {
    const charts = [
      sentimentChart.value,
      platformChart.value,
      trendChart.value,
      wordCloudChart.value
    ]
    
    charts.forEach(chart => {
      const instance = echarts.getInstanceByDom(chart)
      instance?.resize()
    })
  })
})
</script>

<style lang="scss" scoped>
.analysis-container {
  .filter-card {
    margin-bottom: 20px;
  }
  
  .chart-row {
    margin-bottom: 20px;
    
    .chart-card {
      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      
      .chart {
        height: 400px;
      }
    }
  }
}
</style> 