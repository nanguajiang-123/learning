<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

// 获取用户名，如果没有就显示 Guest
const username = computed(() => {
  return route.params.username || 'Guest'
})

const currentTime = ref(new Date().toLocaleString())

// 更新当前时间（演示 ref 和定时器的使用）
setInterval(() => {
  currentTime.value = new Date().toLocaleString()
}, 1000)

// 退出登录
function handleLogout() {
  router.push({ name: 'hello' })
}
</script>

<template>
  <div class="welcome-container">
    <div class="welcome-card">
      <h1 class="welcome-title">Welcome, {{ username }}! 🎉</h1>
      <p class="welcome-subtitle">You have successfully logged in</p>
      
      <div class="current-time">
        <p>Current Time: {{ currentTime }}</p>
      </div>

      <div class="welcome-content">
        <p>This is a blank welcome page after successful login.</p>
        <p>You can build your dashboard or home page here.</p>
      </div>

      <button @click="handleLogout" class="logout-btn">
        Logout
      </button>
    </div>
  </div>
</template>

<style scoped>
.welcome-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.welcome-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  padding: 50px;
  text-align: center;
  max-width: 500px;
}

.welcome-title {
  font-size: 32px;
  color: #667eea;
  margin: 0 0 10px 0;
}

.welcome-subtitle {
  font-size: 16px;
  color: #999;
  margin: 0 0 30px 0;
}

.current-time {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 5px;
  margin: 20px 0;
  font-size: 14px;
  color: #666;
}

.welcome-content {
  margin: 30px 0;
  line-height: 1.6;
  color: #666;
}

.logout-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 5px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.logout-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
}
</style>
