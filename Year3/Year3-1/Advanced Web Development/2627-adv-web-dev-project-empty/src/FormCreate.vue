<script>
export default {
    emits: ["cancel", "confirm"],

    data() {
        return {
            dialogVisible: false,
            errorMessage: "",
            form: {name: "", age: null, record_1: null, record_2: null, record_3: null}
        };
    },

    methods: {
        showDialog() {
            this.form = {name: "", age: null, record_1: null, record_2: null, record_3: null};
            this.errorMessage = "";
            this.dialogVisible = true;
        },

        handleCancel() {
            this.dialogVisible = false;
            this.$emit("cancel");
        },

        handleConfirm() {
            this.errorMessage = "";

            if (!this.form.name.trim()) {
                this.errorMessage = "Please enter a name";
                return;
            }

            if (!Number.isInteger(this.form.age) || this.form.age < 1) {
                this.errorMessage = "Please enter a valid age";
                return;
            }

            const records = [this.form.record_1, this.form.record_2,  this.form.record_3];

            if (!records.every(value => Number.isInteger(value) && value >= 0)) {
                this.errorMessage = "Please enter valid records";
                return;
            }

            const record = {
                name: this.form.name.trim(),
                age: this.form.age,
                record_1: this.form.record_1,
                record_2: this.form.record_2,
                record_3: this.form.record_3
            };

            this.dialogVisible = false;
            this.$emit("confirm", record);
        }
    }
};
</script>


<template>
    <el-dialog v-model="dialogVisible" title="Add a New Participant" width="500px">
        <el-form :model="form" label-width="110px">
            <el-form-item label="Name"> <el-input v-model="form.name" placeholder="Enter name" /> </el-form-item>
            <el-form-item label="Age"> <el-input-number v-model="form.age" :min="1" :step="1" :precision="0" /> </el-form-item>

            <el-form-item label="Record 1"> <el-input-number v-model="form.record_1" :min="0" :step="1" :precision="0" /> </el-form-item>
            <el-form-item label="Record 2"> <el-input-number v-model="form.record_2" :min="0" :step="1" :precision="0" /> </el-form-item>
            <el-form-item label="Record 3"> <el-input-number v-model="form.record_3" :min="0" :step="1" :precision="0" /> </el-form-item>
            <p v-if="errorMessage" class="error"> {{ errorMessage }} </p>
        </el-form>

        <template #footer>
            <el-button @click="handleCancel"> Cancel </el-button>
            <el-button type="primary" @click="handleConfirm"> Confirm </el-button>
        </template>
    </el-dialog>
</template>


<style scoped>
.error {
    color: red;
    margin-left: 110px;
}
</style>
