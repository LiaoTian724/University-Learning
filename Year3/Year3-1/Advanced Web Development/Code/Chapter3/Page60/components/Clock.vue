
<template>
    <div class='clock'>

        <h3>{{ title }}</h3>
        <p>{{ timeNow }}</p>
    </div>
</template>


<script>
    export default {
        props: {
            title: String,
            timeZone: String
        },

        data() {
            return {
                timeNow: "",
                timerId: null
            };
        },

        methods: {
            updateTime() {
                this.timeNow = new Date().toLocaleTimeString(
                    'en-GB',
                    {timeZone: this.timeZone}
                );
            }
        },

        mounted() {
            this.updateTime();

            this.timerId = setInterval(() => {
                this.updateTime();
            }, 1000);
        },
        unmounted() {
            clearInterval(this.timerId);
        }
    };
</script>




<style scoped>
    .clock {
        border: 1px solid gray;
        padding: 12px;
        margin-bottom: 10px;
        width: 230px;
        border-radius: 6px;
    }

    .clock h3 {
        margin: 0;
    }

    .clock p {
        font-size: 24px;
    }
</style>