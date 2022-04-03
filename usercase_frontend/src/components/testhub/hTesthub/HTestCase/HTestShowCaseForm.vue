<template>
  <div class="h-case-form">
    <div class="h-case-form-title">
      <div class="h-case-form-title-1">
        测试用例 {{ testHub.flag }}-{{ form.id }}
      </div>
      <div class="h-case-form-title-2">
        |
      </div>
      <div class="h-case-form-title-3">
        {{ testHub.name }}
      </div>
    </div>
    <hr style="height:1px;border:none;border-top:1px solid #C0C4CC;"/>
    <div class="h-case-form-title">
      <el-input v-model="form.title"></el-input>
    </div>
    <div style="display: flex; justify-content: space-between; margin-top: 5px">
      <div class="h-case-form-rich-p">
        <el-dropdown trigger="click" @command="handleCommandStatus">
          <span class="el-dropdown-link" style="cursor: pointer">
            <span v-if="!form.status_id" class="h-case-form-title-3">
              状态
            </span>
            <el-tag v-else :type="getStatus(form.status_id).type" size="small">{{
                getStatus(form.status_id).name
              }}</el-tag>
            <i class="el-icon-arrow-down el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item v-for="item in caseStatus" :key="item.id" :command="item.id">
              <el-tag :type="item.type" size="small">{{ item.name }}</el-tag>
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>

      </div>
      <div class="h-case-form-rich-p">
        <el-dropdown trigger="click" @command="handleCommandPriority">
          <span class="el-dropdown-link" style="cursor: pointer">
            <span v-if="!form.priority_id" class="h-case-form-title-3">
              优先级
            </span>
            <el-tag v-else :type="getPriority(form.priority_id).type" size="small">{{
                getPriority(form.priority_id).name
              }}</el-tag>
            <i class="el-icon-arrow-down el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item v-for="item in casePriority" :key="item.id" :command="item.id">
              <el-tag :type="item.type" size="small">{{ item.name }}</el-tag>
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
      <div class="h-case-form-rich-p">
        <el-dropdown trigger="click" @command="handleCommandType">
          <span class="el-dropdown-link" style="cursor: pointer">

            <span v-if="!form.type_id" class="h-case-form-title-3">
              类型
            </span>
            <span v-else>
              {{ getType(form.type_id).name }}
            </span>
            <i class="el-icon-arrow-down el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item v-for="item in caseTypes" :key="item.id" :command="item.id">
              {{ item.name }}
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>

      <div class="h-case-form-module">
        <el-cascader
            placeholder="模块"
            :props="{'value': 'id', 'label': 'name'}"
            v-model="testModuleIdList"
            :options="moduleTree"
            @change="handleChangeModule"></el-cascader>
      </div>
    </div>

    <div class="h-case-form-text">
      <div class="h-case-form-text-p">前置</div>
      <el-input type="textarea" v-model="form.pre_step" @blur="handleChangePre"></el-input>
    </div>
    <div class="h-case-form-text">
      <div class="h-case-form-text-p">步骤</div>
      <el-input type="textarea" v-model="form.step" :rows="4" @blur="handleChangeStep"></el-input>
    </div>
    <div class="h-case-form-text">
      <div class="h-case-form-text-p">后置</div>
      <el-input type="textarea" v-model="form.post_step" @blur="handleChangePost"></el-input>
    </div>
    <div class="h-case-form-text">
      <div class="h-case-form-text-p">预期</div>
      <el-input type="textarea" v-model="form.expect" @blur="handleChangeExpect"></el-input>
    </div>
    <div style="color: #aaa;font-size: 11px; margin-top: 15px">
      {{ user.name }} 创建于 {{ form.create_time }}
    </div>
    <!--        -->
    <!--    <div style="display: flex; justify-content: space-between">-->
    <!--      -->
    <!--      -->
    <!--      -->
    <!--    </div>-->

  </div>
</template>

<script>
import TestHubApi from '../../../../request/testHub'
import HTestCaseMap from "../../../../utils/hTestCase"

