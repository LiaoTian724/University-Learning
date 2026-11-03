<script>

    export default {
        data() {
            return {
                sortBy: 'default',
                errorMessage: '',

                participants: [
                    {id: 0, name:"Michael Jason", age:23, attempt_1: 274, attempt_2:147, attempt_3: 223},
                    {id: 1, name:'Zhang San',     age:18, attempt_1: 86,  attempt_2:455, attempt_3: 312}
                ],

                showForm: false,
                nextId: 2,
                form: {name:'',    age:null,     attempt_1:null,   attempt_2:null,   attempt_3:null}
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
                if (confirm('Are you sure you want to delete this record?')) {
                    this.participants = this.participants.filter(person=>person.id != id);
                }
            },

            addParticipant() {
                this.errorMessage = '';
                
                if (this.form.name == '') {
                    this.errorMessage = 'Please enter a name';
                    return;
                }
                if (this.form.age == '' || Number(this.form.age) < 0 || !Number.isInteger(Number(this.form.age))) {
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
                    id: this.nextId++,
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
    <div class="page">
        <!-- <h2>Reaction Time Records</h2> -->

        <button class="add-button" @click="showForm=true">Add New Record</button>

        <span>Sort by: </span>
        <select v-model="sortBy">
            <option value="default">Original Order</option>
            <option value="name">Name</option>
            <option value="age">Age</option>
            <option value="best">Best Record</option>
        </select>

        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Age</th>
                    <th>Attempt 1</th>
                    <th>Attempt 2</th>
                    <th>Attempt 3</th>
                    <th>Best</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="person in sortedParticipants" :key="person.id">
                    <td>{{ person.name }}</td>
                    <td>{{ person.age }}</td>
                    <td>{{ person.attempt_1 }}</td>
                    <td>{{ person.attempt_2 }}</td>
                    <td>{{ person.attempt_3 }}</td>
                    <td :class="{ fast: bestTime(person) < 100 }">{{ bestTime(person) }}</td>
                    <td>
                        <button class="delete-button" @click="deleteParticipant(person.id)">Delete</button>
                    </td>
                </tr>
            </tbody>
        </table>

        <div v-if="showForm" class="background">
                <div class="popup">
                    <button class="close-button" @click="showForm=false">×</button>

                    <h3>Add a New Participant</h3>
                    <div class="form-row"><label>Name:</label> <input v-model="form.name" placeholder="Name"></div>
                    <div class="form-row"><label>Age:</label>
                        <div class="number-box">
                            <button @click="form.age = Math.max(1, form.age-1)">-</button>
                            <input v-model.number="form.age" type="number">
                            <button @click="form.age++">+</button>
                        </div>
                    </div>
                    <div class="form-row"><label>Record 1:</label>
                        <div class="number-box">
                            <button @click="form.attempt_1 = Math.max(0, form.attempt_1-1)">-</button>
                            <input v-model.number="form.attempt_1" type="number">
                            <button @click="form.attempt_1++">+</button>
                        </div>
                    </div>
                    <div class="form-row"><label>Record 2:</label>
                        <div class="number-box">
                            <button @click="form.attempt_2 = Math.max(0, form.attempt_2-1)">-</button>
                            <input v-model.number="form.attempt_2" type="number">
                            <button @click="form.attempt_2++">+</button>
                        </div>
                    </div>
                    <div class="form-row"><label>Record 3:</label>
                        <div class="number-box">
                            <button @click="form.attempt_3 = Math.max(0, form.attempt_3-1)">-</button>
                            <input v-model.number="form.attempt_3" type="number">
                            <button @click="form.attempt_3++">+</button>
                        </div>
                    </div>
                   
                    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
                    <button class="create-button" @click="addParticipant()">Create</button>
                </div>

        </div>

    </div>
</template>




<style scoped>
.page {padding: 20px;}

.add-button, .create-button {
    background-color: #009dff;
    color: white;
    border: none;
    padding: 10px;
    border-radius: 4px;
}

.add-button {
    margin-right: 20px;
}


table {
    margin-top: 20px;
    border-collapse: collapse;
}

th, td {
    padding: 8px;
    text-align: center;
}


.delete-button {
    background-color: #ff5962;
    color: white;
    border: none;
    padding: 8px;
    border-radius: 4px;
}


.fast, .error {
    color: red;
}


.background {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: #0006;
    display: flex;
    justify-content: center;
    align-items: center;
}


.popup {
    background-color: white;
    padding: 25px;
    border-radius: 5px;
    width: 350px;
}


.form-row {
    display: flex;
    margin-bottom: 15px;
}

.form-row label {
    width: 90px;
}


.form-row input {
    width: 200px;
    padding: 7px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.number-box {
    display: flex;
}

.number-box input {
    width: 70px;
    text-align: center;
    border-radius: 0;
    appearance: textfield;
}

.number-box input::-webkit-inner-spin-button,
.number-box input::-webkit-outer-spin-button {
    -webkit-appearance: none;
}

.number-box button {
    width: 35px;
    border: 1px solid #ddd;
    background-color: #f5f5f8;
    color: #666;
    cursor: pointer;
}


.close-button {
    float: right;
}
</style>
