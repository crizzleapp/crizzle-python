import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('./views/Home.vue')
    },
    {
      path: '/data',
      name: 'data',
      component: () => import('./views/Data.vue')
    },
    {
      path: '/research',
      name: 'research',
      component: () => import('./views/Research.vue')
    },
    {
      path: '/portfolio',
      name: 'portfolio',
      component: () => import('./views/Portfolio.vue')
    },
    {
      path: '/backtesting',
      name: 'backtesting',
      component: () => import('./views/Backtesting.vue')
    },
    {
      path: '/trading',
      name: 'trading',
      component: () => import('./views/Trading.vue')
    },
    {
      path: '/configuration',
      name: 'configuration',
      component: () => import('./views/Configuration.vue')
    },
    {
      path: '/docs',
      name: 'docs',
      component: () => import('./views/Docs.vue')
    },
  ]
})
