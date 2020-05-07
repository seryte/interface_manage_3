import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    props: {
      menu: "service"
    },
    children: [
      {
        path: "service",
        name: "service",
        component: () => import("../views/service/index.vue")
      }
    ]
  },
  {
    path: '/',
    name: 'Home',
    component: Home,
    props: {
      menu: "task"
    },
    children: [
      {
        path: "task",
        name: "task",
        component: () => import("../views/task/index.vue")
      }
    ]
},

  {
    path: '/login',
    name: 'login',
    component: () => import('../views/login')
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
