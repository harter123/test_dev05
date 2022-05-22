<template>
  <div id="report-dialog-main">
    <el-dialog
        :visible.sync="dialogVisible"
        width="30%"
        :fullscreen="true"
        @close="cancelTestPlan()">
      <div slot="title" class="report-title">
        <i class="el-icon-pie-chart" style="color: #348fe4; margin-right: 5px;font-size: 20px"></i>
        <span>测试报告</span>
        <div style="color: #aaa">
          <span style="padding: 0 15px">|</span>
          <span>{{ testPlan.name }}</span>
        </div>

      </div>
      <div style="display: flex; justify-content: center">
        <el-card shadow="never" class="report-content">
          <div style="margin-bottom: 10px">报告概览</div>
          <div class="report-summary-rate">
            <div class="report-summary-rate-item" style="background-color: #fffcf7">
              <div class="report-summary-rate-item-context">{{ totalNum }}</div>
              用例数
            </div>
            <div class="report-summary-rate-item" style="background-color: #f7fdff">
              <div class="report-summary-rate-item-context">{{ testPlan.owner_name }}</div>
              负责人
            </div>
            <div class="report-summary-rate-item" style="background-color: #f8fdfa">
              <div class="report-summary-rate-item-context">{{ testPlan.successRate }} %</div>
              通过率
            </div>
            <div class="report-summary-rate-item" style="background-color: #fff8f8">
              <div class="report-summary-rate-item-context">{{ testPlan.runRate }} %</div>
              覆盖率
            </div>

          </div>

          <div>
            <div style="display: flex;padding: 15px 50px">
              <div style="width: 400px; display: flex">
                <div class="report-tip-text">测试库:</div>
                {{ testHub.name }}
              </div>
              <div style="width: 400px; display: flex">
                <div class="report-tip-text">测试计划:</div>
                {{ testPlan.name }}
              </div>
            </div>
            <div style="display: flex;padding-left: 50px">
              <div style="width: 400px; display: flex">
                <div class="report-tip-text">状态:</div>
                <el-tag :type="getPlanStatus(testPlan.status_id).type" size="small">
                  {{ getPlanStatus(testPlan.status_id).name }}
                </el-tag>
              </div>
              <div style="width: 400px; display: flex">
                <div class="report-tip-text">时间:</div>
                {{ testPlan.start_date }} 到 {{ testPlan.end_date }}
              </div>
            </div>
          </div>
        </el-card>

      </div>
      <div style="display: flex; justify-content: center;margin-top: 20px">
        <el-card shadow="never" class="report-content">
          <div style="margin-bottom: 10px">执行结果分布</div>
          <div style="display: flex; justify-content: space-between">
            <div>
              <div id="report-echarts" style="width:450px ;height:300px;"></div>
            </div>
            <div>
              <div style="width: 481px">
                <el-table
                    :data="tableData"
                    header-cell-class-name="table-header-style"
                    border>
                  <el-table-column
                      prop="type"
                      label="结果"
                      width="160">
                    <template slot-scope="scope">
                      <el-tag :type="scope.row.type">{{ scope.row.name }}</el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column
                      prop="num"
                      label="用例数"
                      width="160">
                  </el-table-column>
                  <el-table-column
                      prop="rate"
                      label="占比"
                      width="160">
                  </el-table-column>
                </el-table>
              </div>
            </div>
          </div>

        </el-card>
      </div>

    </el-dialog>
  </div>

</template>

<script>
import TestHubApi from '../../../../request/testHub'
import HTestCaseMap from "../../../../utils/hTestCase";
import * as echarts from "echarts"

