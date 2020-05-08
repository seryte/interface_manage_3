import {deleteRequest, getRequest, postRequest, putRequest} from "./common";

export const getAllTask = function () {
    return getRequest("api/task/",)
};

export const getSingleTask = function (taskId) {
    return getRequest(`api/service/${taskId}`,)
};

export const addTask = function (data) {
    return postRequest("api/task", data)

}

export const deleteTask = function (taskId) {
    // `符号代表编程式字符串，等夹于"api/task/"+ taskId
    return deleteRequest(`api/task/${taskId}`)

}

export const updateTask = function (taskId, data) {
    return putRequest(`api/task/${taskId}`, data)
}