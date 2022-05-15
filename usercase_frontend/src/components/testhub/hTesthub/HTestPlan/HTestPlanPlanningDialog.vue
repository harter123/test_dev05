<template>
  <div class="test-plan-planning-dialog">
    <el-dialog title="规划用例" style="margin-top: -8vh" :visible.sync="showStatus" @close="cancelTestPlan()" width="600px">
      <div style="display: flex;justify-content: space-between; padding-top: 10px">
        <el-card class="box-card" style="width: 24%;overflow: auto" id="planning-case-menu-module" ref="caseMenuModule">
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
                @selection-change="handleSelectionChange"
                style="width: 100%;margin-top: -10px">
              <el-table-column
                  type="selection"
                  width="40">
              </el-table-column>
              <el-table-column
                  prop="title"
                  min-width="200"
                  label="标题">
                <template slot-scope="scope">
                  <a href="javascript:void(0)"
                     style="color: #409EFF; font-weight: normal; display: flex; align-items: center"
                     @click="showTestCase(scope.row.id)">
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
          <div class="foot-page" style="text-align: right">
            <el-pagination
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
                :page-sizes="[10, 20, 50, 100]"
                :page-size=query.size
                layout="total, sizes, prev, pager, next"
                :total=query.total>
            </el-pagination>
          </div>
        </el-card>
      </div>
      <div class="dialog-footer">
        <el-button @click="cancelTestPlan" size="small">取 消</el-button>
        <el-button type="primary" @click="onSubmit" size="small">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import TestHubApi from "../../../../request/testHub";
import HTestCaseMap from "../../../../utils/hTestCase";

export default {
  props: ['testPlanId', 'testHubId'],
  data() {
    return {
      testHub: {},
      moduleTree: [],
      defaultProps: {
        children: 'children',
        label: 'name'
      },
      showStatus: true,
      total: 0,
      query: {
        page: 1,
        size: 5,
        total: 0,
        hTestHubId: 0,
        HModuleIds: "all"
      },
      testCaseList: [],
      multipleSelection: [],
      moduleHeight: 0,
    }
  },
  created() {
    this.getTestHubModuleList()
    this.getTestHub();
    this.getTestCase()
  },
  mounted() {
  },
  methods: {
    handleSelectionChange(val) {
      this.multipleSelection = val;
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
    getAllTestCase() {
      this.query.HModuleIds = "all"
      this.getTestCase()
    },
    handleNodeClick(data) {
      this.query.HModuleIds = data.id
      this.getTestCase()
    },
    //初始化测试库列表列表
    async getTestHubModuleList() {
      const resp = await TestHubApi.getTestCaseModuleList({testHubId: this.testHubId})
      if (resp.success == true) {
        this.moduleTree = resp.data
      } else {
        this.$message.error(resp.error.message);
      }
    },
    async getTestHub() {
      let resp = await TestHubApi.getTestHub(this.testHubId)
      if (resp.success == true) {
        this.testHub = resp.data
      } else {
        this.$message.error(resp.error.message);
      }
    },
    // 关闭dialog
    cancelTestPlan() {
      this.$emit('cancel', {})
    },

    // 创建任务按钮
    onSubmit() {
      let data = {test_plan_id: this.testPlanId, test_case_ids: []}
      for (let i = 0; i < this.multipleSelection.length; i++) {
        data.test_case_ids.push(this.multipleSelection[i].id)
      }
      TestHubApi.createTestPlanTestCase(data).then(resp => {
        if (resp.success == true) {
          this.$message.success("创建成功！")
          this.$emit('success', {})
        } else {
          this.$message.error("创建失败！");
        }
      })
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
      this.query.size = val
      this.getTestCase()
    },

    // 点给第几页
    handleCurrentChange(val) {
      this.query.page = val
      this.getTestCase()
    }

  }

}
</script>

<style>
.test-plan-planning-dialog .el-dialog__body {
  padding: 0 20px 40px 20px;
}
</style>
<style scoped>
.test-plan-planning-dialog {
  text-align: left;
}

.dialog-footer {
  float: right;
}

.div-tree {
  max-height: 180px;
  overflow: auto;
}

.test-plan-dialog {
  text-align: left;
}
</style>