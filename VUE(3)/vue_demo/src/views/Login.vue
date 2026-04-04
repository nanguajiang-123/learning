<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const email = ref('')
const password = ref('')
const isPasswordVisible = ref(false)

// 计算属性：验证表单是否有效（涉及你学的 computed）
const isFormValid = computed(() => {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailPattern.test(email.value) && password.value.length >= 6
})

// 计算属性：登录按钮的样式类（涉及类与样式绑定）
const submitButtonClass = computed(() => ({
  'btn-active': isFormValid.value,
  'btn-disabled': !isFormValid.value
}))

// 提交表单
function handleLogin() {
  if (isFormValid.value) {
    // 模拟登录成功，跳转到欢迎页面
    router.push({
      name: 'welcome',
      params: { username: email.value.split('@')[0] }
    })
  }
}

// 切换密码显示
function togglePasswordVisibility() {
  isPasswordVisible.value = !isPasswordVisible.value
}
</script>

<template>
  <div class="login-container">
    <div class="login-box">
      <h1 class="login-title">Welcome</h1>
      <p class="login-subtitle">Sign in to your account</p>

      <form @submit.prevent="handleLogin" class="login-form">
        <!-- Email 输入框 -->
        <div class="form-group">
          <label for="email" class="form-label">Email Address</label>
          <input
            id="email"
            v-model="email"
            type="email"
            placeholder="Enter your email"
            class="form-input"
          />
        </div>

        <!-- Password 输入框 -->
        <div class="form-group">
          <label for="password" class="form-label">Password</label>
          <div class="password-wrapper">
            <input
              id="password"
              v-model="password"
              :type="isPasswordVisible ? 'text' : 'password'"
              placeholder="Enter your password"
              class="form-input"
            />
            <button
              type="button"
              class="toggle-password-btn"
              @click="togglePasswordVisibility"
            >
              {{ isPasswordVisible ? '👁️ Hide' : '👁️ Show' }}
            </button>
          </div>
          <p v-if="password.length > 0 && password.length < 6" class="error-text">
            Password must be at least 6 characters
          </p>
        </div>

        <!-- 表单验证提示 -->
        <div v-if="email && !email.includes('@')" class="error-text">
          Please enter a valid email address
        </div>

        <!-- 登录按钮 -->
        <button
          type="submit"
          :class="submitButtonClass"
          class="submit-btn"
          :disabled="!isFormValid"
        >
          {{ isFormValid ? 'Sign In' : 'Fill in all fields' }}
        </button>
      </form>

      <!-- 表单状态显示 -->
      <div class="form-status">
        <p v-if="email && password" class="status-info">
          Current email: <span>{{ email }}</span>
        </p>
        <p class="validation-status">
          Form valid: <span :class="isFormValid ? 'valid' : 'invalid'">
            {{ isFormValid ? '✓ Valid' : '✗ Invalid' }}
          </span>
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.login-box {
  background: white;
  border-radius: 10px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  padding: 40px;
  width: 100%;
  max-width: 400px;
}

.login-title {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  margin: 0 0 10px 0;
  text-align: center;
}

.login-subtitle {
  font-size: 14px;
  color: #999;
  text-align: center;
  margin: 0 0 30px 0;
}

.login-form {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #555;
  margin-bottom: 8px;
}

.form-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  font-size: 14px;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.password-wrapper {
  position: relative;
}

.toggle-password-btn {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #667eea;
  cursor: pointer;
  font-size: 12px;
  padding: 0;
  transition: color 0.3s;
}

.toggle-password-btn:hover {
  color: #764ba2;
}

.error-text {
  color: #e74c3c;
  font-size: 12px;
  margin-top: 5px;
}

.submit-btn {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-active:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
}

.btn-disabled {
  background: #e0e0e0;
  color: #999;
  cursor: not-allowed;
}

.form-status {
  background: #f5f5f5;
  border-radius: 5px;
  padding: 15px;
  font-size: 13px;
  color: #666;
}

.form-status p {
  margin: 8px 0;
}

.form-status span {
  font-weight: 600;
  color: #667eea;
}

.status-info span {
  color: #764ba2;
  word-break: break-all;
}

.valid {
  color: #27ae60 !important;
}

.invalid {
  color: #e74c3c !important;
}
</style>
