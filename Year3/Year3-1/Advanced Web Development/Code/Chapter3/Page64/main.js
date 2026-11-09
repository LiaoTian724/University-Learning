
import { createApp } from 'vue';
import options from './app.vue';

// 找到 HTML 中 id="app" 的元素，把 Vue 应用挂载到这个元素上
createApp(options).mount('#app');