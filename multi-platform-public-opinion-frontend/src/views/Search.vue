<template>
  <div class="search-container">
    <!-- 搜索表单 -->
    <el-card class="search-form">
      <el-form :model="searchForm" ref="searchFormRef" :inline="true">
        <el-form-item label="关键词">
          <el-input
            v-model="searchForm.keyword"
            placeholder="请输入关键词"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        
        <el-form-item label="平台">
          <el-select v-model="searchForm.platform" placeholder="请选择平台" clearable>
            <el-option
              v-for="item in platformOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="情感倾向">
          <el-select v-model="searchForm.sentiment" placeholder="请选择情感倾向" clearable>
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
            v-model="searchForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 搜索结果 -->
    <el-card class="search-results">
      <template #header>
        <div class="results-header">
          <span>搜索结果</span>
          <el-button type="primary" @click="handleExport">导出数据</el-button>
        </div>
      </template>
      
      <el-table
        v-loading="loading"
        :data="opinionList"
        style="width: 100%"
        border
      >
        <el-table-column prop="platform" label="平台" width="100" />
        <el-table-column prop="content" label="内容" show-overflow-tooltip />
        <el-table-column prop="sentiment" label="情感倾向" width="100">
          <template #default="{ row }">
            <el-tag :type="getSentimentType(row.sentiment)">
              {{ getSentimentLabel(row.sentiment) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="keywords" label="关键词" width="200">
          <template #default="{ row }">
            <el-tag
              v-for="keyword in row.keywords"
              :key="keyword"
              size="small"
              class="keyword-tag"
            >
              {{ keyword }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="publishTime" label="发布时间" width="180" />
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button
              type="text"
              size="small"
              @click="handleViewDetail(row)"
            >
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    
    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="舆情详情"
      width="60%"
    >
      <div v-if="currentDetail" class="detail-content">
        <div class="detail-item">
          <span class="label">平台：</span>
          <span>{{ currentDetail.platform }}</span>
        </div>
        <div class="detail-item">
          <span class="label">发布时间：</span>
          <span>{{ currentDetail.publishTime }}</span>
        </div>
        <div class="detail-item">
          <span class="label">情感倾向：</span>
          <el-tag :type="getSentimentType(currentDetail.sentiment)">
            {{ getSentimentLabel(currentDetail.sentiment) }}
          </el-tag>
        </div>
        <div class="detail-item">
          <span class="label">关键词：</span>
          <el-tag
            v-for="keyword in currentDetail.keywords"
            :key="keyword"
            size="small"
            class="keyword-tag"
          >
            {{ keyword }}
          </el-tag>
        </div>
        <div class="detail-item">
          <span class="label">内容：</span>
          <div class="content">{{ currentDetail.content }}</div>
        </div>
        <div class="detail-item">
          <span class="label">互动数据：</span>
          <div class="interaction-data">
            <span>评论：{{ currentDetail.replyCount }}</span>
            <span>转发：{{ currentDetail.forwardCount }}</span>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'

const store = useStore()
const searchFormRef = ref(null)
const loading = ref(false)
const detailDialogVisible = ref(false)
const currentDetail = ref(null)

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 搜索表单数据
const searchForm = reactive({
  keyword: '',
  platform: '',
  sentiment: '',
  dateRange: []
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

// 获取情感标签类型
const getSentimentType = (sentiment) => {
  const types = {
    positive: 'success',
    neutral: 'info',
    negative: 'danger'
  }
  return types[sentiment] || 'info'
}

// 获取情感标签文本
const getSentimentLabel = (sentiment) => {
  const labels = {
    positive: '正面',
    neutral: '中性',
    negative: '负面'
  }
  return labels[sentiment] || '未知'
}

// 搜索结果数据
const opinionList = ref([])

// 搜索方法
const handleSearch = () => {
  currentPage.value = 1
  fetchData()
}

// 重置搜索
const handleReset = () => {
  searchFormRef.value?.resetFields()
  handleSearch()
}

// 获取数据
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      ...searchForm,
      page: currentPage.value,
      pageSize: pageSize.value,
      startDate: searchForm.dateRange?.[0],
      endDate: searchForm.dateRange?.[1]
    }
    
    const { list, total: totalCount } = await store.dispatch('opinion/searchOpinions', params)
    opinionList.value = list
    total.value = totalCount
  } catch (error) {
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

// 查看详情
const handleViewDetail = async (row) => {
  try {
    const detail = await store.dispatch('opinion/getOpinionDetail', row.id)
    currentDetail.value = detail
    detailDialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取详情失败')
  }
}

// 导出数据
const handleExport = async () => {
  try {
    const params = {
      ...searchForm,
      startDate: searchForm.dateRange?.[0],
      endDate: searchForm.dateRange?.[1]
    }
    await store.dispatch('opinion/exportOpinions', params)
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

// 分页方法
const handleSizeChange = (val) => {
  pageSize.value = val
  fetchData()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchData()
}

// 初始化
fetchData()
</script>

<style lang="scss" scoped>
.search-container {
  .search-form {
    margin-bottom: 20px;
  }
  
  .search-results {
    .results-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .keyword-tag {
      margin-right: 5px;
    }
    
    .pagination-container {
      margin-top: 20px;
      text-align: right;
    }
  }
  
  .detail-content {
    .detail-item {
      margin-bottom: 15px;
      
      .label {
        font-weight: bold;
        margin-right: 10px;
      }
      
      .content {
        margin-top: 10px;
        line-height: 1.6;
      }
      
      .interaction-data {
        span {
          margin-right: 20px;
        }
      }
    }
  }
}
</style> 