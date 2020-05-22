import {deleteRequest, getRequest, postRequest, putRequest} from "./common";

export const getAllService = function (page,pageSize) {
    return getRequest(`api/services/?page=${page}&pageSize=${pageSize}`,)
};

export const getSingleService = function (serviceId) {
    return getRequest(`api/service/${serviceId}/`,)
};

export const addService = function (data) {
    return postRequest("api/services/", data)

}

export const deleteService = function (serviceId) {
    return deleteRequest(`api/service/${serviceId}/`)

}

export const updateService = function (serviceId, data) {
    return putRequest(`api/service/${serviceId}/`, data)
}