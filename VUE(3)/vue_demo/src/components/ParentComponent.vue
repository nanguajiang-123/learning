<script setup>
import { ref } from 'vue'
import ChildComponent from './ChildComponent.vue'

// 父组件的数据
const parentMessage = ref('Hello from Parent')
const childMessages = ref([])

// 接收子组件发送的数据
function handleChildMessage(message) {
  childMessages.value.push({
    text: message,
    time: new Date().toLocaleTimeString()
  })
}

// 更新发送给子组件的数据
function updateParentMessage() {
  parentMessage.value = `Updated at ${new Date().toLocaleTimeString()}`
}
</script>

<template>
  <div class="parent-container">
    <div class="parent-box">
      <h2>👨‍👧 Parent Component</h2>
      
      <div class="parent-info">
        <p>Parent Message: <strong>{{ parentMessage }}</strong></p>
        <button @click="updateParentMessage" class="update-btn">
          Update Parent Message
        </button>
      </div>

      <div class="messages-box">
        <h3>Messages from Children:</h3>
        <div v-if="childMessages.length === 0" class="no-messages">
          No messages yet...
        </div>
        <div v-else class="messages-list">
          <div v-for="(msg, index) in childMessages" :key="index" class="message-item">
            <span class="time">{{ msg.time }}</span>
            <span class="text">{{ msg.text }}</span>
          </div>
        </div>
      </div>

      <!-- 传递数据给子组件（父传子） -->
      <ChildComponent
        :parentMessage="parentMessage"
        @send-message="handleChildMessage"
      />
    </div>
  </div>
</template>

<style scoped>
.parent-container {
  padding: 20px;
  background: #f5f5f5;
  border-radius: 10px;
  margin: 20px 0;
}

.parent-box {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.parent-box h2 {
  color: #667eea;
  margin-top: 0;
}

.parent-info {
  background: #f9f9f9;
  padding: 15px;
  border-left: 4px solid #667eea;
  margin-bottom: 20px;
  border-radius: 5px;
}

.parent-info p {
  margin: 0 0 10px 0;
}

.update-btn {
  background: #667eea;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s;
}

.update-btn:hover {
  background: #764ba2;
  transform: translateY(-2px);
}

.messages-box {
  background: #f0f0f0;
  padding: 15px;
  border-radius: 5px;
  margin-bottom: 20px;
}

.messages-box h3 {
  margin-top: 0;
  color: #333;
}

.no-messages {
  color: #999;
  font-style: italic;
}

.messages-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.message-item {
  background: white;
  padding: 10px;
  border-radius: 5px;
  display: flex;
  gap: 10px;
  border-left: 3px solid #764ba2;
}

.time {
  color: #999;
  font-size: 12px;
  min-width: 100px;
}

.text {
  color: #333;
  flex: 1;
}
</style>
