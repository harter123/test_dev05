<template>
  <div class="case-main">
    <div style="margin-top: 10px;">
      <el-card>
        <div class="testplan-filter-line">
          <div>测试计划</div>
          <div>
            <el-input
                :clearable="true"
                @change="getTestPlanList()"
                @keyup.enter.native="getTestPlanList"
                style="width: 200px;margin-right: 10px"
                placeholder="请输入搜索内容"
                prefix-icon="el-icon-search"
                v-model="query.keyword">
            </el-input>

            <el-dropdown trigger="click" @command="handleCommandStatus" style="width: 80px">
              <span class="el-dropdown-link" style="cursor: pointer">
                <span v-if="query.statusId == undefined" class="h-case-form-title-3">
                  状态
                </span>
                <el-tag v-else :type="getStatus(query.statusId).type" size="small">
                  {{ getStatus(query.statusId).name }}</el-tag>
                <i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item v-for="item in testPlanStatus" :key="item.id" :command="item.id">
                  <el-tag :type="item.type" size="small">{{ item.name }}</el-tag>
                </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>

        </div>

        <div id="test-plan-id">
          <!-- 表格 -->
          <el-table id="test-plan-table-id" :data="tableData" v-loading="loading" style="width: 100%;overflow-y: auto" >
            <el-table-column prop="name" label="名称" min-width="30%">
              <template slot-scope="scope">
                <div style="display: flex; align-items: center">
                  <img width="15px" height="15px" class="app-icon"
                       src="https://cdn.pingcode.com/static/portal/assets/app-icons/app-testhub-square-fill.svg?v=3.62.2">
                  <a style="line-height: 15px;font-weight: normal; margin-left: 5px" @click="gotoTestPlan(scope.row)"
                     href="javascript:void(0)">{{ scope.row.name }}</a>
                </div>

              </template>
            </el-table-column>
            <el-table-column prop="status_id" label="状态" min-width="10%">
              <template slot-scope="scope">
                <span v-if="!scope.row.status_id">
                </span>
                <el-tag v-else :type="getStatus(scope.row.status_id).type" size="small">
                  {{ getStatus(scope.row.status_id).name }}
                </el-tag>

              </template>
            </el-table-column>
            <el-table-column prop="h_test_plan_num" label="结果" min-width="10%">
            </el-table-column>
            <el-table-column prop="creator_name" label="创建人" min-width="10%">
            </el-table-column>
            <el-table-column prop="owner_name" label="负责人" min-width="10%">
            </el-table-column>
            <el-table-column prop="create_time" label="时间" min-width="20%">
              <template slot-scope="scope">
                {{ scope.row.start_date }} 到 {{ scope.row.end_date }}

              </template>
            </el-table-column>
            <el-table-column fixed="right" label="操作" width="100">
              <template slot-scope="scope">
                <el-button @click="showEditDialog(scope.row)" type="primary" size="mini" circle
                           icon="el-icon-edit"></el-button>
                <el-button @click="showDeleteDialog(scope.row)" type="danger" size="mini" circle
                           icon="el-icon-delete"></el-button>
              </template>
            </el-table-column>
          </el-table>
          <!-- 分页 -->
          <div class="foot-page">
            <el-pagination
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
                :page-sizes="[10, 20, 50, 10]"
                :page-size=query.size
                background
                layout="total, sizes, prev, pager, next"
                :total=total>
            </el-pagination>
          </div>
        </div>
      </el-card>

    </div>
    <testPlanDialog v-if="showTestPlanDailogFlag"
                    :test-hub-id="testHubId"
                    @cancel="showTestPlanDailogFlag=false"
                    @success="closeAddEDitDialog"
                    :test-plan-id="editTestPlanId">

    </testPlanDialog>
  </div>
</template>

<script>
import TestHubApi from "../../../request/testHub";
import HTestCaseMap from "../../../utils/hTestCase";
import testPlanDialog from "./HTestPlan/HTestPlanDialog.vue"

export default {
  name: "HTestTodoList",
  components: {
    testPlanDialog,
  },
  data() {
    return {
      clientHeight: 100,

      loading: false,
      tableData: [],
      showTestPlanDailogFlag: false,
      showDeleteDailogFlag: false,
      total: 0,
      query: {
        page: 1,
        size: 10,
        keyword: "",
        statusId: 2,
      },
      editTestPlanId: 0,
      testPlanStatus: [],
      testHubId: 0
    }
  },
  mounted() {
    this.getTestPlanList()

    this.testPlanStatus = HTestCaseMap.getTestPlanStatusList()
    this.clientHeight = document.body.clientHeight - 190
    document.getElementById('test-plan-table-id').style.height = this.clientHeight + 'px'
  },
  methods: {
    closeAddEDitDialog() {
      this.showTestPlanDailogFlag = false
      this.getTestPlanList()
    },
    showEditDialog(testPlan) {
      this.testHubId = testPlan.h_test_hub_id;
      this.editTestPlanId = testPlan.id
      this.showTestPlanDailogFlag = true
    },
    showDeleteDialog(testPlan) {
      this.$confirm('此操作将永久删除该数据, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        TestHubApi.deleteTestPlan(testPlan.id).then(resp => {
          if (resp.success == true) {
            this.$message.success("删除成功！")
            this.getTestPlanList()
          } else {
            this.$message.error("删除失败！");
          }
        })
      }).catch(() => {
      });
    },
    getStatus(statusID) {
      return HTestCaseMap.getTestPlanStatus(statusID)
    },
    handleCommandStatus(statusId) {
      this.query.statusId = statusId
      this.getTestPlanList()
    },
    handleSelect(key) {
      this.$router.push('/main/testHub/' + this.testHubId + "/" + key)
    },
    //初始化测试计划列表列表
    async getTestPlanList() {
      this.loading = true
      const resp = await TestHubApi.getToDoTestPlanList(this.query)
      if (resp.success == true) {
        this.tableData = resp.data.TestPlanList
        this.total = resp.data.total
      } else {
        this.$message.error(resp.error.message);
      }
      this.loading = false
    },
    gotoTestPlan(data) {
      this.$router.push('/main/testHub/' + data.h_test_hub_id + "/testplan/" + data.id)
    },

    // 修改每页显示个数
    handleSizeChange(val) {
      this.query.size = val
      this.getTestPlanList()
    },

    // 点给第几页
    handleCurrentChange(val) {
      this.query.page = val
      this.getTestPlanList()
    }
  }
}
</script>

<!--全局的，优先级非常高-->
<style>
#case-menu .el-menu.el-menu--horizontal {
  border-bottom: none !important;
}
</style>

<!--局部的，优先级很低-->
<style scoped>
.testplan-filter-line {
  display: flex;
  justify-content: space-between;

}

.foot-page {
  text-align: right;
}
</style>