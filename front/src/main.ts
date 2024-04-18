import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'
import './style.css'
import App from '@/App.vue'

import MainView from '@/views/MainView.vue'
import HelpView from '@/views/HelpView.vue'

const pinia = createPinia()
const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '', component: MainView },
        { path: '/help', component: HelpView },
    ]
})

createApp(App).use(router).use(pinia).mount('#app')
