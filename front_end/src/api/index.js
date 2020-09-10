import axios from "../utils/request"
import Qs from 'qs'   //引入方式

const api = {
    
    getRegister(params){
        console.log(params);
        let readyData=Qs.stringify({
            username:params.username,
            password:params.password,
            email: params.email
        });
       return axios.post("/api/v1/register",readyData);
    },

    getLogin(params){
        // console.log(params);
        let readyData=Qs.stringify({
            username:params.username,
            password:params.password
        });
        return axios.patch("/api/v1/login",readyData);
    },
    
    getLogout(){
        return axios.patch("/api/v1/logout");
    },


    //成为设备提供者申请
    upgrade_apply(params){
        // console.log(params);
        let readyData=Qs.stringify({
            lab_info:params.lab_info,
            
        });
        // console.log(readyData)
        return axios.put("/api/v1/upgrade",readyData)
    },
    /**
     * provider
     */
    getMyEquipmentList(params){
        return axios.get("/api/v2/equipmentlist",{params})
    },
    modifyEquipment(params){
        // console.log(params);
        let readyData=Qs.stringify({
            id:params.id,
            name:params.name,
            description: params.description,
            count: params.count
        });
        return axios.put("/api/v2/edit",readyData);
    },
    addEquipment(params){
        // console.log(params);
        let readyData=Qs.stringify({
            id: params.id,
            count: params.count
        });
        return axios.post("/api/v2/increase",readyData);
    },
    minusEquipment(params){
        // console.log(params);
        let readyData=Qs.stringify({
            id: params.id,
            count: params.count
        });
        return axios.post("/api/v2/decrease",readyData);
    },

    //获取设备列表
    getequipmentlist(page,name)
    {
        console.log(name)
        return axios.get("/api/v1/search?"+"page="+String(page)+"&name="+name)
    },
    //申请信息列表
    getapplylist()
    {
        return axios.get("/api/v1/applylist")
    },
    //租借成功列表
    getborrowlist()
    {
        return axios.get("/api/v1/borrowlist")
    },




    
}

export default api;