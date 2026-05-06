<script setup>
import { ref, computed ,watch} from 'vue'
import ParentComponent from './ParentComponent.vue'

const count = ref(0)
function increment() {
    count.value++
    console.log(count.value)
}




//若我们将同样的函数定义为一个方法而不是计算属性，两种方式在结果上确实是完全相同的，然而，不同之处在于计算属性值会基于其响应式依赖被缓存。
const firstName = ref('John')
const lastName = ref('Doe')
const fullName = computed({
    // getter
    get() {
        return firstName.value + ' ' + lastName.value
    },
    // setter
    set(newValue) {
        // 注意：我们这里使用的是解构赋值语法
        [firstName.value, lastName.value] = newValue.split(' ')
    }
})


//3.类与样式绑定
const isActive = ref(false)
const error = ref(null)

const classObject = computed(() => ({
    active: isActive.value && !error.value,
    'text-danger': error.value && error.value.type === 'fatal'
}))


//4.在内联事件处理中访问事件参数
function warn(message, event) {
    // 这里可以访问原生事件
    if (event) {
        event.preventDefault()
    }
    alert(message)
}



const checked = ref(true)
function cheked() {
    console.log(checked.value)
}


const checkedNames = ref([])


const picked = ref("")

const selected = ref("")


// 数据侦听(监听，校验数据)
watch([picked,selected],(newx,oldx)=>{
    console.log('new','old');
    console.log("111")
    console.log(newx,oldx)
    console.log(newx+oldx)
});

</script>



<template>
    <div>
        <button @click="increment">{{ count }}</button>
    </div>
    <div>
        <input v-model="firstName" placeholder="姓" />
        <input v-model="lastName" placeholder="名" />
        <input v-model="fullName" placeholder="全名" />
        <p>姓：{{ firstName }}</p>
        <p>名：{{ lastName }}</p>
        <p>全名：{{ fullName }}</p>
    </div>



    <div class="{active:isActive}"></div>



    <!-- 3 -->
    <div :class="classObject">
        <p>what is this</p>
    </div>



    <!-- 4.使用特殊的 $event 变量 -->
    <button @click="warn('Form cannot be submitted yet.', $event)">
        Submit
    </button>

    //<!-- 使用内联箭头函数 -->
    <button @click="(event) => warn('Form cannot be submitted yet.', event)">
        Submit
    </button>




    <!-- //5.时间修饰符 -->
    <!-- 单击事件将停止传递 -->
    <a @click.stop="doThis"></a>

    <!-- 提交事件将不再重新加载页面 -->
    <form @submit.prevent="onSubmit"></form>

    <!-- 修饰语可以使用链式书写 -->
    <a @click.stop.prevent="doThat"></a>

    <!-- 也可以只有修饰符 -->
    <form @submit.prevent></form>

    <!-- 仅当 event.target 是元素本身时才会触发事件处理器 -->
    <!-- 例如：事件处理器不来自子元素 -->
    <div @click.self="doThat">...</div>
    <!-- 添加事件监听器时，使用 `capture` 捕获模式 -->
    <!-- 例如：指向内部元素的事件，在被内部元素处理前，先被外部处理 -->
    <div @click.capture="doThis">...</div>

    <!-- 点击事件最多被触发一次 -->
    <a @click.once="doThis"></a>

    <!-- 滚动事件的默认行为 (scrolling) 将立即发生而非等待 `onScroll` 完成 -->
    <!-- 以防其中包含 `event.preventDefault()` -->
    <div @scroll.passive="onScroll">...</div>
    <!-- 仅在 `key` 为 `Enter` 时调用 `submit` -->
    <input @keyup.enter="submit" />


    <!-- 6.表单输入绑定单行文本-->
    <p>Message is: {{ message }}</p>
    <input v-model="message" placeholder="edit me" />
    <!-- 多行文本 -->
    <div>
        <span>Multiline message is:</span>
        <p style="white-space: pre-line;">{{ message }}</p>
        <textarea v-model="message" placeholder="add multiple lines"></textarea>
    </div>

    <div>
        <input type="checkbox" v-model="checked" @click="cheked" />
        <label>{{ checked }}</label>
    </div>


    <div>
        <div>Checked names: {{ checkedNames }}</div>

        <input type="checkbox" id="jack" value="Jack" v-model="checkedNames" />
        <label for="jack">Jack</label>

        <input type="checkbox" id="john" value="John" v-model="checkedNames" />
        <label for="john">John</label>

        <input type="checkbox" id="mike" value="Mike" v-model="checkedNames" />
        <label for="mike">Mike</label>
    </div>

    <div>
        <div>Picked: {{ picked }}</div>

        <input type="radio" id="one" value="One" v-model="picked" />
        <label for="one">One</label>

        <input type="radio" id="two" value="Two" v-model="picked" />
        <label for="two">Two</label>
    </div>

    <div>
        <div>Selected: {{ selected }}</div>

        <select v-model="selected">
            <option disabled value="">Please select one</option>
            <option>A</option>
            <option>B</option>
            <option>C</option>
        </select>
    </div>

    <div>
        <!-- 在 "change" 事件后同步更新而不是 "input" -->
        <input v-model.lazy="msg" />
    </div>
    <!-- 默认自动去除用户输入内容中两端的空格 -->
    <div>

        <input v-model.trim="msg" />
    </div>

    <!-- 7. 父传子、子传父通信示例 -->
    <div style="margin-top: 30px; padding: 20px; background: #f0f0f0; border-radius: 8px;">
        <h2 style="color: #667eea; margin-top: 0;">Props & Emit - Parent-Child Communication</h2>
        <ParentComponent />
    </div>

</template>

<!-- 
<script>
    import {ref} from 'vue'
    export default{
        setup(){
        const count = ref(0)
        function increment(){
            count.value++
            console.log(count.value)
        
        }
        return {
        count,
        increment
        }
    }
    }
</script> -->







<style>
.active {
    color: blue;
}
</style>