export default {
  name: "HTestReportDialog",
  props: {
    testPlanId: {
      type: Number,
      required: true,
      default: 0
    },
    testHubId: {
      type: Number,
      required: true,
      default: 0
    }
  },
  data() {
    return {
      dialogVisible: true,
      testPlan: {},
      testHub: {},
      totalNum: 0,
      tableData: [],
    }
  },
  created() {
    this.getTestPlan()
    this.getTestHub()
  },
  methods: {
    getPie() {
      // 绘制图表
      var myChart = echarts.init(document.getElementById('report-echarts'))
      // 指定图表的配置项和数据
      let data = []
      for (let i = 0; i < this.tableData.length; i++) {
        data.push({
          name: this.tableData[i].name, value: this.tableData[i].num
        })
      }
      let option = {
        //鼠标划过时饼状图上显示的数据
        tooltip: {
          trigger: 'item',
          formatter: '{b}:{c} ({d}%)'
        },
        color: ['#67c23a', '#e6a23c', '#f56c6c', '#909399', '#409EFF'],
        // 饼图数据
        series: {
          // name: 'bug分布',
          type: 'pie',             //echarts图的类型   pie代表饼图
          // data:''               //饼图数据
          data: data
        }
      }
      // 使用刚指定的配置项和数据显示图表。
      myChart.setOption(option)
    },

    getPlanStatus(statusID) {
      return HTestCaseMap.getTestPlanStatus(statusID)
    },
    async getTestHub() {
      let resp = await TestHubApi.getTestHub(this.testHubId)
      if (resp.success == true) {
        this.testHub = resp.data
      } else {
        this.$message.error(resp.error.message);
      }
    },
    makeTableData() {
      let ret = this.testPlan
      let totalNum = ret['success_num'] + ret['failed_num'] + ret['skip_num'] + ret['block_num'] + ret["not_start_num"]
      let success = {
        type: "success",
        name: "成功",
        num: this.testPlan.success_num,
        rate: (this.testPlan.success_num * 100 / totalNum).toFixed(2) + "%"
      }
      this.tableData.push(success)

      let block = {
        type: "warning",
        name: "阻塞",
        num: this.testPlan.block_num,
        rate: (this.testPlan.block_num * 100 / totalNum).toFixed(2) + "%"
      }
      this.tableData.push(block)

      let failed = {
        type: "danger",
        name: "失败",
        num: this.testPlan.failed_num,
        rate: (this.testPlan.failed_num * 100 / totalNum).toFixed(2) + "%"
      }
      this.tableData.push(failed)

      let notStart = {
        type: "info",
        name: "未开始",
        num: this.testPlan.not_start_num,
        rate: (this.testPlan.not_start_num * 100 / totalNum).toFixed(2) + "%"
      }
      this.tableData.push(notStart)

      let skip = {
        type: "",
        name: "跳过",
        num: this.testPlan.skip_num,
        rate: (this.testPlan.skip_num * 100 / totalNum).toFixed(2) + "%"
      }
      this.tableData.push(skip)
    },
    async getTestPlan() {
      let resp = await TestHubApi.getTestPlan(this.testPlanId)
      if (resp.success == true) {
        this.testPlan = resp.data
        let ret = resp.data
        this.totalNum = ret['success_num'] + ret['failed_num'] + ret['skip_num'] + ret['block_num'] + ret["not_start_num"]
        this.makeTableData();
        this.getPie();
      } else {
        this.$message.error(resp.error.message);
      }
    },
    // 关闭dialog
    cancelTestPlan() {
      this.$emit('cancel', {})
    },
  }
}
</script>

<style>
#report-dialog-main .el-dialog__body {
  padding: 5px 20px;
}

#report-dialog-main .el-table__header-wrapper .el-table__cell {
  background-color: #f3f3f3;
}
</style>

<style scoped>
#report-dialog-main {
  text-align: left;
}

.report-content {
  width: 950px;
}

.report-title {
  text-align: left;
  font-size: 18px;
  display: flex;
  align-items: center;
}

.report-summary-rate {
  display: flex;
  justify-content: space-between;
}

.report-summary-rate-item {
  padding: 20px 40px;
  width: 145px;
}

.report-summary-rate-item-context {
  font-size: 30px;
}

.report-tip-text {
  color: #888;
  width: 70px;
}

.table-header-style {
  background-color: #f3f3f3;
}
</style>