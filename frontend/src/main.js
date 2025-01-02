import {createApp} from 'vue'
import App from '@/App.vue'
import router from '@/router/router'
import store from "@/store";

import NavBar from "@/components/NavBar.vue";



const app = createApp(App)

app.component('NavBar', NavBar);
app.use(router)
app.use(store)
app.mount('#app')
