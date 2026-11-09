
<template>
    <div class='rating'>

        <h3>{{ title }}</h3>

        <p>Rating: {{ rating }}</p>

        <!-- :key 等价于 v-bind:key='n' key用来标识列表中的每个元素 -->
        <!-- :class="{selected: true}" 表示选择 :class属性 -->
        <!-- v-on:click= 等价于 @click= , 调用 methods 里面的 setRating 方法 -->
        <button 
            v-for='n in 5'
            :key='n'  
            class='star'
            :class="{ selected: n <= rating }"
            v-on:click='setRating(n)'
        >
            *
        </button>

        <p>
            <input
                type='range'
                min='0'
                max='5'
                v-model.number='rating'
            > 
            <!-- v-model.number 是将输入值转换为数字, 不需要声明, 直接使用 -->
        </p>

        <button @click='reset'>Reset</button>

        <p v-if='rating >= 4'>High rating!</p>
        <p v-else> Try selecting four or five stars.</p>
    </div>
</template>


<script>
    export default {
        props: {
            title: {
                type: String,
                default: 'Rating'
            },

            initialValue: {
                type: Number,
                default: 0
            }
        },

        data() {
            return {
                rating: this.initialValue
            };
        },

        methods: {
            setRating(n) {
                this.rating = n;
            },
            reset() {
                this.rating = 0;
            }
        }
    };
</script>


<style scoped>
    .rating {
        border: 1px solid gray;
        border-radius: 6px;
        padding: 12px;
        margin-bottom: 10px;
    }

    .star {
        font-size: 30px;
        color: lightgray;
        border: none;
        background: none;
        cursor: pointer;
    }

    .selected {
        color: orange;
    }

    button {
        margin-right: 5px;
    }
</style>