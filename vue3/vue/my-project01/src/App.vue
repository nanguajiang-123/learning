<template>
  <img alt="Vue logo" src="./assets/logo.png">
  <HelloWorld msg="Welcome to Your Vue.js App"/>
  <mycomponents :title="title" :age="age" :names="names"/>
  <mycomnents02 @onevent="getdatahandle" />
    <p>{{ msg }}</p>
  

</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import mycomponents from './components/mycomponents.vue';
import mycomnents02 from './components/mycomnents02.vue';

export default {
  name: 'App',
  components: {
    HelloWorld,
    mycomponents,
    mycomnents02
  },
  data(){
    return{
      title:"我是一个标题",
      age:20,
      names:["amy","bob","moke"],
      msg:""
    }
  },
  methods:{
    getdatahandle(data){
      console.log(data)
      this.msg=data;
    }

  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
