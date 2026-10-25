<script setup>
    import {ref, computed} from 'vue';

    const participants = ref([
        {id: 12, name:"Michael Jason", age:23, attempt_1: 274, attempt_2:147, attempt_3: 223},
        {id: 13, name:'Zhang San',     age:18, attempt_1: 86,  attempt_2:455, attempt_3: 312}
    ]);
    
    const compare = (a, b) => {
        if (a - b > 0) return 1;
        if (a - b < 0) return -1;
        return 0;

    };
    function sortTime(person) {
        let time = [person.attempt_1, person.attempt_2, person.attempt_3];
        return time.sort(compare);
    };

    function bestTime(person) {
        let sorted_min = sortTime(person);
        return sorted_min[0];
    };

    function sortParticipants(type) {
        if (type == 'name') {
            participants.value.sort((a,b)=>{
                return a.name.localeCompare(b.name);
            });
        }
        
        if (type == 'age') {
            participants.value.age.sort((a,b)=>{
                return a - b;
            });
        }
    }
</script>

<template>
    <table>
        <tr>
            <th>Name</th> <th>Age</th> <th>Attempt 1</th> <th>Attempt 2</th> <th>Attempt 3</th>
            <th>Best</th>
        </tr>

        <tr v-for="person in participants">
            <td>{{ person.name }}</td>
            <td>{{ person.age }}</td>
            <td>{{ person.attempt_1 }}</td>
            <td>{{ person.attempt_2 }}</td>
            <td>{{ person.attempt_3 }}</td>
            <td>{{ bestTime(person) }}</td>
        </tr>
    </table>

</template>

<style scoped>

</style>