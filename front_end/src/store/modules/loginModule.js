export default {
    namespaced:true,
    state:{
        token:'',
        isProvider:''
    },
    mutations:{
        setToken(state,value){
            state.token = value
        },
        setRole(state,value){
            state.isProvider = value
        },
        clearToken(state){
            state.token = "",
            state.isProvider =false
        }
    }
}