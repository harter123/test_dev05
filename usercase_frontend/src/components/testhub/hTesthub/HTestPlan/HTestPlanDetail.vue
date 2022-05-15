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
          <el-menu-item index="testcase">用例管理</el-menu-item>
          <el-menu-item index="testplan">测试计划</el-menu-item>
        </el-menu>
      </div>
      <div style="width: 30%"></div>
    </div>

    <div class="status-bar">
      <div>
        <a class="class-a" href="javascript:void(0)" style="margin-right: 10px" @click="back">
          <i class="el-icon-back"></i></a>
        <el-button type="primary" size="mini" @click="showPlanningFlag=true">规划用例</el-button>
      </div>
      <div class="common-flex">

        <el-dropdown trigger="click" @command="handleCommandPlanStatus">
          <span class="el-dropdown-link" style="cursor: pointer">
            <span>状态:</span>
            <el-tag :type="getPlanStatus(testPlan.status_id).type" size="small">
              {{ getPlanStatus(testPlan.status_id).name }}
            </el-tag>
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item v-for="item in getPlanStatusList()" :key="item.id" :command="item.id">
              <el-tag :type="item.type" size="small">{{ item.name }}</el-tag>
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>

      </div>
      <div class="common-flex">
        <div>负责人: {{ testPlan.owner_name }}</div>
      </div>
      <div style="padding-top: 2px">
        <el-popover
            placement="top-start"
            width="70"
            trigger="hover">
          <div>
            <div class="common-flex">
              <div>成功：&nbsp;{{ testPlan.success_num }}</div>
            </div>
            <div class="common-flex">
              <div>跳过：&nbsp;{{ testPlan.skip_num }}</div>
            </div>
            <div class="common-flex">
              <div>阻塞：&nbsp;{{ testPlan.block_num }}</div>
            </div>
            <div class="common-flex">
              <div>失败：&nbsp;{{ testPlan.failed_num }}</div>
            </div>
          </div>
          <div slot="reference" class="common-flex">
            <div>覆盖率:</div>
            <div style="width: 100px">
              <el-progress :text-inside="true" :stroke-width="18" :percentage="testPlan.runRate"></el-progress>
            </div>

          </div>
        </el-popover>

      </div>

      <div style="padding-top: 2px">
        <el-popover
            placement="top-start"
            width="70"
            trigger="hover">
          <div>
            <div class="common-flex">
              <div>成功：&nbsp;{{ testPlan.success_num }}</div>
            </div>
            <div class="common-flex">
              <div>跳过：&nbsp;{{ testPlan.skip_num }}</div>
            </div>
            <div class="common-flex">
              <div>阻塞：&nbsp;{{ testPlan.block_num }}</div>
            </div>
            <div class="common-flex">
              <div>失败：&nbsp;{{ testPlan.failed_num }}</div>
            </div>
          </div>
          <div slot="reference" class="common-flex">
            <div>通过率:</div>
            <div style="width: 100px">
              <el-progress :text-inside="true" :stroke-width="18" :percentage="testPlan.successRate"
                           status="success"></el-progress>

            </div>
          </div>
        </el-popover>
      </div>
      <div class="common-flex">
        <a class="class-a" href="javascript:void(0)"><i class="el-icon-pie-chart"></i>测试报告</a>
      </div>
    </div>
    <div style="display: flex;justify-content: space-between;">
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
          <div class="custom-tree-node" slot-scope="{ node }">
            <span>{{ node.label }}</span>
          </div>

        </el-tree>
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
                <a href="javascript:void(0)"
                   style="color: #409EFF; font-weight: normal; display: flex; align-items: center"
                   @click="showTestCase(scope.row.h_test_case_id)">
                  <svg style="width: 15px; height: 15px" t="1648959546637" class="icon" viewBox="0 0 1024 1024"
                       version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="43792" width="200" height="200">
                    <path
                        d="M853.333333 0h-512C273.066667 0 213.333333 59.733333 213.333333 128v597.333333c0 68.266667 59.733333 128 128 128h512c68.266667 0 128-59.733333 128-128v-597.333333C981.333333 59.733333 921.6 0 853.333333 0z m42.666667 725.333333c0 25.6-17.066667 42.666667-42.666667 42.666667h-512c-25.6 0-42.666667-17.066667-42.666666-42.666667v-597.333333c0-25.6 17.066667-42.666667 42.666666-42.666667h512c25.6 0 42.666667 17.066667 42.666667 42.666667v597.333333zM768 512h-341.333333c-25.6 0-42.666667 17.066667-42.666667 42.666667s17.066667 42.666667 42.666667 42.666666h341.333333c25.6 0 42.666667-17.066667 42.666667-42.666666S793.6 512 768 512z m-256-85.333333h170.666667c25.6 0 42.666667-17.066667 42.666666-42.666667S708.266667 341.333333 682.666667 341.333333h-170.666667c-25.6 0-42.666667 17.066667-42.666667 42.666667s17.066667 42.666667 42.666667 42.666667z m341.333333 512h-682.666666c-25.6 0-42.666667-17.066667-42.666667-42.666667v-682.666667C128 187.733333 110.933333 170.666667 85.333333 170.666667s-42.666667 17.066667-42.666666 42.666666v682.666667c0 68.266667 59.733333 128 128 128h682.666666c25.6 0 42.666667-17.066667 42.666667-42.666667s-17.066667-42.666667-42.666667-42.666666z"
                        p-id="43793" fill="#3ddc91"></path>
                  </svg>
                  <span style="margin-left: 5px">{{ scope.row.title }}</span>
                </a>
              </template>
            </el-table-column>
            <el-table-column
                prop="status_id"
                label="执行状态"
                width="100">
              <template slot-scope="scope">

                <el-dropdown trigger="click" @command="handleCommandStatus">
                  <span class="el-dropdown-link" style="cursor: pointer">
                    <el-tag :type="getStatus(scope.row.run_status_id).type" size="small">{{
                        getStatus(scope.row.run_status_id).name
                      }}</el-tag>
                    <i class="el-icon-arrow-down el-icon--right"></i>
                  </span>
                  <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item v-for="item in getRunStatusList()" :key="item.id"
                                      :command="{'id': scope.row.id, 'run_status_id': item.id}">
                      <el-tag :type="item.type" size="small">{{ item.name }}</el-tag>
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </el-dropdown>

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

            <el-table-column fixed="right" label="操作" width="50">
              <template slot-scope="scope">
                <el-button @click="showDeleteDialog(scope.row)" type="danger" size="mini" circle
                           icon="el-icon-delete"></el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>

      </el-card>
    </div>


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
    <HTestPlanPlanningDialog
        v-if="showPlanningFlag"
        @cancel="showPlanningFlag=false"
        @success="closePlanningDialog"
        :test-hub-id="Number(testHubId)"
        :test-plan-id="testPlanId">
    </HTestPlanPlanningDialog>
  </div>
