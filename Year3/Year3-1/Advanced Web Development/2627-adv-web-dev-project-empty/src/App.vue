<script>

    export default {
        data() {
            return {
                sortBy: 'default',
                errorMessage: '',

                participants: [
                    {id: 12, name:"Michael Jason", age:23, attempt_1: 274, attempt_2:147, attempt_3: 223},
                    {id: 13, name:'Zhang San',     age:18, attempt_1: 86,  attempt_2:455, attempt_3: 312}
                ],

                showForm: false,
                form: {name:'',    age:'',     attempt_1:'',   attempt_2:'',   attempt_3:''}
            };
        },

        methods: {
            sortTime(person) {
                let time = [person.attempt_1, person.attempt_2, person.attempt_3];
                return time.sort((a,b)=>a-b);
            },

            bestTime(person) {
                let sorted = this.sortTime(person);
                return sorted[0];
            },

            deleteParticipant(id) {
                this.participants = this.participants.filter(person=>person.id != id);
            },

            addParticipant() {
                this.errorMessage = '';
                
                if (this.form.name == '') {
                    this.errorMessage = 'Please enter a name';
                    return;
                }
                if (this.form.age == '' || Number(this.form.age) < 0) {
                    this.errorMessage = 'Please enter a valid age';
                    return;
                }
                if (this.form.attempt_1 == '' || Number(this.form.attempt_1) < 0 || 
                    this.form.attempt_2 == '' || Number(this.form.attempt_2) < 0 ||
                    this.form.attempt_3 == '' || Number(this.form.attempt_3) < 0) {
                    this.errorMessage = 'Please make sure all attempts are correct';
                    return;
                }
                for (let i=0; i < this.participants.length; i++) {
                    if(this.participants[i].name == this.form.name) {
                        this.errorMessage = 'This name already exists';
                        return;
                    }
                }

                this.participants.push({
                    id: this.participants[this.participants.length - 1].id + 1,
                    name: this.form.name,
                    age: Number(this.form.age),
                    attempt_1: Number(this.form.attempt_1),
                    attempt_2: Number(this.form.attempt_2),
                    attempt_3: Number(this.form.attempt_3)
                });
                this.showForm = false;
                this.form = {name:'',    age:'',     attempt_1:'',   attempt_2:'',   attempt_3:''};
                this.errorMessage = '';
            }
        },

        computed: {
            sortedParticipants() {
                let result = [...this.participants];
                
                if (this.sortBy == 'name') {
                    result.sort((a,b) => a.name.localeCompare(b.name));
                }
                if (this.sortBy == 'age') {
                    result.sort((a,b) => a.age - b.age);
                }
                if (this.sortBy == 'best') {
                    result.sort((a,b) => this.bestTime(a) - this.bestTime(b));
                }

                return result;
            }
        }
    }
</script>

<template>

    <label>Sort by:</label>

    <select v-model="sortBy">
        <option value="default">Original Order</option>
        <option value="name">Name</option>
        <option value="age">Age</option>
        <option value="best">Best</option>
    </select>

    <button @click="showForm=true">Add New Record</button>
    <div v-if="showForm">
        <h3>Add New Participant</h3>

        <p>Name:</p> <input v-model="form.name" placeholder="Name">
        <p>Age:</p> <input v-model="form.age" placeholder="number">
        <p>Attempt 1:</p> <input v-model="form.attempt_1" placeholder="number">
        <p>Attempt 2:</p> <input v-model="form.attempt_2" placeholder="number">
        <p>Attempt 3:</p> <input v-model="form.attempt_3" placeholder="number">
        <p>
            <button @click="showForm=false">Cancel</button>
            <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
            <button @click="addParticipant()">Create</button>
        </p>
    </div>


    <table>
        <tr>
            <th>Name</th> <th>Age</th> <th>Attempt 1</th> <th>Attempt 2</th> <th>Attempt 3</th>
            <th>Best</th><th>Action</th>
        </tr>

        <tr v-for="person in sortedParticipants">
            <td>{{ person.name }}</td>
            <td>{{ person.age }}</td>
            <td>{{ person.attempt_1 }}</td>
            <td>{{ person.attempt_2 }}</td>
            <td>{{ person.attempt_3 }}</td>
            <td :class="{ fast: bestTime(person) < 100 }">{{ bestTime(person) }}</td>
            <td>
                <button @click="deleteParticipant(person.id)">Delete</button>
            </td>
        </tr>
    </table>

    

</template>

<style scoped>
    .fast {
        color: red;
        font-weight: bold;
    };

    .error {
        color: red;
    }
</style>