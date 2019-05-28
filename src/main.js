import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import router from './router'
import store from './store'
import './registerServiceWorker'
import Vuetify from 'vuetify'

Vue.config.productionTip = false
Vue.use(Vuetify, {
    theme: {
        primary: '#4CAF50',
        accent: '#FF5722',
    }
})

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')
