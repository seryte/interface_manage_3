<template>
  <div class="home">
<!--    <img alt="Vue logo" src="../assets/logo.png">-->
<!--    <HelloWorld msg="Welcome to Your Vue.js App" myProps="hahaha"/>-->
    <div class="left-menu">
     <el-menu
             style="height: 100%"
              :default-active="activeIndex"
              class="el-menu-vertical-demo"
              background-color="#304156"
              text-color="#fff"
              @select="handleSelect"
              active-text-color="#409eff">

              <el-menu-item index="service" style="text-align: left">
                <i class="el-icon-menu"></i>
                <span slot="title">服务</span>
              </el-menu-item>
              <el-menu-item index="task" style="text-align: left">
                <i class="el-icon-setting"></i>
                <span slot="title">任务</span>
              </el-menu-item>

                <el-menu-item index="logout" style="text-align: left">
                <i class="el-icon-user"></i>
                <span slot="title">退出</span>
              </el-menu-item>
    </el-menu>
      </div>
    <div class="right-context">
            <router-view/>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import {logout} from "../request/user";

export default {
  name: 'Home',
  components: {},
    props: {
      menu: String
    },
    data(){
    return {
      activeIndex: "service"
      }
    },
    methods: {
      logoutUser() {
          logout().then(data=>{
                let success = data.data.success;
                if (success) {
                  this.$message({
                    message: '退出成功',
                    type: 'success'
                });
                    this.$router.push("/login")
                }else{
                  this.$notify.error({
                    title: "错误",
                    message: data.data.error.message
                  })
                }
              })
      },
      handleSelect(index, keyPath){
        this.activeIndex = index;
        switch (index) {
            case "logout":
              this.logoutUser();
              break
            case "task":
                this.$router.push("/task")
                break
            case "service":
                this.$router.push("/service")
                break

        }
      }
    },
    created() {
      this.activeIndex = this.menu
    }

}

</script>

<style scoped>
  .home {
    display: flex;
    height: 100%;
  }
  .left-menu {
    width: 10%;
}
  .right-context {
    width: 85%;
  }
</style>