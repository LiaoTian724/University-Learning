<script>

    export default {
        data() {
            return {
                sortBy: 'default',
                errorMessage: '',

                participants: [
                    {id: 0, name:"Michael Jason", age:23, record_1: 274, record_2:147, record_3: 223},
                    {id: 1, name:'Zhang San',     age:18, record_1: 86,  record_2:455, record_3: 312},
                    {id: 2, name:'Albert Bappu',  age:47, record_1: 352, record_2:243, record_3: 366},
                    {id: 3, name:'Tai Man Chan',  age:23, record_1: 274, record_2:176, record_3: 233},
                ],

                showForm: false,
                
                nextId: 4,
                form: {name:'',    age:null,     record_1:null,   record_2:null,   record_3:null}
            };
        },

        methods: {
            sortTime(person) {
                let time = [person.record_1, person.record_2, person.record_3];
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
                if (this.form.age == '' || this.form.age < 1 || !Number.isInteger(Number(this.form.age))) {
                    this.errorMessage = 'Please enter a valid age';
                    return;
                }
                if (this.form.record_1 == null || this.form.record_1 < 0 || 
                    this.form.record_2 == null || this.form.record_2 < 0 ||
                    this.form.record_3 == null || this.form.record_3 < 0) {
                    this.errorMessage = 'Please make sure all attempts are correct';
                    return;
                }
                // for (let i=0; i < this.participants.length; i++) {
                //     if (this.participants[i].name == this.form.name) {
                //         this.errorMessage = 'This name already exists';
                //         return;
                //     }
                // }

                this.participants.push({
                    id: this.nextId++,
                    name: this.form.name,
                    age: this.form.age,
                    record_1: this.form.record_1,
                    record_2: this.form.record_2,
                    record_3: this.form.record_3
                });
                this.showForm = false;
                this.form = {name:'',    age:null,     record_1:null,   record_2:null,   record_3:null};
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
        <div class="toolbar">
            <!-- <button class="add-button" @click="showForm=true">Add New Record</button> -->
            <el-button type="primary" @click="showForm=true">Add New Record</el-button>

            <span>Sort by:</span>
            <!-- <select v-model="sortBy">
                <option value="default">Original Order</option>
                <option value="name">Name</option>
                <option value="age">Age</option>
                <option value="best">Best Record</option>
            </select> -->
            <el-select v-model="sortBy" style="width: 200px;">
                <el-option label="Original Order" value="default"></el-option>
                <el-option label="Name" value="name"></el-option>
                <el-option label="Age" value="age"></el-option>
                <el-option label="Best Record" value="best"></el-option>
            </el-select>
        </div>

        <div class="table-container">
            <table class="record-table">
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
                        <td>{{ person.record_1 }}</td>
                        <td>{{ person.record_2 }}</td>
                        <td>{{ person.record_3 }}</td>
                        <td :class="{ fast: bestTime(person) < 100 }">{{ bestTime(person) }}</td>
                        <td>
                            <!-- <button class="delete-button" @click="deleteParticipant(person.id)">Delete</button> -->
                            <el-button type="danger" @click="deleteParticipant(person.id)">Delete</el-button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- <div v-if="showForm" class="background">
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
                            <button @click="form.record_1 = Math.max(0, form.record_1-1)">-</button>
                            <input v-model.number="form.record_1" type="number">
                            <button @click="form.record_1++">+</button>
                        </div>
                    </div>
                    <div class="form-row"><label>Record 2:</label>
                        <div class="number-box">
                            <button @click="form.record_2 = Math.max(0, form.record_2-1)">-</button>
                            <input v-model.number="form.record_2" type="number">
                            <button @click="form.record_2++">+</button>
                        </div>
                    </div>
                    <div class="form-row"><label>Record 3:</label>
                        <div class="number-box">
                            <button @click="form.record_3 = Math.max(0, form.record_3-1)">-</button>
                            <input v-model.number="form.record_3" type="number">
                            <button @click="form.record_3++">+</button>
                        </div>
                    </div>
                   
                    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
                    <button class="create-button" @click="addParticipant()">Create</button>
                </div>

        </div>  -->
    </div> 

    <el-dialog v-model="showForm" title="Add a New Participant">
        <el-form label-width="90px">
            <el-form-item label="Name">
                <el-input v-model="form.name" placeholder="Enter name"></el-input>
            </el-form-item>
            <el-form-item label="Age">
                <el-input-number v-model="form.age" :min="1" :step="1" placeholder="Enter age"></el-input-number>
            </el-form-item>
            <el-form-item label="Record 1">
                <el-input-number v-model="form.record_1" :min="0" :step="1" placeholder="Enter record 1"></el-input-number>
            </el-form-item>
            <el-form-item label="Record 2">
                <el-input-number v-model="form.record_2" :min="0" :step="1" placeholder="Enter record 2"></el-input-number>
            </el-form-item>
            <el-form-item label="Record 3">
                <el-input-number v-model="form.record_3" :min="0" :step="1" placeholder="Enter record 3"></el-input-number>
            </el-form-item>

            <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        </el-form>

        <template #footer>
                <el-button @click="showForm=false">Cancel</el-button>
                <el-button type="primary" @click="addParticipant">Create</el-button>
        </template>
    </el-dialog>
</template>




<style scoped>

.page {
    padding: 20px;
    max-width: 1100px;
    margin: 0 auto;
}

.toolbar {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
    flex-wrap: wrap;
}

.table-container {
    width: 100%;
    overflow-x: auto;
}

.record-table {
    width: 100%;
    border-collapse: collapse;
}

.record-table th,
.record-table td {
    border: 1px solid #ddd;
    padding: 10px;
    text-align: center;
}

.record-table th {
    background-color: #f2f2f2;
}

.record-table tbody tr:nth-child(even) {
    background-color: #fafafa;
}

.fast {
    color: red;
    font-weight: bold;
}

.error {
    color: red;
    margin: 0 0 10px;
}

</style>