  <template>
    <div class="profile-container">
      <el-card class="profile-card">
        <template #header>
          <div class="card-header">
            <span>个人资料</span>
          </div>
        </template>
        
        <el-form
          ref="profileForm"
          :model="profileForm"
          :rules="rules"
          label-width="100px"
        >
          <el-form-item label="用户名" prop="username">
            <el-input v-model="profileForm.username" disabled />
          </el-form-item>
          
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="profileForm.email" />
          </el-form-item>
          
          <el-form-item label="手机号" prop="phone">
            <el-input v-model="profileForm.phone" />
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="handleSubmit">保存修改</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </template>

  <script setup>
  import { ref, reactive } from 'vue'
  import { useStore } from 'vuex'
  import { ElMessage } from 'element-plus'

  const store = useStore()
  const profileForm = reactive({
    username: '',
    email: '',
    phone: ''
  })

  const rules = {
    email: [
      { required: true, message: '请输入邮箱地址', trigger: 'blur' },
      { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
    ],
    phone: [
      { required: true, message: '请输入手机号', trigger: 'blur' },
      { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
    ]
  }

  const handleSubmit = async () => {
    try {
      await store.dispatch('user/updateProfile', profileForm)
      ElMessage.success('保存成功')
    } catch (error) {
      ElMessage.error('保存失败')
    }
  }
  </script>

  <style lang="scss" scoped>
  .profile-container {
    padding: 20px;
    
    .profile-card {
      max-width: 600px;
      margin: 0 auto;
    }
  }
  </style>