export default {
  props: {
    testCaseId: {
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
      caseStatus: [],
      moduleTree: [],
      user: {},
      testHub: {},
    }
  },
  created() {
    this.init()
  },
  mounted() {
    const user = sessionStorage.getItem('user')
    this.user = JSON.parse(user);
  },
  methods: {
    // 定义递归函数
    getTreeDeepArr(moduleId, moduleTreeData) {
      let arr = []; // 在递归时操作的数组
      let returnArr = []; // 存放结果的数组
      let depth = 0; // 定义全局层级
      // 定义递归函数
      function childrenEach(childrenData, depthN) {
        for (let j = 0; j < childrenData.length; j++) {
          depth = depthN; // 将执行的层级赋值 到 全局层级
          arr[depthN] = childrenData[j].id;
          if (childrenData[j].id == moduleId) {
            returnArr = arr.slice(0, depthN + 1); //将目前匹配的数组，截断并保存到结果数组，
            break
          } else {
            if (childrenData[j].children) {
              depth++;
              childrenEach(childrenData[j].children, depth);
            }
          }
        }
        return returnArr;
      }
      return childrenEach(moduleTreeData, depth);
    },
    handleCommandStatus(statusId) {
      let params = {"status_id": statusId}
      this.updateTestCase(params)
    },
    handleCommandType(typeId) {
      let params = {"type_id": typeId}
      this.updateTestCase(params)
    },
    handleCommandPriority(priorityId) {
      let params = {"priority_id": priorityId}
      this.updateTestCase(params)
    },
    handleChangeModule(value) {
      let moduleId = value[value.length - 1]
      let params = {"h_test_module_id": moduleId}
      this.updateTestCase(params)
    },
    handleChangePre() {
      let params = {"pre_step": this.form.pre_step}
      this.updateTestCase(params)
    },
    handleChangeStep() {
      let params = {"step": this.form.step}
      this.updateTestCase(params)
    },
    handleChangePost() {
      let params = {"post_step": this.form.post_step}
      this.updateTestCase(params)
    },
    handleChangeExpect() {
      let params = {"expect": this.form.expect}
      this.updateTestCase(params)
    },
    async updateTestCase(params) {
      const resp = await TestHubApi.updateTestCase(this.testCaseId, params)
      if (resp.success == true) {
        this.form = resp.data
      } else {
        this.$message.error(resp.error.message);
      }
    },

    async getTestHubModuleList() {
      const resp = await TestHubApi.getTestCaseModuleList({testHubId: this.$route.params.testhubId})
      if (resp.success == true) {
        this.moduleTree = resp.data
      } else {
        this.$message.error(resp.error.message);
      }
    },
    //初始化测试库列表列表
    async getTestCase() {
      const resp = await TestHubApi.getTestCase(this.testCaseId)
      if (resp.success == true) {
        this.form = resp.data
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
      this.casePriority = HTestCaseMap.getPriorityList()
      this.caseTypes = HTestCaseMap.getTypeList()
      this.caseStatus = HTestCaseMap.getStatusList()
      await this.getTestHub()
      await this.getTestCase()
      await this.getTestHubModuleList()

      this.testModuleIdList = this.getTreeDeepArr(this.form.h_test_module_id, this.moduleTree)
    },

    getStatus(statusID) {
      return HTestCaseMap.getStatus(statusID)
    },
    getPriority(priorityId) {
      return HTestCaseMap.getPriority(priorityId)
    },
    getType(typeId) {
      return HTestCaseMap.getType(typeId)
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
          if (this.testModuleIdList.length > 0) {
            this.form.h_test_module_id = this.testModuleIdList[this.testModuleIdList.length - 1] //取最后一项
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
.h-case-form-title .el-input__inner {
  padding: 0 5px;
  font-size: 18px;
  border: 1px solid white !important;
}

.h-case-form-title .el-input__inner:hover {
  border: 1px solid #DCDFE6 !important;
}

.h-case-form-module .el-input__inner {
  padding: 0 5px;
  width: 120px;
  border: 1px solid white !important;
  height: 30px;
}

.h-case-form-module .el-input__inner:hover {
  border: 1px solid #DCDFE6 !important;
}

.h-case-form-module .el-cascader {
  line-height: 30px;
}

.h-case-form-module .el-input__icon {
  line-height: 30px;
}

.h-case-form-text .el-textarea__inner {
  padding: 5px;
}

</style>
<style scoped>
.h-case-form {
  text-align: left;
  padding: 10px 15px;
}

.h-case-form-title {
  display: flex;
}

.h-case-form-title-1 {
  padding: 5px 10px;
  border-radius: 2px;
  color: rgb(51, 51, 51);
  background-color: rgba(61, 220, 145, 0.1);
}

.h-case-form-title-2 {
  color: #aaa;
  padding: 7px 15px;
}

.h-case-form-title-3 {
  color: #c0c4cc;
  padding: 7px 0px;
}

.h-case-form-rich-p {
  display: flex;
  flex-direction: column;
  justify-content: center
}

.h-case-form-text {
  padding-top: 8px;
}

.h-case-form-text-p {
  color: #888;
  font-size: 13px;
  margin-bottom: 5px;
}
</style>