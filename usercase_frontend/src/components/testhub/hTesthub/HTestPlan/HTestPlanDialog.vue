<template>
  <div class="test-plan-dialog">
    <el-dialog :title=showTitle :visible.sync="showStatus" @close="cancelTestPlan()" width="450px">
      <el-form :rules="rules" ref="elForm" :model="form" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" style="width: 300px"></el-input>
        </el-form-item>

        <el-form-item label="负责人" prop="owner_id">
          <el-select v-model="form.owner_id" placeholder="请选择" style="width: 300px">
            <el-option
                v-for="item in users"
                :key="item.id"
                :label="item.name"
                :value="item.id">
            </el-option>
          </el-select>

        </el-form-item>

        <el-form-item label="开始时间" prop="start_date">
          <el-date-picker
              style="width: 300px"
              format="yyyy-MM-dd"
              value-format="yyyy-MM-dd"
              v-model="form.start_date"
              align="right"
              type="date"
              placeholder="开始时间">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="结束时间" prop="end_date">
          <el-date-picker
              style="width: 300px"
              v-model="form.end_date"
              format="yyyy-MM-dd"
              value-format="yyyy-MM-dd"
              align="right"
              type="date"
              placeholder="结束时间">
          </el-date-picker>
        </el-form-item>

        <el-form-item label="测试库">
          {{testHub.name}}
        </el-form-item>

        <el-form-item>
          <div class="dialog-footer">
            <el-button @click="cancelTestPlan()">取消</el-button>
            <el-button type="primary" @click="onSubmit()">保存</el-button>
          </div>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import TestHubApi from "../../../../request/testHub";

export default {
  props: ['testPlanId', 'testHubId'],
  data() {
    return {
      testHub:{},
      users: [],
      showStatus: true,
      showTitle: '',
      form: {
        id: 0,
        name: '',
        h_test_hub_id: 0,
        owner_id: 0,
        start_date: undefined,
        end_date: undefined,
      },
      rules: {
        name: [
          {required: true, message: '请输入名称', trigger: 'blur'}
        ],
        h_test_hub_id: [
          {required: true, message: '请输入测试库', trigger: 'blur'}
        ],
        owner_id: [
          {required: true, message: '请输入负责人', trigger: 'blur'}
        ],
        start_date: [
          {required: true, message: '请输入开始时间', trigger: 'blur'}
        ],
        end_date: [
          {required: true, message: '请输入结束时间', trigger: 'blur'}
        ],
      },
      inResize: true,
      data: [],
    }
  },
  created() {
    this.init()
    this.getTestHub();
    this.getUsers();
  },
  mounted() {
  },
  methods: {
    async getUsers() {
      let resp = await TestHubApi.getUsers()
      if (resp.success == true) {
        this.users = resp.data
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
    async init() {
      if (this.testPlanId === 0) {
        this.showTitle = "创建测试计划"
        this.form.id = 0
        this.form.name = ""
        this.form.start_date = undefined
        this.form.end_date = undefined
        this.form.owner_id = undefined
        this.form.h_test_hub_id = this.testHubId
      } else {
        this.showTitle = "编辑测试计划"
        const resp = await TestHubApi.getTestPlan(this.testPlanId);
        if (resp.success == true) {
          this.form.id = resp.data.id
          this.form.name = resp.data.name
          this.form.start_date = resp.data.start_date
          this.form.end_date = resp.data.end_date
          this.form.owner_id = resp.data.owner_id
          this.form.h_test_hub_id = resp.data.h_test_hub_id
        } else {
          this.$message.error("获取数据失败！");
        }

      }
    },

    // 关闭dialog
    cancelTestPlan() {
      this.$emit('cancel', {})
    },

    // 创建任务按钮
    onSubmit() {
      this.$refs.elForm.validate((valid) => {
        if (valid) {
          if (this.testPlanId === 0) {
            TestHubApi.createTestPlan(this.form).then(resp => {
              if (resp.success == true) {
                this.$message.success("创建成功！")
                this.$emit('success', {})
              } else {
                this.$message.error("创建失败！");
              }
            })
          } else {
            TestHubApi.updateTestPlan(this.testPlanId, this.form).then(resp => {
              if (resp.success == true) {
                this.$message.success("更新成功！")
                this.$emit('success', {})
              } else {
                this.$message.error("更新失败！");
              }
            })
          }

        } else {
          return false;
        }
      });

    },

  }

}
</script>

<style>

</style>
<style scoped>
.dialog-footer {
  float: right;
}

.div-tree {
  max-height: 180px;
  overflow: auto;
}
.test-plan-dialog{
  text-align: left;
}
</style>