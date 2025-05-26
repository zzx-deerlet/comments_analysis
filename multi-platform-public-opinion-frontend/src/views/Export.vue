<template>
  <div class="export-container">
    <!-- 导出配置 -->
    <el-card class="export-config">
      <template #header>
        <div class="card-header">
          <span>导出配置</span>
        </div>
      </template>
      
      <el-form :model="exportForm" ref="exportFormRef" label-width="100px">
        <!-- 数据范围 -->
        <el-form-item label="数据范围" required>
          <el-radio-group v-model="exportForm.range">
            <el-radio label="all">全部数据</el-radio>
            <el-radio label="custom">自定义筛选</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <!-- 自定义筛选条件 -->
        <template v-if="exportForm.range === 'custom'">
          <el-form-item label="关键词">
            <el-input
              v-model="exportForm.keyword"
              placeholder="请输入关键词"
              clearable
            />
          </el-form-item>
          
          <el-form-item label="平台">
            <el-select
              v-model="exportForm.platform"
              placeholder="请选择平台"
              clearable
            >
              <el-option
                v-for="item in platformOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          
          <el-form-item label="情感倾向">
            <el-select
              v-model="exportForm.sentiment"
              placeholder="请选择情感倾向"
              clearable
            >
              <el-option
                v-for="item in sentimentOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          
          <el-form-item label="时间范围">
            <el-date-picker
              v-model="exportForm.dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              value-format="YYYY-MM-DD"
            />
          </el-form-item>
        </template>
        
        <!-- 导出字段 -->
        <el-form-item label="导出字段" required>
          <el-checkbox-group v-model="exportForm.fields">
            <el-checkbox label="platform">平台</el-checkbox>
            <el-checkbox label="content">内容</el-checkbox>
            <el-checkbox label="sentiment">情感倾向</el-checkbox>
            <el-checkbox label="keywords">关键词</el-checkbox>
            <el-checkbox label="publishTime">发布时间</el-checkbox>
            <el-checkbox label="replyCount">评论数</el-checkbox>
            <el-checkbox label="forwardCount">转发数</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        
        <!-- 导出格式 -->
        <el-form-item label="导出格式" required>
          <el-radio-group v-model="exportForm.format">
            <el-radio label="csv">CSV</el-radio>
            <el-radio label="excel">Excel</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <!-- 导出按钮 -->
        <el-form-item>
          <el-button
            type="primary"
            :loading="exporting"
            @click="handleExport"
          >
            开始导出
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 导出历史 -->
    <el-card class="export-history">
      <template #header>
        <div class="card-header">
          <span>导出历史</span>
          <el-button type="text" @click="refreshHistory">刷新</el-button>
        </div>
      </template>
      
      <el-table
        v-loading="loading"
        :data="exportHistory"
        style="width: 100%"
      >
        <el-table-column prop="fileName" label="文件名" />
        <el-table-column prop="createTime" label="导出时间" width="180" />
        <el-table-column prop="fileSize" label="文件大小" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'success' ? 'success' : 'danger'">
              {{ row.status === 'success' ? '成功' : '失败' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button
              v-if="row.status === 'success'"
              type="text"
              size="small"
              @click="handleDownload(row)"
            >
              下载
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'

const store = useStore()
const exportFormRef = ref(null)
const loading = ref(false)
const exporting = ref(false)

// 导出表单数据
const exportForm = reactive({
  range: 'all',
  keyword: '',
  platform: '',
  sentiment: '',
  dateRange: [],
  fields: ['platform', 'content', 'sentiment', 'keywords', 'publishTime'],
  format: 'excel'
})

// 平台选项
const platformOptions = [
  { label: '微博', value: 'weibo' },
  { label: '微信', value: 'wechat' },
  { label: '知乎', value: 'zhihu' },
  { label: 'B站', value: 'bilibili' }
]

// 情感倾向选项
const sentimentOptions = [
  { label: '正面', value: 'positive' },
  { label: '中性', value: 'neutral' },
  { label: '负面', value: 'negative' }
]

// 导出历史数据
const exportHistory = ref([])

// 获取导出历史
const fetchExportHistory = async () => {
  loading.value = true
  try {
    // 这里应该调用获取导出历史的API
    // const data = await store.dispatch('opinion/getExportHistory')
    // exportHistory.value = data
    
    // 模拟数据
    exportHistory.value = [
      {
        fileName: '舆情数据_20240101_20240131.xlsx',
        createTime: '2024-01-31 15:30:00',
        fileSize: '2.5MB',
        status: 'success'
      },
      {
        fileName: '舆情数据_20231201_20231231.xlsx',
        createTime: '2023-12-31 16:45:00',
        fileSize: '3.1MB',
        status: 'success'
      }
    ]
  } catch (error) {
    ElMessage.error('获取导出历史失败')
  } finally {
    loading.value = false
  }
}

// 刷新历史记录
const refreshHistory = () => {
  fetchExportHistory()
}

// 导出数据
const handleExport = async () => {
  if (!exportForm.fields.length) {
    ElMessage.warning('请选择导出字段')
    return
  }
  
  exporting.value = true
  try {
    const params = {
      ...exportForm,
      startDate: exportForm.dateRange?.[0],
      endDate: exportForm.dateRange?.[1]
    }
    
    await store.dispatch('opinion/exportOpinions', params)
    ElMessage.success('导出成功')
    refreshHistory()
  } catch (error) {
    ElMessage.error('导出失败')
  } finally {
    exporting.value = false
  }
}

// 下载文件
const handleDownload = (row) => {
  // 这里应该调用下载文件的API
  // store.dispatch('opinion/downloadExportFile', row.fileName)
  ElMessage.success('开始下载')
}

// 初始化
fetchExportHistory()
</script>

<style lang="scss" scoped>
.export-container {
  .export-config {
    margin-bottom: 20px;
  }
  
  .export-history {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  }
}
</style> 