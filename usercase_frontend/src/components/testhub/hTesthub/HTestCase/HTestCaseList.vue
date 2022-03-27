<template>
  <div class="case-main">
    <!-- 面包屑 -->
    <div id="case-menu" style="display: flex;justify-content: space-between;border-bottom: solid 1px #e6e6e6;
}
">
      <el-breadcrumb separator-class="el-icon-arrow-right" style="width: 30%">
        <el-breadcrumb-item :to="{ path: '/main/testhub' }">测试库</el-breadcrumb-item>
        <el-breadcrumb-item>{{ testHub.name }}</el-breadcrumb-item>
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
      <el-card class="box-card" style="width: 24%;overflow: auto" id="case-menu-module" ref="caseMenuModule">
        <div slot="header" class="clearfix">
          <span>模块</span>
        </div>

        <div style="text-align: left">
          <el-button type="text" icon="el-icon-s-open" style="padding-left: 5px"
                     @click="getAllTestCase">全部用例
          </el-button>
        </div>

        <el-tree :data="moduleTree" :props="defaultProps" @node-click="handleNodeClick">
          <div class="custom-tree-node" slot-scope="{ node, data }">

            <span>{{ node.label }}</span>
            <span>
<!--            <i class="el-icon-plus" style="margin-left:4px;font-size: 14px;color: dodgerblue" @click.prevent.stop="showAddModuleDialog(0, data.id)"></i>-->
              <!--            <i class="el-icon-edit" style="margin-left:4px;font-size: 14px;color: limegreen" @click.prevent.stop="showEditModuleDialog(data.id)"></i>-->
              <!--            <i class="el-icon-delete" style="margin-left:4px;font-size: 14px;color: orangered" @click.prevent.stop="showDeleteModuleDialog(data.id)"></i>-->
            <el-dropdown @command="handleCommand">
              <span class="el-dropdown-link">
                <i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item :command="{'type': 'add', 'data': data}">添加</el-dropdown-item>
                <el-dropdown-item :command="{'type': 'edit', 'data': data}">编辑</el-dropdown-item>
                <el-dropdown-item :command="{'type': 'delete', 'data': data}">删除</el-dropdown-item>

              </el-dropdown-menu>
            </el-dropdown>
          </span>


          </div>

        </el-tree>
        <el-button type="text" icon="el-icon-plus" style="float: left; padding-left: 5px"
                   @click="showAddModuleDialog(0, 0)">新建模块
        </el-button>
      </el-card>
      <el-card class="box-card" style="width: 75%;overflow: auto">
        <div>
          <el-table
              :data="testCaseList"
              style="width: 100%;margin-top: -10px">
            <el-table-column
                prop="id"
                label="编号"
                width="80">
              <template slot-scope="scope">
                {{ testHub.name }}-{{ scope.row.id }}
              </template>
            </el-table-column>
            <el-table-column
                prop="title"
                min-width="200"
                label="标题">
              <template slot-scope="scope">
                <a href="javascript:void(0)" style="color: #409EFF; font-weight: normal" @click="showTestCase(scope.row.id)">{{ scope.row.title }}</a>
              </template>
            </el-table-column>
            <el-table-column
                prop="status_id"
                label="状态"
                width="100">
              <template slot-scope="scope">
                <span v-if="!scope.row.status_id">
                </span>
                <el-tag v-else :type="getStatus(scope.row.status_id).type" size="small">
                  {{ getStatus(scope.row.status_id).name }}
                </el-tag>

              </template>
            </el-table-column>

            <el-table-column
                prop="creator_name"
                label="创建人"
                width="150">
            </el-table-column>
            <el-table-column
                prop="priority_id"
                label="优先级"
                width="100">
              <template slot-scope="scope">
                <span v-if="!scope.row.priority_id">
                </span>
                <el-tag v-else :type="getPriority(scope.row.priority_id).type" size="small">
                  {{ getPriority(scope.row.priority_id).name }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column
                prop="type_id"
                label="类型"
                width="100">
              <template slot-scope="scope">
                {{ getType(scope.row.type_id).name }}
              </template>
            </el-table-column>
          </el-table>
        </div>

      </el-card>
    </div>
    <HTestModuleDialog v-if="showTestModuleDialogFlag"
                       :test-module-id="testModuleId"
                       :parent-id="testModuleParentId"
                       :test-hub-id="testHubId"
                       @cancel="cancelModule"
                       @success="successModule"
    ></HTestModuleDialog>
    <HTestAddCaseDialog
        v-if="addCaseDialogFlag"
        :test-hub-id="testHubId"
        @cancel="cancelAddCase"
        @success="successAddCase"
    ></HTestAddCaseDialog>
    <el-button type="primary" @click="openAddCaseDialog" round style="position: absolute; right: 20px; bottom: 25px;">创建用例</el-button>

    <el-drawer
        size="40%"
        :modal="false"
        :visible.sync="showCaseDrawerFlag"
        :with-header="false">
      <HTestShowCaseForm
          :test-case-id="testCaseId"
          v-if="showCaseDrawerFlag"
          :test-hub-id="Number(testHubId)">
      </HTestShowCaseForm>
    </el-drawer>
  </div>
</template>

<script>
import TestHubApi from '../../../../request/testHub'
import HTestCaseMap from "../../../../utils/hTestCase"
import HTestModuleDialog from "./HTestModuleDialog.vue"
import HTestAddCaseDialog from "./HTestAddCaseDialog.vue"
import HTestShowCaseForm from "./HTestShowCaseForm";

export default {
  name: "TestCaseList",
  components: {
    HTestModuleDialog,
    HTestAddCaseDialog,
    HTestShowCaseForm
  },
  data() {
    return {
      testCaseId: 0,
      showCaseDrawerFlag: false,
      loading: false,
      testCaseList: [{
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
      testHub: {},
      total: 0,
      query: {
        page: 1,
        size: 5,
        total: 0,
        hTestHubId: 0,
        HModuleIds: "all"
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

      moduleHeight: 500,
      addCaseDialogFlag: false,
    }
  },
  created() {
    console.log("父组件", this.showDailog)
  },
  mounted() {
    this.testHubId = Number(this.$route.params.testhubId);
    this.getTestHubModuleList()
    this.getTestHub()
    this.getTestCase()

    this.moduleHeight = document.body.clientHeight - 100
    document.getElementById('case-menu-module').style.height = this.moduleHeight + 'px'
  },
  methods: {
    showTestCase(testCaseId){
      this.showCaseDrawerFlag = true
      this.testCaseId = testCaseId
    },
    getAllTestCase(){
      this.query.HModuleIds = "all"
      this.getTestCase()
    },
    openAddCaseDialog(){
      this.addCaseDialogFlag = true;
    },
    // 子组件的回调
    cancelAddCase() {
      this.addCaseDialogFlag = false
    },
    successAddCase() {
      this.addCaseDialogFlag = false
      this.getTestCase()
    },
    handleCommand(command) {
      switch (command.type) {
        case 'add':
          this.showAddModuleDialog(0, command.data.id)
          break;
        case 'edit':
          this.showEditModuleDialog(command.data.id)
          break;
        case 'delete':
          this.showDeleteModuleDialog(command.data.id)
          break;
      }
    },
    getStatus(statusId) {
      return HTestCaseMap.getStatus(statusId)
    },
    getPriority(priorityId) {
      return HTestCaseMap.getPriority(priorityId)
    },
    getType(typeId) {
      return HTestCaseMap.getType(typeId)
    },
    async getTestHub() {
      let resp = await TestHubApi.getTestHub(this.testHubId)
      if (resp.success == true) {
        this.testHub = resp.data
      } else {
        this.$message.error(resp.error.message);
      }
    },
    handleNodeClick(data) {
      this.query.HModuleIds = data.id
      this.getTestCase()
    },
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
    },
    showAddModuleDialog(moduleId, parentId) {
      this.testModuleId = moduleId
      this.testModuleParentId = parentId
      this.showTestModuleDialogFlag = true
    },
    showEditModuleDialog(moduleId) {
      this.testModuleId = moduleId
      this.showTestModuleDialogFlag = true
    },
    showDeleteModuleDialog(testModuleId) {
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
    async getTestCase() {
      this.query.hTestHubId = this.testHubId

      const resp = await TestHubApi.getTestCaseList(this.query)
      if (resp.success == true) {
        this.testCaseList = resp.data.testCaseList;
        this.query.total = resp.data.total
      } else {
        this.$message.error(resp.error.message);
      }
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

.case-main .el-tree {
  background: #ffffff !important;
}

.case-main .el-card__body {
  padding: 10px;
}

.case-main .el-card__header {
  padding: 13px 20px;

}
</style>

<style scoped>
.clearfix {
  text-align: left;
}

.custom-tree-node {
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