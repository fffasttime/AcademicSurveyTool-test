import './assets/main.css'

import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import BookList from './components/BookList.vue'
import SectionList from './components/SectionList.vue'
import TheWelcome from './components/TheWelcome.vue'

import App from './App.vue'
import PrimeVue from 'primevue/config'
import 'primevue/resources/themes/bootstrap4-light-purple/theme.css'
import 'primeicons/primeicons.css'
import Button from "primevue/button"
import Card from "primevue/card"
import Textarea from "primevue/textarea"
import Rating from "primevue/rating"
import Tag from 'primevue/tag'
import Menu from 'primevue/menu';
import InputText from 'primevue/inputtext';
import Dialog from 'primevue/dialog';
import Ripple from 'primevue/ripple';

const routes = [
    { path: '/', component: TheWelcome },
    { path: '/booklist', component: BookList },
    { path: '/outline', component: SectionList },
]
const router = createRouter({
history: createWebHashHistory(),
routes,
})

const app = createApp(App)
app.use(PrimeVue, { ripple: true })
app.use(router)
app.directive('ripple', Ripple);
app.component('Button', Button)
app.component('Card', Card)
app.component('Textarea', Textarea)
app.component('Rating', Rating)
app.component('Tag', Tag)
app.component('Menu', Menu)
app.component('Dialog', Dialog)
app.component('InputText', InputText)
app.mount('#app')
