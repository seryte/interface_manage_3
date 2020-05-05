<!--入口模板文件一般不动这个文件-->
<template>
  <div id="app">
<!--    页面加载均是App.vue + 自定义-->
    <router-view/>
  </div>
</template>


<script>
    import {getLoginUserInfo} from "./request/user";

    export default {
        name: "App",
        comments: {},
        data() {
            return {

            }
        },
        methods: {},
        created() {
            getLoginUserInfo().then(data => {
                let success = data.data.success
                if (!success){
                    // 未校验通过重定向到登录页面
                    this.$router.push("/login")
                }
            })
        },
    }
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100%;
  overflow: auto;
}

html, body{
    height: 100%;
}
#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
