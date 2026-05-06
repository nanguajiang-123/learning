<script setup>
import { ref } from 'vue'

// 定义 props（接收父组件的数据）
const props = defineProps({
  parentMessage: {
    type: String,
    default: 'No message'
  }
})

// 定义 emit（发送数据给父组件）
const emit = defineEmits(['send-message'])

const childMessage = ref('')

// 子组件发送消息给父组件
function sendMessage() {
  if (childMessage.value.trim() === '') {
    alert('Please enter a message!')
    return
  }
  emit('send-message', childMessage.value)
  childMessage.value = ''
}

// 处理回车键
function handleKeyPress(event) {
  if (event.key === 'Enter') {
    sendMessage()
  }
}
</script>

<template>
  <div class="child-container">
    <h3>👧 Child Component</h3>
    
    <!-- 子组件接收的父组件数据 -->
    <div class="received-message">
      <p>Message from Parent:</p>
      <div class="message-display">
        {{ props.parentMessage }}
      </div>
    </div>

    <!-- 子组件发送数据给父组件 -->
    <div class="send-message">
      <p>Send Message to Parent:</p>
      <div class="input-group">
        <input
          v-model="childMessage"
          type="text"
          placeholder="Type your message..."
          @keypress="handleKeyPress"
          class="message-input"
        />
        <button @click="sendMessage" class="send-btn">
          Send
        </button>
      </div>
    </div>

    <!-- 显示当前消息状态 -->
    <div class="status">
      <p>Current message: <span>{{ childMessage || '(empty)' }}</span></p>
    </div>
  </div>
</template>

<style scoped>
.child-container {
  background: #fff9f0;
  border: 2px dashed #764ba2;
  padding: 15px;
  border-radius: 8px;
  margin-top: 20px;
}

.child-container h3 {
  color: #764ba2;
  margin-top: 0;
}

.received-message {
  background: white;
  padding: 12px;
  border-radius: 5px;
  margin-bottom: 15px;
}

.received-message p {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #666;
}

.message-display {
  background: #f0f0f0;
  padding: 10px;
  border-radius: 4px;
  color: #667eea;
  font-weight: 600;
  word-break: break-word;
}

.send-message {
  background: white;
  padding: 12px;
  border-radius: 5px;
  margin-bottom: 15px;
}

.send-message p {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #666;
}

.input-group {
  display: flex;
  gap: 8px;
}

.message-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  transition: all 0.3s;
}

.message-input:focus {
  outline: none;
  border-color: #764ba2;
  box-shadow: 0 0 0 2px rgba(118, 75, 162, 0.1);
}

.send-btn {
  background: #764ba2;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 600;
}

.send-btn:hover {
  background: #667eea;
  transform: translateY(-2px);
}

.status {
  background: #f0f0f0;
  padding: 10px;
  border-radius: 4px;
  font-size: 13px;
  color: #666;
}

.status p {
  margin: 0;
}

.status span {
  color: #764ba2;
  font-weight: 600;
}
</style>
