const statusList = [
    {"id": 1, 'name': "未审核", "type": "warning"},
    {"id": 2, 'name': "已审核", "type": "success"}
]

const testPlanStatusList = [
    {"id": 1, 'name': "未开始", "type": "info"},
    {"id": 2, 'name': "阻塞", "type": "warning"},
    {"id": 3, 'name': "通过", "type": "success"},
    {"id": 4, 'name': "跳过", "type": "info"},
    {"id": 5, 'name': "失败", "type": "danger"}
]


const priorityList = [
    {"id": 1, 'name': "P1", "type": "success"},
    {"id": 2, 'name': "P2", "type": "info"},
    {"id": 3, 'name': "P3", "type": "warning"},
    {"id": 4, 'name': "P4", "type": "danger"}
]

const typeList = [
    {"id": 1, 'name': "功能测试"},
    {"id": 2, 'name': "接口测试"},
    {"id": 3, 'name': "性能测试"},
    {"id": 4, 'name': "安全性测试"},
    {"id": 5, 'name': "兼容性测试"},
    {"id": 6, 'name': "其他"},
]

class HTestCaseMap {

    getItem(itemId, itemType) {
        let data = []
        switch (itemType) {
            case "status":
                data = statusList
                break;
            case "type":
                data = typeList
                break;
            case "priority":
                data = priorityList;
                break
            case "testPlanStatus":
                data = testPlanStatusList
                break
            default:
                return {"id": -1, "name": "未知"}
        }
        for (let i = 0; i < data.length; i++) {
            if (itemId == data[i]['id']) {
                console.log(data[i])
                return data[i]
            }
        }
        return {}
    }

    getTestPlanStatus(statusId) {
        return this.getItem(statusId, 'testPlanStatus')
    }

    getStatus(statusId) {
        return this.getItem(statusId, 'status')
    }

    getPriority(priorityId) {
        return this.getItem(priorityId, 'priority')
    }

    getType(typeId) {
        return this.getItem(typeId, 'type')
    }

    getTypeList() {
        return typeList
    }

    getStatusList() {
        return statusList
    }

    getPriorityList() {
        return priorityList
    }

    getTestPlanStatusList() {
        return testPlanStatusList
    }
}

export default new HTestCaseMap()