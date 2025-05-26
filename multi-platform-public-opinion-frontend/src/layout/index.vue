<template>
  <div class="app-wrapper">
    <!-- 侧边栏 -->
    <div class="sidebar-container">
      <div class="logo">
        <h1>多平台舆情分析系统</h1>
      </div>
      <el-menu
        :default-active="activeMenu"
        class="sidebar-menu"
        :router="true"
        :collapse="isCollapse"
      >
        <el-menu-item index="/dashboard">
          <el-icon><Odometer /></el-icon>
          <template #title>数据概览</template>
        </el-menu-item>
        
        <el-menu-item index="/search">
          <el-icon><Search /></el-icon>
          <template #title>舆情搜索</template>
        </el-menu-item>
        
        <el-menu-item index="/analysis">
          <el-icon><DataAnalysis /></el-icon>
          <template #title>数据分析</template>
        </el-menu-item>
        
        <el-menu-item index="/export">
          <el-icon><Download /></el-icon>
          <template #title>数据导出</template>
        </el-menu-item>
        
        <el-sub-menu index="system">
          <template #title>
            <el-icon><Setting /></el-icon>
            <span>系统管理</span>
          </template>
          <el-menu-item index="/system">系统设置</el-menu-item>
          <el-menu-item index="/user">用户管理</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </div>
    
    <!-- 主要内容区 -->
    <div class="main-container">
      <!-- 顶部导航栏 -->
      <div class="navbar">
        <div class="left">
          <el-icon
            class="collapse-btn"
            @click="toggleSidebar"
          >
            <Fold v-if="!isCollapse" />
            <Expand v-else />
          </el-icon>
        </div>
        <div class="right">
          <el-dropdown trigger="click">
            <span class="user-info">
              {{ username }}
              <el-icon><CaretBottom /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="$router.push('/profile')">
                  个人资料
                </el-dropdown-item>
                <el-dropdown-item divided @click="handleLogout">
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
      
      <!-- 内容区 -->
      <div class="app-main">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useStore } from 'vuex'
import {
  Odometer,
  Search,
  DataAnalysis,
  Download,
  Setting,
  Fold,
  Expand,
  CaretBottom
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const store = useStore()

const isCollapse = ref(false)
const username = computed(() => store.state.user.username)

const activeMenu = computed(() => route.path)

const toggleSidebar = () => {
  isCollapse.value = !isCollapse.value
}

const handleLogout = async () => {
  try {
    await store.dispatch('user/logout')
    router.push('/login')
  } catch (error) {
    console.error('退出登录失败:', error)
  }
}
</script>

<style lang="scss" scoped>
.app-wrapper {
  display: flex;
  height: 100vh;
  
  .sidebar-container {
    width: 240px;
    height: 100%;
    background-color: #304156;
    transition: width 0.3s;
    
    &.collapse {
      width: 64px;
    }
    
    .logo {
      height: 60px;
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: #2b3649;
      
      h1 {
        color: #fff;
        font-size: 18px;
        margin: 0;
        white-space: nowrap;
      }
    }
    
    .sidebar-menu {
      border-right: none;
      background-color: transparent;
      
      :deep(.el-menu-item),
      :deep(.el-sub-menu__title) {
        color: #bfcbd9;
        
        &:hover {
          color: #fff;
          background-color: #263445;
        }
        
        &.is-active {
          color: #409eff;
          background-color: #263445;
        }
      }
    }
  }
  
  .main-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    
    .navbar {
      height: 60px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;
      background-color: #fff;
      box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
      
      .collapse-btn {
        font-size: 20px;
        cursor: pointer;
        
        &:hover {
          color: #409eff;
        }
      }
      
      .user-info {
        display: flex;
        align-items: center;
        cursor: pointer;
        
        .el-icon {
          margin-left: 5px;
        }
      }
    }
    
    .app-main {
      flex: 1;
      padding: 20px;
      overflow-y: auto;
      background-color: #f0f2f5;
    }
  }
}
</style> 