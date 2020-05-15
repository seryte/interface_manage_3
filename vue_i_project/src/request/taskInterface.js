import {deleteRequest, getRequest, postRequest, putRequest} from "./common";

export const getTaskInterface = function (taskId) {
    return getRequest(`api/task_interfaces/?task_id=${taskId}`,)
};


export const addTaskInterface = function (data_list) {
    return postRequest("api/task_interfaces/", data_list)

}

export const deleteTaskInterface = function (taskInterfaceId) {
    // `符号代表编程式字符串，等夹于"api/task/"+ taskId
    return deleteRequest(`api/task_interface/${taskInterfaceId}/`)

}
