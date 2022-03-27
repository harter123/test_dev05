<template>
  <div class="h-case-dialog">
    <el-dialog :title=showTitle :visible.sync="showStatus" @close="cancelTestModule()" width="80%"
               style="margin-top: -9vh;">
      <el-form :rules="rules" ref="elForm" :model="form" label-width="80px" label-position="top">
        <hr style="height:1px;border:none;border-top:1px solid #C0C4CC;"/>
        <div style="display: flex; justify-content: space-between">

          <div id="h-case-left"
               :style="{'height': height, 'width': '65%', 'overflow-y': 'scroll', 'padding-right': '5px'}">
            <el-form-item label="标题" prop="title">
              <el-input v-model="form.title"></el-input>
            </el-form-item>

            <el-form-item label="前置">
              <el-input type="textarea" v-model="form.pre_step"></el-input>
            </el-form-item>
            <el-form-item label="步骤">
              <el-input type="textarea" v-model="form.step" :rows="4"></el-input>
            </el-form-item>
            <el-form-item label="后置">
              <el-input type="textarea" v-model="form.post_step"></el-input>
            </el-form-item>
            <el-form-item label="预期">
              <el-input type="textarea" v-model="form.expect"></el-input>
            </el-form-item>
          </div>

          <div style="width: 33%;text-align: left">

            <el-form-item label="用例模块" prop="h_test_module_id">
              <el-cascader
                  :props="{'value': 'id', 'label': 'name'}"
                  v-model="testModuleIdList"
                  :options="moduleTree"
                  @change="handleChange"></el-cascader>
            </el-form-item>
            <el-form-item label="用例类型" prop="type_id">
              <el-select v-model="form.type_id" placeholder="请选择">
                <el-option
                    v-for="item in caseTypes"
                    :key="item.id"
                    :label="item.name"
                    :value="item.id">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="优先级" prop="priority_id">
              <el-select v-model="form.priority_id" placeholder="请选择">
                <el-option
                    v-for="item in casePriority"
                    :key="item.id"
                    :label="item.name"
                    :value="item.id">
                  <el-tag :type="item.type" size="small">
                    {{ item.name }}
                  </el-tag>
                </el-option>
              </el-select>
            </el-form-item>
            <div style="padding: 10px 0 15px 0">
              测试库: &nbsp; &nbsp;{{ testHub.name }}
            </div>
            <div style="padding: 0 0 5px 0">
              创建人: &nbsp; &nbsp;{{ user.name }}
            </div>
          </div>

        </div>

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
import HTestCaseMap from "../../../../utils/hTestCase"

export default {
  props: {
    testHubId: {
      type: Number,
      default: 0,
      required: true,
    },
  },
  data() {
    return {
      showStatus: true,
      showTitle: '创建用例',

      testModuleIdList: [],
      form: {
        id: 0,
        title: '',
        pre_step: '',
        step: '',
        post_step: '',
        expect: '',
        type_id: undefined,
        priority_id: 1,
        h_test_module_id: undefined,
        h_test_hub_id: 0,
        status_id: 1,
      },
      rules: {
        title: [
          {required: true, message: '请输入用例标题', trigger: 'blur'}
        ],
      },
      inResize: true,
      height: '200px',
      caseTypes: [],
      casePriority: [],
      moduleTree: [],
      user: {},
      testHub: {},
    }
  },
  created() {
    this.init()
  },
  mounted() {
    this.height = document.body.clientHeight - 220 + 'px'
    const user = sessionStorage.getItem('user')
    this.user = JSON.parse(user);

  },
  methods: {
    //初始化测试库列表列表
    async getTestHubModuleList() {
      const resp = await TestHubApi.getTestCaseModuleList({testHubId: this.$route.params.testhubId})
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
    handleChange() {

    },
    async init() {

      this.casePriority = HTestCaseMap.getPriorityList()
      this.caseTypes = HTestCaseMap.getTypeList()
      this.getTestHub()
      this.getTestHubModuleList()
    },

    // 关闭dialog
    cancelTestModule() {
      this.$emit('cancel', {})
    },

    // 创建任务按钮
    onSubmit() {
      this.$refs.elForm.validate((valid) => {
        if (valid) {
          console.log(this.testModuleIdList)
          if(this.testModuleIdList.length > 0){
            this.form.h_test_module_id = this.testModuleIdList[this.testModuleIdList.length -1 ] //取最后一项
          }
          this.form.h_test_hub_id = this.testHubId

          TestHubApi.createTestCase(this.form).then(resp => {
            if (resp.success == true) {
              this.$message.success("创建成功！")
              this.$emit('success', {})
            } else {
              this.$message.error("创建失败！");
            }
          })

        } else {
          return false;
        }
      });

    },

  }

}
</script>

<style>
.h-case-dialog .el-dialog__body {
  padding: 0px 15px 1px 15px;
}

.h-case-dialog .el-form-item {
  text-align: left;
}

.h-case-dialog .el-form--label-top .el-form-item__label {
  padding: 0;
}

.h-case-dialog .el-form-item {
  margin-bottom: 10px;
}

</style>
<style scoped>
.dialog-footer {
  float: right;
}

</style>