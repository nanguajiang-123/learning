<template>
    <h3>自定义事件组件交互</h3>
    <button @click="sendclickhandle">click</button>
</template>


<script>
export default {
    __name:"mycomponents02",
    data(){
        return {
            msg:"我是components02数据"
        }
    },
    methods:{
        sendclickhandle(){
        this.$emit("onevent",this.msg)
    }
}
}
</script>

<style scoped>
button{
    color: blue
}

</style>