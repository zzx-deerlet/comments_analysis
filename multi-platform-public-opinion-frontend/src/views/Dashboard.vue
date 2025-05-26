<template>
  <div class="dashboard-container">
    <!-- 数据卡片 -->
    <el-row :gutter="20" class="data-cards">
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>今日舆情总量</span>
            </div>
          </template>
          <div class="card-content">
            <h2>{{ stats.todayCount }}</h2>
            <div class="trend">
              <span :class="{ 'up': stats.todayTrend > 0, 'down': stats.todayTrend < 0 }">
                {{ Math.abs(stats.todayTrend) }}%
              </span>
              较昨日
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>情感分布</span>
            </div>
          </template>
          <div class="card-content">
            <div class="sentiment-distribution">
              <div class="sentiment-item">
                <span class="label">正面</span>
                <span class="value">{{ stats.positiveCount }}</span>
              </div>
              <div class="sentiment-item">
                <span class="label">中性</span>
                <span class="value">{{ stats.neutralCount }}</span>
              </div>
              <div class="sentiment-item">
                <span class="label">负面</span>
                <span class="value">{{ stats.negativeCount }}</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>平台分布</span>
            </div>
          </template>
          <div class="card-content">
            <div class="platform-distribution">
              <div v-for="(item, index) in stats.platformDistribution" :key="index" class="platform-item">
                <span class="label">{{ item.platform }}</span>
                <span class="value">{{ item.count }}</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>热点话题</span>
            </div>
          </template>
          <div class="card-content">
            <div class="hot-topics">
              <div v-for="(topic, index) in stats.hotTopics" :key="index" class="topic-item">
                <span class="rank">{{ index + 1 }}</span>
                <span class="name">{{ topic.name }}</span>
                <span class="count">{{ topic.count }}</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 图表区域 -->
    <el-row :gutter="20" class="charts-container">
      <el-col :span="16">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>舆情趋势</span>
              <el-radio-group v-model="trendTimeRange" size="small">
                <el-radio-button label="day">日</el-radio-button>
                <el-radio-button label="week">周</el-radio-button>
                <el-radio-button label="month">月</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div class="chart" ref="trendChart"></div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>情感分布</span>
            </div>
          </template>
          <div class="chart" ref="sentimentChart"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { useStore } from 'vuex'
import * as echarts from 'echarts'

const store = useStore()
const trendChart = ref(null)
const sentimentChart = ref(null)
const trendTimeRange = ref('day')

const stats = reactive({
  todayCount: 0,
  todayTrend: 0,
  positiveCount: 0,
  neutralCount: 0,
  negativeCount: 0,
  platformDistribution: [],
  hotTopics: []
})

// 初始化趋势图
const initTrendChart = () => {
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
      data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '舆情总量',
        type: 'line',
        data: [120, 132, 101, 134, 90, 230, 210]
      },
      {
        name: '正面',
        type: 'line',
        data: [220, 182, 191, 234, 290, 330, 310]
      },
      {
        name: '负面',
        type: 'line',
        data: [150, 232, 201, 154, 190, 330, 410]
      }
    ]
  }
  chart.setOption(option)
}

// 初始化情感分布图
const initSentimentChart = () => {
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
          { value: 1048, name: '正面' },
          { value: 735, name: '中性' },
          { value: 580, name: '负面' }
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

// 获取统计数据
const fetchStats = async () => {
  try {
    const data = await store.dispatch('opinion/getOpinionStats')
    Object.assign(stats, data)
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

onMounted(() => {
  fetchStats()
  initTrendChart()
  initSentimentChart()
  
  // 监听窗口大小变化，重绘图表
  window.addEventListener('resize', () => {
    const trendChartInstance = echarts.getInstanceByDom(trendChart.value)
    const sentimentChartInstance = echarts.getInstanceByDom(sentimentChart.value)
    trendChartInstance?.resize()
    sentimentChartInstance?.resize()
  })
})
</script>

<style lang="scss" scoped>
.dashboard-container {
  .data-cards {
    margin-bottom: 20px;
    
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .card-content {
      text-align: center;
      
      h2 {
        margin: 10px 0;
        font-size: 24px;
      }
      
      .trend {
        font-size: 14px;
        color: #909399;
        
        .up {
          color: #67C23A;
        }
        
        .down {
          color: #F56C6C;
        }
      }
      
      .sentiment-distribution,
      .platform-distribution {
        .sentiment-item,
        .platform-item {
          display: flex;
          justify-content: space-between;
          margin: 10px 0;
          
          .label {
            color: #606266;
          }
          
          .value {
            font-weight: bold;
          }
        }
      }
      
      .hot-topics {
        .topic-item {
          display: flex;
          align-items: center;
          margin: 10px 0;
          
          .rank {
            width: 20px;
            height: 20px;
            line-height: 20px;
            text-align: center;
            background-color: #f0f2f5;
            border-radius: 4px;
            margin-right: 10px;
          }
          
          .name {
            flex: 1;
            margin-right: 10px;
          }
          
          .count {
            color: #909399;
          }
        }
      }
    }
  }
  
  .charts-container {
    .chart {
      height: 400px;
    }
  }
}
</style> 