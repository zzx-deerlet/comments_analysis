<template>
  <div class="system-container">
    <el-card class="system-card">
      <template #header>
        <div class="card-header">
          <span>系统设置</span>
        </div>
      </template>
      
      <el-form
        ref="systemFormRef"
        :model="systemForm"
        label-width="120px"
      >
        <el-form-item label="系统名称">
          <el-input v-model="systemForm.systemName" />
        </el-form-item>
        
        <el-form-item label="系统Logo">
          <el-upload
            class="logo-uploader"
            action="/api/system/upload"
            :show-file-list="false"
            :on-success="handleLogoSuccess"
          >
            <img v-if="systemForm.logo" :src="systemForm.logo" class="logo" />
            <el-icon v-else class="logo-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        
        <el-form-item label="数据刷新间隔">
          <el-input-number
            v-model="systemForm.refreshInterval"
            :min="1"
            :max="60"
          />
          <span class="unit">分钟</span>
        </el-form-item>
        
        <el-form-item label="数据保留时间">
          <el-input-number
            v-model="systemForm.dataRetention"
            :min="1"
            :max="365"
          />
          <span class="unit">天</span>
        </el-form-item>
        
        <el-form-item label="导出文件格式">
          <el-radio-group v-model="systemForm.exportFormat">
            <el-radio label="excel">Excel</el-radio>
            <el-radio label="csv">CSV</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="数据源配置">
          <el-button type="primary" @click="handleDataSourceConfig">
            配置数据源
          </el-button>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSubmit">保存设置</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 数据源配置对话框 -->
    <el-dialog
      v-model="dataSourceDialogVisible"
      title="数据源配置"
      width="60%"
    >
      <el-form :model="dataSourceForm" label-width="100px">
        <el-form-item label="微博API">
          <el-input v-model="dataSourceForm.weiboApi" placeholder="请输入微博API配置" />
        </el-form-item>
        <el-form-item label="微信API">
          <el-input v-model="dataSourceForm.wechatApi" placeholder="请输入微信API配置" />
        </el-form-item>
        <el-form-item label="知乎API">
          <el-input v-model="dataSourceForm.zhihuApi" placeholder="请输入知乎API配置" />
        </el-form-item>
        <el-form-item label="B站API">
          <el-input v-model="dataSourceForm.bilibiliApi" placeholder="请输入B站API配置" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dataSourceDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleDataSourceSave">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

const store = useStore()
const systemFormRef = ref(null)
const dataSourceDialogVisible = ref(false)

const systemForm = reactive({
  systemName: '多平台舆情分析系统',
  logo: '',
  refreshInterval: 5,
  dataRetention: 30,
  exportFormat: 'excel'
})

const dataSourceForm = reactive({
  weiboApi: '',
  wechatApi: '',
  zhihuApi: '',
  bilibiliApi: ''
})

const handleLogoSuccess = (response) => {
  systemForm.logo = response.url
}

const handleDataSourceConfig = () => {
  dataSourceDialogVisible.value = true
}

const handleDataSourceSave = async () => {
  try {
    await store.dispatch('system/updateDataSource', dataSourceForm)
    ElMessage.success('数据源配置保存成功')
    dataSourceDialogVisible.value = false
  } catch (error) {
    ElMessage.error('数据源配置保存失败')
  }
}

const handleSubmit = async () => {
  try {
    await store.dispatch('system/updateSettings', systemForm)
    ElMessage.success('设置保存成功')
  } catch (error) {
    ElMessage.error('设置保存失败')
  }
}

const handleReset = () => {
  systemFormRef.value?.resetFields()
}
</script>

<style lang="scss" scoped>
.system-container {
  padding: 20px;
  
  .system-card {
    max-width: 800px;
    margin: 0 auto;
  }
  
  .unit {
    margin-left: 10px;
    color: #909399;
  }
  
  .logo-uploader {
    :deep(.el-upload) {
      border: 1px dashed #d9d9d9;
      border-radius: 6px;
      cursor: pointer;
      position: relative;
      overflow: hidden;
      transition: var(--el-transition-duration-fast);
      
      &:hover {
        border-color: var(--el-color-primary);
      }
    }
    
    .logo-uploader-icon {
      font-size: 28px;
      color: #8c939d;
      width: 100px;
      height: 100px;
      text-align: center;
      line-height: 100px;
    }
    
    .logo {
      width: 100px;
      height: 100px;
      display: block;
    }
  }
}
</style>
