import request from '@/HttpCommon.js'


class TestHubApi {
    getTestHubList(data) {
      return request.get('/v1/testhub/', data)
    }

    getTestHub(tid) {
      return request.get('/v1/testhub/'+tid+'/')
    }

    deleteTestHub(tid) {
      return request.delete('/v1/testhub/'+tid+'/')
    }
  
    createTestHub(data) {
      return request.post('/v1/testhub/', data)
    }
  
    updateTestHub(tid, data) {
      return request.put('/v1/testhub/'+tid+'/', data)
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
        return request.get('/v1/testmodule/'+tid+'/')
    }

    deleteTestCaseModule(tid) {
        return request.delete('/v1/testmodule/'+tid+'/')
    }

    createTestCaseModule(data) {
        return request.post('/v1/testmodule/', data)
    }

    updateTestCaseModule(tid, data) {
        return request.put('/v1/testmodule/'+tid+'/', data)
    }
  }
  
  export default new TestHubApi()