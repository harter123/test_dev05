const statusList = [
    {"id": 1, 'name': "未通过", "type": "warning"},
    {"id": 2, 'name': "通过", "type": "success"}
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
        switch (itemType){
            case "status":
                data = statusList
                break;
            case "type":
                data = typeList
                break;
            case "priority":
                data = priorityList;
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
}

export default new HTestCaseMap()