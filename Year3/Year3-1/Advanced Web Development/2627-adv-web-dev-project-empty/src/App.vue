<script>

    import FormCreate from "./FormCreate.vue";
    import FormEdit from "./FormEdit.vue";

    export default {
        components: {FormCreate, FormEdit},
        data() {
            return {
                sortBy: 'default',
                pageError: '',
                participants:[],
            };
        },
        mounted() {this.loadParticipants();},

        methods: {
            async loadParticipants() {
                this.pageError = '';
                try {
                    const response = await fetch("/api/records", {
                        method: 'GET'
                    });
                    if (!response.ok) {
                        throw new Error('Failed to load records');
                    }
                    const data = await response.json();
                    this.participants = data;
                } catch (error) {
                    console.log(error);
                    this.pageError = 'Cannot load records';
                }
            },

            sortTime(person) {
                let time = [person.record_1, person.record_2, person.record_3];
                return time.sort((a,b)=>a-b);
            },

            bestTime(person) {
                let sorted = this.sortTime(person);
                return sorted[0];
            },


            async deleteParticipant(id) {
                if (!confirm("Are you sure you want to delete this record?")) { return; }
                this.pageError = '';
                try {
                    const response = await fetch(`/api/records/${id}`, {
                        method:'DELETE'
                    });
                    if (!response.ok) {
                        throw new Error('Failed to delete record');
                    }
                    await this.loadParticipants();
                } catch (error) {
                    console.log(error);
                    this.pageError = 'Cannot delete record';
                }
            }, 

            // 父组件 调用 子组件 $refs
            handleCreate() {
                this.$refs.formCreate.showDialog();
            },

            async handleFormCreateConfirm(rec) {
                this.pageError = '';
                try {
                    const response = await fetch('/api/records', {
                        method: 'POST',
                        headers: {"Content-Type": 'application/json'},
                        body: JSON.stringify(rec)
                    });
                    const data = await response.json();
                    if (!response.ok) {
                        throw new Error(data.error || "Failed to add record");
                    }
                    this.participants.push(data);
                    this.$refs.formCreate.closeDialog();
                } catch (error) {
                    console.log(error),
                    this.pageError = "Cannot add record";
                }
            },
            
            handleEdit(person) {
                this.$refs.formEdit.showDialog(person);
            },

            async handleFormEditConfirm(rec) {
                this.pageError = '';
                try {
                    const response = await fetch(`/api/records/${rec.id}`, {
                        method: 'PUT', 
                        headers: {'Content-Type': 'application/json'}, 
                        body: JSON.stringify(rec)
                    });

                    const data = await response.json();
                    if (!response.ok) {throw new Error(data.error || 'Failed to update record');}

                    this.$refs.formEdit.closeDialog();
                    await this.loadParticipants();
                } catch (error) {
                    console.log(error);
                    this.pageError = 'Cannot update record';
                }
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

        <div class="toolbar">
            <el-button type="primary" @click="handleCreate"> Add New Record </el-button>
            <span>Sort by:</span>

            <el-select v-model="sortBy" style="width: 200px">
                <el-option label="Original Order" value="default" />
                <el-option label="Name" value="name" />
                <el-option label="Age" value="age" />
                <el-option label="Best Record" value="best" />
            </el-select>
        </div>


        <p v-if="pageError" class="error"> {{ pageError }} </p>


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

                        <td :class="{ fast: bestTime(person) < 100 }"> {{ bestTime(person) }} </td>
                        <td>
                            <el-button type="primary" size="small" @click="handleEdit(person)">Edit</el-button>
                            <el-button type="danger" size="small" @click="deleteParticipant(person.id)"> Delete </el-button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>


        <form-create  ref="formCreate"  @confirm="handleFormCreateConfirm"/>
        <form-edit  ref="formEdit"  @confirm="handleFormEditConfirm"/>
    </div>
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
}

</style>