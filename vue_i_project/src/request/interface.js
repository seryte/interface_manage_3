import {deleteRequest, getRequest, postRequest, putRequest} from "./common";

export const getInterfaces = function (serviceId) {
    return getRequest(`api/interfaces/?service_id=${serviceId}`)
};

export const addInterface = function (data) {
    return postRequest("api/interfaces/", data)

}

export const deleteInterface = function (interfaceId) {
    return deleteRequest(`api/interface/${interfaceId}/`)

}

export const updateInterface = function (interfaceId, data) {
    return putRequest(`api/interface/${interfaceId}/`, data)
}