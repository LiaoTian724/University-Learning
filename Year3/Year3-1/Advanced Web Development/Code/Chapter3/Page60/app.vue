<!-- 
<template>
    <p>The time now is</p>

    <div class='clock'>
        {{ timeNow }}
    </div>
</template>

<script>
    export default {
        data() {
            return {
                timeNow: new Date().toLocaleTimeString(),
                timerId: null
            };
        },

        mounted() {
            this.timeNow = (new Date()).toLocaleTimeString();

            this.timerId = setInterval(() => {
                this.timeNow = (new Date()).toLocaleTimeString();
            }, 1000);
        },

        unmounted() {
            clearInterval(this.timerId);
        }
    };
</script>

<style scoped>
    .clock {
        padding: 2px;
        width: 10em;
        border: 1px solid gray;
        text-align: center;
    }
</style> -->




<template>
    <div class='page'>
        
        <h1>Page60 - Vue Compoenent Practice</h1>

        <h2>1. Clock Component</h2>

        <Clock title='London' timeZone='Europe/London'></Clock>
        <Clock title='New York' timeZone='America/New_York'></Clock>
        

        <h2>2. Weather Component</h2>

        <Weather />

        <h2>3. Rating Components</h2>
        <Rating title='Course A' :initialValue='3'></Rating>
        <Rating title='Course B' :initialValue='1'></Rating>

        <h2>4. Button Counter Component</h2>
        <ButtonCounter />

        <h2>5. Blog Post Component</h2>
        <BlogPost title="My journey with Vue" />
        <BlogPost title="Blogging with Vue" />
        <BlogPost title="Why Vue is so fun" />
        
    </div>
</template>


<script>
    import Clock from './components/Clock.vue';
    import Weather from './components/Weather.vue';
    import Rating from './components/Rating.vue';
    import ButtonCounter from './components/ButtonCounter.vue';
    import BlogPost from './components/BlogPost.vue';


    export default {
        components: {
            Clock,
            Weather,
            Rating,
            ButtonCounter,
            BlogPost
        }
    };
</script>



<style scoped>
    .page {
        font-family: Arial, sans-serif;
        margin: 25px;
    }

    h2 {
        margin-top: 30px;
    }
</style>
