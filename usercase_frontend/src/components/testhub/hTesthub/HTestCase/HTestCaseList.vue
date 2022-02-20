
<template>
  <div class="case">
    <!-- 面包屑 -->
    <div id="case-menu" style="display: flex;justify-content: space-between;border-bottom: solid 1px #e6e6e6;
}
">
      <el-breadcrumb separator-class="el-icon-arrow-right" style="width: 30%">
        <el-breadcrumb-item :to="{ path: '/main/testhub' }">测试库</el-breadcrumb-item>
        <el-breadcrumb-item>测试库名称 {{ $route.params.testhubId }}</el-breadcrumb-item>
      </el-breadcrumb>

      <div style="margin-top: -20px; width: 30%">
        <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
          <el-menu-item index="htestcase">用例管理</el-menu-item>
          <el-menu-item index="htestplan">测试计划</el-menu-item>
        </el-menu>
      </div>
      <div style="width: 30%"></div>
    </div>
    <div style="display: flex;justify-content: space-between; padding-top: 10px">
      <el-card class="box-card" style="width: 29%">
        <el-tree :data="moduleTree" :props="defaultProps" @node-click="handleNodeClick"></el-tree>
      </el-card>
      <el-card class="box-card" style="width: 70%">
        用例
      </el-card>
    </div>
    <!-- 卡片 -->
  </div>
</template>

<script>
import TestHubApi from '../../../../request/testHub'
// import HTestHubDialog from "./HTestHubDialog.vue"

export default {
  name: "TestCaseList",
  components: {

  },
  data(){
    return {
      loading: false,
      tableData: [],
      showTestHubDailogFlag: false,
      showDeleteDailogFlag: false,
      testHubId: 0,
      total: 0,
      query: {
        page: 1,
        size: 5,
        keyword: "",
      },
      recentTestHubList: [],
      activeIndex: "htestcase",
      moduleTree: [],
      defaultProps: {
        children: 'children',
        label: 'name'
      }
    }
  },
  created() {
    console.log("父组件", this.showDailog)
  },
  mounted() {
    this.getTestHubModuleList()
  },
  methods: {
    handleNodeClick(){

    },
    handleSelect(key, keyPath){
      console.log(key, keyPath);
    },
    showAddDialog(){
      this.showTestHubDailogFlag = true
      this.testHubId = 0
    },
    showEditDialog(testHub){
      this.testHubId = testHub.id
      this.showTestHubDailogFlag = true

    },
    closeAddEDitDialog(){
      this.showTestHubDailogFlag = false
      this.getTestHubList()
    },
    // showDeleteDialog(testHub){
    //   this.$confirm('此操作将永久删除该数据, 是否继续?', '提示', {
    //     confirmButtonText: '确定',
    //     cancelButtonText: '取消',
    //     type: 'warning'
    //   }).then(() => {
    //     // TestHubApi.deleteTestHub(testHub.id).then(resp => {
    //     //   if (resp.success == true) {
    //     //     this.$message.success("删除成功！")
    //     //     this.getTestHubList()
    //     //   } else {
    //     //     this.$message.error("删除失败！");
    //     //   }
    //     // })
    //   }).catch(() => {
    //   });
    // },
    //初始化测试库列表列表
    async getTestHubModuleList() {
      const resp = await TestHubApi.getTestCaseModuleList({testHubId: this.$route.params.testhubId})
      if (resp.success == true) {
        this.moduleTree = resp.data
      } else {
        this.$message.error(resp.error.message);
      }
    },
    //初始化最近测试库列表列表
    async getRecentTestHubList() {
      // const resp = await TestHubApi.getRecentTestHubList()
      // if (resp.success == true) {
      //   this.recentTestHubList = resp.data
      // } else {
      //   this.$message.error(resp.error.message);
      // }
    },

    // 删除一条项目信息
    // async deleteModule(row) {
    //   this.$confirm('是否要删除用例?', '提示', {
    //     confirmButtonText: '确定',
    //     cancelButtonText: '取消',
    //     type: 'warning'
    //   }).then(() => {
    //     // ModuleApi.deleteModule(row.id).then(resp =>{
    //     //   if (resp.success == true) {
    //     //     this.$message.success("删除成功！")
    //     //     this.initModule()
    //     //   } else {
    //     //     this.$message.error("删除失败");
    //     //   }
    //     // })
    //
    //   })
    // },

    // 子组件的回调
    cancelModule() {
      console.log("接收到-子组件关闭")
      this.showDailog = false
      this.moduleId = 0
      //this.initModule()
    },

    // 修改每页显示个数
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`)
      this.query.size = val
      //this.initModule()
    },

    // 点给第几页
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`)
      this.query.page = val
      //this.initModule()
    }

  }

}
</script>

<style>
#case-menu .el-menu.el-menu--horizontal {
  border-bottom: none !important;
}
</style>

<style scoped>
.testhub-recent-item {
  border-left-color: rgb(86, 171, 251);
  background-color: rgba(86, 171, 251, 0.2);
  height: 70px;
  width: 150px;
  margin-top: 5px;
  border-radius: 5px;
  cursor: pointer;
  margin-right: 20px;
}
.testhub-recent-line {
  height: 90px;
  text-align: left;
  /*display: flex;*/
  /*justify-content: space-between;*/
}
.testhub-filter-line {
  height: 50px;
  text-align: left;
  display: flex;
  justify-content: space-between;
}
.foot-page {
  margin-top: 20px;
  float: right;
  margin-bottom: 20px;
}

</style>