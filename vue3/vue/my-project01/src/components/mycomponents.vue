<template>
    <h3>我是单文件组件</h3>
    <p>{{ title }}</p>
    <p>{{ age }}</p>
    <ul>
        <li v-for="(name,index) in names" key="index">{{ name }}
        </li>
    </ul>
</template>


<script>
export default{
    __name:"mycomponents",
    props:{
        title:{
            type:String,
            default:""
        },
        age:{
            type:Number,
            //数组和对象必须使用函数进行返回
            default:""
        },
        names:{
            type:Array,
            default:function(){
                return []
            }
        }
    }
}
</script>

<style scoped>
h3{
    color: blanchedalmond;
}

</style>