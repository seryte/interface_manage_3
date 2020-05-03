<template>
  <div class="hello">
    {{ msg }}
    {{ message }}
    {{ myProps }}
    <div v-html="htmlMessage"></div>
    <div :id="idMessage" name="hello" :class="classMessage">test</div>
    <div v-if="boolMessage">
      v-if
    </div>
    <div v-else>
      v-else
    </div>
    <div v-show="showMessage">v-show</div>
    <div v-for="item in forMessage" :key="item">{{item}}</div>
    <el-button onclick="alert('纯js事件')">纯js button</el-button>
    <el-button @click="buttonEvent">vue button</el-button>
    <el-input v-model="inputMessage"/>
    <div>{{inputMessage}}</div>
    <el-button @click="inputEvent">input button</el-button>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String,
    myProps: String,
  },
  data(){
    return {
      message: "尼玛",
      htmlMessage: "<span style='color: crimson'>尼玛逼</span>",
      idMessage: "idNiMa",
      classMessage: "classNiMa",

      boolMessage: false,
      showMessage: false,
      forMessage: ["f", "o", "r"],
      inputMessage: "input"
    }
  },
  methods: {
    buttonEvent(){
      this.showMessage = !this.showMessage
    },
    inputEvent(){
      this.inputMessage = "new_input"
    }

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
  .classNiMa{
    color: aqua;
    border: salmon;
  }
</style>
