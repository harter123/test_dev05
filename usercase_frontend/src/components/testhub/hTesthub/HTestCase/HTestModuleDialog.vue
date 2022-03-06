<template>
  <div class="task-dialog">
    <el-dialog :title=showTitle :visible.sync="showStatus" @close="cancelTestModule()">
      <el-form :rules="rules" ref="elForm" :model="form" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item>
          <div class="dialog-footer">
            <el-button @click="cancelTestModule()">取消</el-button>
            <el-button type="primary" @click="onSubmit()">保存</el-button>
          </div>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import TestHubApi from '../../../../request/testHub'

export default {
  // props: ['testModuleId', "parentId"],
  props: {
    testModuleId:{
      type: Number,
      default: 0,
      required: true,
    },
    parentId: {
      type: Number,
      default: 0,
      required: true,
    },
    testHubId: {
      type: Number,
      default: 0,
      required: true,
    },
  },
  data() {
    return {
      showStatus: true,
      showTitle: '',
      form: {
        id: 0,
        name: '',
        parent_id: 0,
        h_test_hub_id: 0,
      },
      rules: {
        name: [
          {required: true, message: '请输入模块名称', trigger: 'blur'}
        ],
      },
      inResize: true,
    }
  },
  created() {
    this.init()
  },
  mounted() {
    console.log("自动被执行mounted")
  },
  methods: {
    async init(){
      this.form.h_test_hub_id = this.testHubId
      if (this.testModuleId === 0) {
        this.showTitle = "创建模块"
        this.form.id = 0
        this.form.name = ""
        this.form.parent_id = this.parentId
      } else {
        this.showTitle = "编辑模块"
        const resp = await TestHubApi.getTestCaseModule(this.testModuleId);
        if (resp.success == true) {
          this.form.id = resp.data.id
          this.form.name = resp.data.name
          this.form.parent_id = resp.data.parent_id
        } else {
          this.$message.error("获取数据失败！");
        }

      }
    },

    // 关闭dialog
    cancelTestModule() {
      this.$emit('cancel', {})
    },

    // 创建任务按钮
    onSubmit() {
      this.$refs.elForm.validate((valid) => {
        if (valid) {
          if(this.testModuleId === 0) {
            TestHubApi.createTestCaseModule(this.form).then(resp => {
              if (resp.success == true) {
                this.$message.success("创建成功！")
                this.$emit('success', {})
              } else {
                this.$message.error("创建失败！");
              }
            })
          } else {
            TestHubApi.updateTestCaseModule(this.testModuleId, this.form).then(resp => {
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

</style>