
<template>
  <div class="case-main">
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
      <el-card class="box-card" style="width: 24%">
        <div slot="header" class="clearfix">
          <span>模块</span>
        </div>

        <el-tree :data="moduleTree" :props="defaultProps" @node-click="handleNodeClick">
          <div class="custom-tree-node" slot-scope="{ node, data }">

        <span>{{ node.label }}</span>
        <span>
          <i class="el-icon-plus" style="margin-left:4px;font-size: 14px;color: dodgerblue" @click.prevent.stop="showAddModuleDialog(0, data.id)"></i>
          <i class="el-icon-edit" style="margin-left:4px;font-size: 14px;color: limegreen" @click.prevent.stop="showEditModuleDialog(data.id)"></i>
          <i class="el-icon-delete" style="margin-left:4px;font-size: 14px;color: orangered" @click.prevent.stop="showDeleteModuleDialog(data.id)"></i>

        </span>
      </div>

        </el-tree>
        <el-button type="text" icon="el-icon-plus" style="float: left; padding-left: 5px"
                   @click="showAddModuleDialog(0, 0)">新建模块</el-button>
      </el-card>
      <el-card class="box-card" style="width: 75%">
        <div>
          <el-table
              :data="tableData"
              style="width: 100%;margin-top: -10px">
            <el-table-column
                prop="date"
                label="日期"
                width="180">
            </el-table-column>
            <el-table-column
                prop="name"
                label="姓名"
                width="180">
            </el-table-column>
            <el-table-column
                prop="address"
                label="地址">
            </el-table-column>
          </el-table>
        </div>

      </el-card>
    </div>
    <HTestModuleDialog v-if="showTestModuleDialogFlag"
                       :test-module-id="testModuleId"
                       :parent-id="testModuleParentId"
                       @cancel="cancelModule"
                       @sccess="successModule"
    ></HTestModuleDialog>
  </div>
</template>

<script>
import TestHubApi from '../../../../request/testHub'
import HTestModuleDialog from "./HTestModuleDialog.vue"

export default {
  name: "TestCaseList",
  components: {
    HTestModuleDialog
  },
  data(){
    return {
      loading: false,
      tableData: [{
        date: '2016-05-02',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }, {
        date: '2016-05-04',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1517 弄'
      }, {
        date: '2016-05-01',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1519 弄'
      }, {
        date: '2016-05-03',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1516 弄'
      }],

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
      },
      testModuleId: 0,
      testModuleParentId: 0,
      showTestModuleDialogFlag: false,
      showDeleteDialogFlag: false,
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
    showAddModuleDialog(moduleId, parentId){
      this.testModuleId = moduleId
      this.testModuleParentId = parentId
      this.showTestModuleDialogFlag = true
    },
    showEditModuleDialog(moduleId){
      this.testModuleId = moduleId
      this.showTestModuleDialogFlag = true
    },
    showDeleteModuleDialog(testModuleId){
      this.$confirm('此操作将永久删除该数据, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        TestHubApi.deleteTestCaseModule(testModuleId).then(resp => {
          if (resp.success == true) {
            this.$message.success("删除成功！")
            this.getTestHubModuleList()
          } else {
            this.$message.error("删除失败！");
          }
        })
      }).catch(() => {
      });
    },
    // 子组件的回调
    cancelModule() {
      this.showTestModuleDialogFlag = false
    },
    successModule() {
      this.showTestModuleDialogFlag = false
      this.getTestHubModuleList()
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

.case-main .el-tree {
  background: #ffffff !important;
}

.case-main .el-card__body{
  padding: 10px;
}

.case-main .el-card__header{
  padding: 13px 20px;

}
</style>

<style scoped>
.clearfix{
  text-align: left;
}
.custom-tree-node{
  display: flex;
  justify-content: space-between;
  flex-grow: 100;
}
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