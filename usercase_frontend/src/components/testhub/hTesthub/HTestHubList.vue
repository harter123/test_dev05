<template>
  <div class="case">
    <!-- 面包屑 -->

    <div id="case-menu" style="display: flex;justify-content: space-between;border-bottom: solid 1px #e6e6e6;">
      <el-breadcrumb separator-class="el-icon-arrow-right" style="width: 30%">
        <el-breadcrumb-item :to="{ path: '/' }">
          首页
        </el-breadcrumb-item>
        <el-breadcrumb-item>
          测试库
        </el-breadcrumb-item>
      </el-breadcrumb>

      <div style="margin-top: -20px; width: 30%">
        <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
          <el-menu-item index="testhub">测试库</el-menu-item>
          <el-menu-item index="todo">待办</el-menu-item>
        </el-menu>
      </div>
      <div style="width: 30%"></div>
    </div>

    <div v-if="activeIndex=='testhub'">
      <el-card class="box-card" style="margin-bottom: 5px;margin-top:10px">
        <div class="testhub-recent-line">
          <div>
            最近访问
          </div>

          <div style="display: flex">
            <div class="testhub-recent-item" v-for="item in recentTestHubList" :key="item.id"
                 @click="gotoTestHub(item.h_test_hub_id)">
              <div style="padding: 15px 10px 10px 10px; display: flex; align-items: center">
                <img class="app-icon"
                     src="https://cdn.pingcode.com/static/portal/assets/app-icons/app-testhub-square-fill.svg?v=3.62.2">
                <span style="font-size: 18px;margin-left: 5px">{{ item.test_hub_name }}</span>
              </div>
              <div style="color: #aaa;font-size: .75rem;padding: 5px 10px 5px 10px">
                {{ item.test_hub_creator_name }} . {{ item.test_hub_create_time }}
              </div>
            </div>
          </div>

        </div>
      </el-card>
      <!-- 卡片 -->
      <el-card class="box-card">
        <div class="testhub-filter-line">
          <el-input
              :clearable="true"
              @change="getTestHubList()"
              style="width: 200px"
              placeholder="请输入搜索内容"
              prefix-icon="el-icon-search"
              v-model="query.keyword">
          </el-input>
          <div>
            <el-button type="primary" @click="showAddDialog()">创建</el-button>
          </div>

        </div>

        <div>
          <!-- 表格 -->
          <el-table :data="tableData" v-loading="loading" style="width: 100%">
            <el-table-column prop="name" label="名称" min-width="30%">
              <template slot-scope="scope">
                <div style="display: flex; align-items: center">
                  <img width="15px" height="15px" class="app-icon"
                       src="https://cdn.pingcode.com/static/portal/assets/app-icons/app-testhub-square-fill.svg?v=3.62.2">
                  <a style="line-height: 15px;font-weight: normal; margin-left: 5px" @click="gotoTestHub(scope.row.id)"
                     href="javascript:void(0)">{{ scope.row.name }}</a>
                </div>

              </template>
            </el-table-column>
            <el-table-column prop="flag" label="标识" min-width="10%">
            </el-table-column>
            <el-table-column prop="h_test_plan_num" label="测试计划" min-width="10%">
            </el-table-column>
            <el-table-column prop="creator_name" label="创建人" min-width="15%">
            </el-table-column>
            <el-table-column prop="create_time" label="创建时间" min-width="15%">
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
                :page-sizes="[5, 10, 20, 50]"
                :page-size=query.size
                background
                layout="total, sizes, prev, pager, next"
                :total=total>
            </el-pagination>
          </div>
        </div>
      </el-card>
    </div>

    <div v-else>
      <HTestTodoList></HTestTodoList>
    </div>

    <HTestHubDialog v-if="showTestHubDailogFlag"
                    :test-hub-id="testHubId"
                    @cancel="closeAddEDitDialog"
                    @success="closeAddEDitDialog">
    </HTestHubDialog>
  </div>
</template>

<script>
import TestHubApi from '../../../request/testHub'
import HTestHubDialog from "./HTestHubDialog.vue"
import HTestTodoList from "./HTestTodoList"

export default {
  name: "TestHubList",
  components: {
    HTestHubDialog,
    HTestTodoList
  },
  data() {
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
      activeIndex: "testhub"
    }
  },
  created() {
    console.log("父组件", this.showDailog)
  },
  mounted() {
    this.getTestHubList()
    this.getRecentTestHubList()
  },
  methods: {
    handleSelect(key) {
      this.activeIndex = key;
    },
    showAddDialog() {
      this.showTestHubDailogFlag = true
      this.testHubId = 0
    },
    showEditDialog(testHub) {
      this.testHubId = testHub.id
      this.showTestHubDailogFlag = true

    },
    closeAddEDitDialog() {
      this.showTestHubDailogFlag = false
      this.getTestHubList()
    },
    showDeleteDialog(testHub) {
      this.$confirm('此操作将永久删除该数据, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        TestHubApi.deleteTestHub(testHub.id).then(resp => {
          if (resp.success == true) {
            this.$message.success("删除成功！")
            this.getTestHubList()
          } else {
            this.$message.error("删除失败！");
          }
        })
      }).catch(() => {
      });
    },
    //初始化测试库列表列表
    async getTestHubList() {
      this.loading = true
      const resp = await TestHubApi.getTestHubList(this.query)
      if (resp.success == true) {
        this.tableData = resp.data.testHubList
        this.total = resp.data.total
      } else {
        this.$message.error(resp.error.message);
      }
      this.loading = false
    },
    //初始化最近测试库列表列表
    async getRecentTestHubList() {
      const resp = await TestHubApi.getRecentTestHubList()
      if (resp.success == true) {
        this.recentTestHubList = resp.data
      } else {
        this.$message.error(resp.error.message);
      }
    },
    gotoTestHub(testHubId) {
      this.$router.push('/main/testHub/' + testHubId + "/testcase")
      TestHubApi.createRecentTestHub({h_test_hub_id: testHubId})
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
      this.getTestHubList()
    },

    // 点给第几页
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`)
      this.query.page = val
      this.getTestHubList()
    }

  }

}
</script>

<style>
.testhub-filter-line .el-input__icon {
  height: 50% !important;
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