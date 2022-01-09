<template>
  <div class="navigation">
    <el-container style="height: 100%; border: 1px solid #eee">
      <el-aside width="90px" style="background-color: rgb(84, 92, 100); overflow-x: hidden;">
        <!-- <h1>重定向</h1> -->
        <img class="logo" alt="itest logo" src="../assets/quick.svg" />
        <el-menu
          default-active="onRoutes"
          class="el-menu-vertical-demo"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b"
        >
          <!-- 项目管理 -->
          <router-link to="/main/project">
            <el-menu-item index="1">
              <i class="el-icon-menu"></i>
              <span slot="title">项目</span>
            </el-menu-item>
          </router-link>
          <router-link to="/main/module">
            <el-menu-item index="2">
              <i class="el-icon-s-grid"></i>
              <span slot="title">模块</span>
            </el-menu-item>
          </router-link>
          <router-link to="/main/case">
            <el-menu-item index="3">
              <i class="el-icon-s-data"></i>
              <span slot="title">用例</span>
            </el-menu-item>
          </router-link>
          <router-link to="/main/task">
            <el-menu-item index="4">
              <i class="el-icon-s-order"></i>
              <span slot="title">任务</span>
            </el-menu-item>
          </router-link>
          <router-link to="/main/report">
            <el-menu-item index="5">
              <i class="el-icon-s-marketing"></i>
              <span slot="title">报告</span>
            </el-menu-item>
          </router-link>

          <router-link to="/main/testhub">
            <el-menu-item index="6">
              <i class="el-icon-c-scale-to-original"></i>
              <span slot="title">测试库</span>
            </el-menu-item>
          </router-link>

        </el-menu>
        <div class="personal-style">
          <el-dropdown @command="handleCommand">
            <el-avatar> {{user.name}} </el-avatar>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item command="center">个人中心</el-dropdown-item>
              <el-dropdown-item command="setting">设置</el-dropdown-item>
              <el-dropdown-item command="logout">退出</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>

      </el-aside>

      <el-container>

        <el-main>
          <router-view> </router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import UserApi from  "../request/user"

export default {
  computed: {
    onRoutes() {
      if (this.$route.path === '/main/module') {
        return '2'
      } else if (this.$route.path === '/main/case') {
        return '3'
      } else if (this.$route.path === '/main/task') {
        return '4'
      } else if (this.$route.path === '/main/report') {
        return '5'
      } 
      return '1'
    }
  },
  data() {
    return {
      user: {
        'id': '',
        "name": "",
      },
    };
  },
  created() {
    const user = sessionStorage.getItem('user')
    this.user = JSON.parse(user);
  },
  methods: {
    async handleCommand(command) {
      console.log(command);
      if (command === 'logout') {
        const data = {
          'id': this.user.id,
        }
        const res = await UserApi.logout(data)
        if(res.success == true) {
          // sessionStorage.removeItem('user')
          sessionStorage.clear()
          this.$router.push('/login')
        } else {
          this.$message.error(res.error.message)
        }
      }
    }
  }
};
</script>

<style>
.navigation {
  height: 100%;
}

.nav {
  height: 100%;
}
.el-container {
  height: 100%;
}

a {
  text-decoration: none;
}

.router-link-active {
  text-decoration: none;
}

.logo {
  margin-top: 20px;
  margin-bottom: 10px;
  height: 22px;
}
.el-header {
  background-color: #b3c0d1;
  color: #333;
  line-height: 60px;
}

.el-aside {
  color: #333;
}

.el-menu-item {
  margin-left: -10px;
}

.personal-style {
  font-size: 12px;position: absolute; bottom: 10px; left: 25px;cursor: pointer
}
</style>