</template>

<script>
import TestHubApi from '../../../../request/testHub'
import HTestCaseMap from "../../../../utils/hTestCase"
import HTestShowCaseForm from "../HTestCase/HTestShowCaseForm";
import HTestPlanPlanningDialog from "./HTestPlanPlanningDialog";

export default {
  name: "TestPlanDetail",
  components: {
    HTestShowCaseForm,
    HTestPlanPlanningDialog
  },
  data() {
    return {
      testPlan: {},
      testCaseId: 0,
      testPlanId: 0,
      showCaseDrawerFlag: false,
      loading: false,
      testCaseList: [],

      testHubId: 0,
      testHub: {},
      total: 0,
      query: {
        page: 1,
        size: 5,
        total: 0,
        hTestPlanId: 0,
        hTestHubId: 0,
        hModuleId: "0"
      },
      recentTestHubList: [],
      activeIndex: "testplan",
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

      showPlanningFlag: false,
    }
  },
  created() {
  },
  mounted() {
    this.testHubId = Number(this.$route.params.testhubId);
    this.testPlanId = Number(this.$route.params.testPlanId);
    this.getTestHubModuleList()
    this.getTestHub()
    this.getTestPlan()
    this.getTestCase()

    this.moduleHeight = document.body.clientHeight - 140
    document.getElementById('case-menu-module').style.height = this.moduleHeight + 'px'
  },
  methods: {
    closePlanningDialog() {
      this.showPlanningFlag = false
      this.getTestCase()
    },
    async updateTestPlanCase(rid, data) {
      let resp = await TestHubApi.updateTestPlanTestCase(rid, data)
      if (resp.success == true) {
        this.getTestCase()
        this.getTestPlan()
      } else {
        this.$message.error(resp.error.message);
      }
    },
    handleCommandStatus(command) {
      let params = {"run_status_id": command.run_status_id}
      this.updateTestPlanCase(command.id, params)
    },
    async handleCommandPlanStatus(command) {
      let params = {"status_id": command}
      let resp = await TestHubApi.updateTestPlan(this.testPlanId, params)
      if (resp.success == true) {
        this.getTestPlan()
      } else {
        this.$message.error(resp.error.message);
      }
    },
    back() {
      this.$router.back()
    },
    async getTestPlan() {
      let resp = await TestHubApi.getTestPlan(this.testPlanId)
      if (resp.success == true) {
        this.testPlan = resp.data
      } else {
        this.$message.error(resp.error.message);
      }
    },
    showDeleteDialog(data) {
      this.$confirm('此操作将永久移除该数据, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 这个ip是关联表的id
        TestHubApi.deleteTestPlanTestCase(data.id).then(resp => {
          if (resp.success == true) {
            this.$message.success("删除成功！")
            this.getTestCase()
          } else {
            this.$message.error("删除失败！");
          }
        })
      }).catch(() => {
      });
    },
    showTestCase(testCaseId) {
      this.showCaseDrawerFlag = true
      this.testCaseId = testCaseId
    },
    getAllTestCase() {
      this.query.hModuleId = "0"
      this.getTestCase()
    },
    openAddCaseDialog() {
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
    getStatus(statusID) {
      return HTestCaseMap.getTestPlanRunStatus(statusID)
    },
    getRunStatusList() {
      return HTestCaseMap.getTestPlanRunStatusList()
    },

    getPlanStatus(statusID) {
      return HTestCaseMap.getTestPlanStatus(statusID)
    },
    getPlanStatusList() {
      return HTestCaseMap.getTestPlanStatusList()
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
      this.query.hModuleId = data.id
      this.getTestCase()
    },
    handleSelect(key) {
      this.$router.push('/main/testHub/' + this.testHubId + "/" + key)
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
      this.query.hTestPlanId = this.testPlanId
      this.query.hTestHubId = this.testHubId

      const resp = await TestHubApi.getTestPlanTestCaseList(this.query)
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
.class-a {
  line-height: 15px;
  font-weight: normal !important;
  margin-left: 5px;
  color: #409EFF !important;
}

.status-bar {
  text-align: left;
  margin: 10px 0;
  display: flex;
  justify-content: space-between;
  font-size: 14px
}

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

.common-flex {
  display: flex;
  align-items: center;
  padding: 3px;
}

.common-width {
  width: 150px;
}
</style>