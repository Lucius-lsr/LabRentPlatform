import Vue from 'vue'
import VueRouter from 'vue-router'
import Layout from "../pages/Layout.vue"
// import Home from '../pages/Home.vue'
import Login from "../pages/Login.vue"
import UCenter from "../pages/UCenter.vue"

import Page400 from "../pages/errorPage/400.vue"
import Page401 from "../pages/errorPage/401.vue"
import Page404 from "../pages/errorPage/404.vue"
import Provider from "../pages/provider/ProviderHome.vue"
import MyEquipmentList from "../pages/provider/main/MyEquipmentList.vue"
import MyEquipmentDetails from "../pages/provider/main/MyEquipmentDetails.vue"
import equipmentlist from '../pages/User/Equipmentlist.vue';
import applylist from '../pages/User/Applylist.vue';
import borrowlist from '../pages/User/Borrowlist.vue';


Vue.use(VueRouter)

const routes = [
  {
    path: "/login",
    name: "Login",
    component: Login
  },
  {
    path: "/",
    name: "Layout",
    redirect: {
      path:'/equipmentlist'
    },
    component: Layout,
    children: [
      
      {
        path: "/ucenter",
        name: "UCenter",
        component: UCenter,
        meta: {
           isLogin: true
        }
      },
      {
        path: "/equipmentlist",
        name: "equipmentlist",
        component: equipmentlist,
        meta: {
                // isLogin: true,
        },
      },
      {
        path: "/applylist",
        name: "applylist",
        component: applylist,
        meta: {
           isLogin: true
        }
      },
      {
        path: "/borrowlist",
        name: "borrowlist",
        component: borrowlist,
        meta: {
           isLogin: true
        }
      },
      {
        path: '/provider',
        name: 'Provider',
        component: Provider,
        meta: {
            isLogin: true,
            isProvider: true
        },
        children: [
          {
            path: '/provider/myequipmentlist',
            name: 'MyEquipmentList',
            component: MyEquipmentList,
            meta: {
                isLogin: true,
                isProvider: true
            },
          },
          {
            path: '/provider/myequipmentdetails',
            name: 'MyEquipmentDetails',
            component: MyEquipmentDetails,
            meta: {
                isLogin: true,
                isProvider: true
            },
          }
        ]
      },
      
      
    ]
  },
  {
    path: '/401',
    name: 'page401',
    component: Page401,
  },
  {
    path: '/404',
    name: 'page404',
    component: Page404,
  },
  {
    path: '/400',
    name: 'page400',
    component: Page400,
  },
  
  
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
    if (to.meta.isLogin) {
        // 是否登陆
        const token = localStorage.getItem('token')
        if (token) {
          next();
        }
        else {
          next({
            //回到登录页面
            path: "/login"
          })
        }
      }
      else {
        next();
      }
})


export default router
