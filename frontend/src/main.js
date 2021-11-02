import Vue from 'vue'
import App from './App.vue'

Vue.config.productionTip = false

import VueSweetalert2 from 'vue-sweetalert2'
Vue.use(VueSweetalert2);

new Vue({
  render: h => h(App),
}).$mount('#app')
