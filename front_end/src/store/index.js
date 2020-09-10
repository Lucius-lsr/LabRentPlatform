import Vue from 'vue'
import Vuex from 'vuex'
import LoginModule from "./modules/loginModule"

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    LoginModule
  }
})
