<template>
  <div class="task-dialog">
    <el-dialog :title=showTitle :visible.sync="showStatus" @close="cancelTestHub()">
      <el-form :rules="rules" ref="form" :model="form" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="标识">
          <el-input v-model="form.flag"></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input type="textarea" v-model="form.describe"></el-input>
        </el-form-item>
        <el-form-item>
          <div class="dialog-footer">
            <el-button @click="cancelTestHub()">取消</el-button>
            <el-button type="primary" @click="onSubmit('form')">保存</el-button>
          </div>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import TestHubApi from '../../../request/testHub'

export default {
  props: ['testHubId'],
  data() {
    return {
      showStatus: true,
      showTitle: '',
      form: {
        id: 0,
        name: '',
        describe: '',
        flag: ""
      },
      rules: {
        name: [
          {required: true, message: '请输入测试库名称', trigger: 'blur'}
        ],
        flag: [
          {required: true, message: '请输入测试库标识', trigger: 'blur'}
        ]
      },
      inResize: true,
      data: [],
    }
  },
  created() {
    if (this.testHubId === 0) {
      this.showTitle = "创建测试库"
    } else {
      this.showTitle = "编辑测试库"
    }
  },
  mounted() {
    console.log("自动被执行mounted")
  },
  methods: {


    // 关闭dialog
    cancelTask() {
      this.$emit('cancel', {})
    },

    // 创建任务按钮
    onSubmit(formName) {
      // this.$refs[formName].validate((valid) => {
      //   if (valid) {
      //     if(this.tid === 0) {
      //       TaskApi.createTask(this.form).then(resp => {
      //         if (resp.success == true) {
      //           this.$message.success("创建成功！")
      //           this.cancelTask()
      //         } else {
      //           this.$message.error("创建失败！");
      //         }
      //       })
      //     } else {
      //       this.form.id = this.tid
      //       TaskApi.updateTask(this.form).then(resp => {
      //         if (resp.success == true) {
      //           this.$message.success("更新成功！")
      //           this.cancelTask()
      //         } else {
      //           this.$message.error("更新失败！");
      //         }
      //       })
      //     }
      //
      //   } else {
      //     return false;
      //   }
      // });

    },

  }

}
</script>

<style>
.el-tree {
  background: #f1f3fa !important;
}
</style>
<style scoped>
.dialog-footer {
  float: right;
}

.div-tree {
  max-height: 180px;
  overflow: auto;
}
</style>