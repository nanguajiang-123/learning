<script setup>
import { useRouter } from 'vue-router'
import HelloWorld from '@/components/helloworld.vue'

const router = useRouter()

function goToLogin() {
  router.push({ name: 'login' })
}
</script>

<template>
  <div class="home-container">
    <div class="home-header">
      <h1>Vue 3 Learning Demo</h1>
      <button @click="goToLogin" class="login-btn">
        Go to Login 🔐
      </button>
    </div>
    
    <div class="home-content">
      <HelloWorld />
    </div>
  </div>
</template>

<style scoped>
.home-container {
  padding: 20px;
}

.home-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
  color: white;
}

.home-header h1 {
  margin: 0;
  font-size: 28px;
}

.login-btn {
  background: white;
  color: #667eea;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.home-content {
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
</style>
