<template>
  <div class="hello">
    <h3>1.hello,模板学习</h3>
    <p>{{ message }}</p>
    <div>{{ rawhtml }}</div>
    <div v-html="rawhtml"></div>
    <div :id="dynamicid"></div>//属性动态化
    <p>{{ num+10 }}</p>
    <p>{{ flag?'真猴子':'假猴子' }}</p>
    
    <h3>2.条件渲染</h3>
    <p v-show="flag">韩婧真的是那只孙猴子吗</p>
    <p v-if="flag">"韩婧是孙猴子"</p>
    <p v-else>韩婧是傻猴子</p>
    <h4>ps：v-if切换开销大，v-show切换开销大，实际上是css的类型改变</h4>


    <h3>3.列表渲染</h3>
    <ul>
      <li v-for="item in items" :key="item.id">
        {{ item.title }}
      </li>
    </ul>
    <h4>ps:为了给vue一个重排提示，必须要给key（每一项唯一拥有）</h4>


    <h3>4.事件处理</h3>
    <button @click="counter+=1">点击:counter={{ counter }}</button>
    <button @click="clickhandle">button</button>
    <p>{{ message }}</p>
    <button @click="say('hi')">say</button>
    <button @click="say('what')">say what</button>
    <ul>
      <li  @click="clickfunc(name)"   v-for="(name,index) in names" :key="index">
        {{ name }}
      </li>
    </ul>



    <h3>5.表单输入绑定,双向绑定</h3>
    <input type="text" v-model.lazy="username">
    <input type="text" v-model.trim="password">
    <button @click="clickgetuserinfo()">获取用户信息</button>
    <h4>ps:v-model实时获取，双向绑定</h4>
    <h4>.lazy当回车或者停止输入时获取，开销小</h4>
    <h4>.trim主动消除前后空格</h4>



    <h3>6.组件基础</h3>
    <h5>a.引入组件</h5>
    <h5>b.挂载组件</h5>
    <h5>c.注入组件</h5>
    <h5>在组件的style里添加scoped属性，就代表只在当前组件中生效</h5>


    <h3>7.组件交互</h3>
    <h4>ps:数组和对象必须使用函数进行返回</h4>


    <h3>8.自定义事件组件交互</h3>




    
    
    






    
  </div>
</template>

<script>
export default {
  //innerhtml，innertext
  name: 'HelloWorld',
  data(){
    return{
      message: "测试",
      rawhtml:"<a href='http://wwww.itbaizhan.com'>百战</a>",
      dynamicid:10001,
      num:10,
      flag:false,
      items:[
        {
          id:1001,
          title:"today_news01"
        },
        {
          id:1002,
          title:"today_news02"
        },
        {
          id:1003,
          title:"today_news03"
        },
        {
          id:1004,
          title:"today_news04"
        }
      ],
      counter:1,
      message:"消息通知",

      names:["iwen","ime","frank"],
      username:"",
      password:""
    }


  },
  methods:{
  clickhandle(event){
    //console.log("hajimicat is cute")，在实践中读取data的属性，是需要通过this.属性
    this.message="消息被撤回了"
    console.log(event);
    event.target.innerHTML = "点击之后"
  },
   say(data){
    console.log(data)

  },
  clickfunc(data){
  console.log(data);
  
  },
  clickgetuserinfo(){
    console.log("username:",this.username)
    console.log("userpssword:",this.password)
  }
}

  
}


</script>


