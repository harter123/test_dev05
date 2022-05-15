import request from '@/HttpCommon.js'


class TestHubApi {
    getTestHubList(data) {
        return request.get('/v1/testhub/', data)
    }

    getTestHub(tid) {
        return request.get('/v1/testhub/' + tid + '/')
    }

    deleteTestHub(tid) {
        return request.delete('/v1/testhub/' + tid + '/')
    }

    createTestHub(data) {
        return request.post('/v1/testhub/', data)
    }

    updateTestHub(tid, data) {
        return request.put('/v1/testhub/' + tid + '/', data)
    }

    getRecentTestHubList() {
        return request.get('/v1/recent/testhub/')
    }

    createRecentTestHub(data) {
        return request.post('/v1/recent/testhub/', data)
    }

    getTestCaseModuleList(data) {
        return request.get('/v1/testmodule/', data)
    }

    getTestCaseModule(tid) {
        return request.get('/v1/testmodule/' + tid + '/')
    }

    deleteTestCaseModule(tid) {
        return request.delete('/v1/testmodule/' + tid + '/')
    }

    createTestCaseModule(data) {
        return request.post('/v1/testmodule/', data)
    }

    updateTestCaseModule(tid, data) {
        return request.put('/v1/testmodule/' + tid + '/', data)
    }

    getTestCaseList(data) {
        return request.get('/v1/testcase/', data)
    }

    getTestCase(tid) {
        return request.get('/v1/testcase/' + tid + '/')
    }

    deleteTestCase(tid) {
        return request.delete('/v1/testcase/' + tid + '/')
    }

    createTestCase(data) {
        return request.post('/v1/testcase/', data)
    }

    updateTestCase(tid, data) {
        return request.put('/v1/testcase/' + tid + '/', data)
    }

    getTestPlanList(data) {
        return request.get('/v1/testplan/', data)
    }

    getTestPlan(pid) {
        return request.get('/v1/testplan/' + pid + '/')
    }

    deleteTestPlan(pid) {
        return request.delete('/v1/testplan/' + pid + '/')
    }

    createTestPlan(data) {
        return request.post('/v1/testplan/', data)
    }

    updateTestPlan(pid, data) {
        return request.put('/v1/testplan/' + pid + '/', data)
    }

    getUsers() {
        return request.get('/v1/users/')
    }

    getTestPlanTestCaseList(data) {
        return request.get('/v1/testplan/testcase/', data)
    }

    deleteTestPlanTestCase(rid) {
        return request.delete('v1/testplan/testcase/' + rid + '/')
    }

    updateTestPlanTestCase(rid, data) {
        return request.put('/v1/testplan/testcase/' + rid + '/', data)
    }

    createTestPlanTestCase(data) {
        return request.post('/v1/testplan/testcase/', data)
    }
}

export default new TestHubApi()