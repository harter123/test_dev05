<template>
  <div class="task-dialog">
    <el-dialog :title=showTitle :visible.sync="showStatus" @close="cancelTestHub()">
      <el-form :rules="rules" ref="elForm" :model="form" label-width="80px">
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
            <el-button type="primary" @click="onSubmit()">保存</el-button>
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
    this.init()
  },
  mounted() {
    console.log("自动被执行mounted")
  },
  methods: {
    async init(){
      if (this.testHubId === 0) {
        this.showTitle = "创建测试库"
        this.form.id = 0
        this.form.name = ""
        this.form.describe = ""
        this.form.flag = ""
      } else {
        this.showTitle = "编辑测试库"
        const resp = await TestHubApi.getTestHub(this.testHubId);
        if (resp.success == true) {
          this.form.id = resp.data.id
          this.form.name = resp.data.name
          this.form.describe = resp.data.describe
          this.form.flag = resp.data.flag
        } else {
          this.$message.error("获取数据失败！");
        }

      }
    },

    // 关闭dialog
    cancelTestHub() {
      this.$emit('cancel', {})
    },

    // 创建任务按钮
    onSubmit() {
      this.$refs.elForm.validate((valid) => {
        if (valid) {
          if(this.testHubId === 0) {
            TestHubApi.createTestHub(this.form).then(resp => {
              if (resp.success == true) {
                this.$message.success("创建成功！")
                this.$emit('success', {})
              } else {
                this.$message.error("创建失败！");
              }
            })
          } else {
            TestHubApi.updateTestHub(this.testHubId, this.form).then(resp => {
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