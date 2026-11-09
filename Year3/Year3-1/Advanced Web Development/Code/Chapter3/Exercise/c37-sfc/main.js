// main.js loaded by HTML

// import 'createApp' from the Vue library as a module
import { createApp } from "vue";

// import the options object from the SFC
import opts from "./app.vue";

const vm = createApp(opts).mount('#app');

// globalThis.vm = vm;
