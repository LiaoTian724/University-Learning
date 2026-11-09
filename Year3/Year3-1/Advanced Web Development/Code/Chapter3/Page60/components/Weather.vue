
<template>
    <div class='weather'>

        <h3>Weather Information</h3>

        <p v-if='cities.length === 0'>
            No weather information.
        </p>

        <table v-else>
            <tr>
                <th>City</th>
                <th>Temperature</th>
            </tr>

            <template v-for='c in cities' :key='c.id'>
                <tr v-if='c.temperature > 27'>
                    <td>{{ c.cityName }}</td>
                    <td>{{ c.temperature }} °C</td>
                </tr>
            </template>
        </table>

        <p>Total records: {{ cities.length }}</p>
        <p>Only temperature above 27 °C are displayed.</p>

        <input 
            v-model='newCityName'
            placeholder='City Name'
        >
        
        <input 
            v-model.number='newTemperature'
            type='number'
            placeholder='Temperature'
        >

        <button @click='addCity'>Add City</button>
        <button v-on:click='clearCities'>Clear</button>
    </div>
</template>


<script>
    export default {
        data() {
            return {
                cities: [
                    { id: 1, cityName: 'London', temperature: 28 },
                    { id: 2, cityName: 'New York', temperature: 30 },
                    { id: 3, cityName: 'Tokyo', temperature: 25 }
                ],

                newCityName: '',
                newTemperature: "",
                nextId: 4
            };
        },

        methods: {
            addCity() {
                if (this.newCityName && this.newTemperature) {
                    this.cities.push({
                        id: this.nextId,
                        cityName: this.newCityName,
                        temperature: this.newTemperature
                    });

                    this.nextId++;

                    this.newCityName = '';
                    this.newTemperature = '';
                }
            },

            clearCities() {
                this.cities = [];
            }
        }
    };
</script>


<style scoped>
    .weather {
        border: 1px solid gray;
        border-radius: 6px;
        padding: 12px;
        margin-bottom: 20px;
    }

    table {
        border-collapse: collapse;
        margin-bottom: 12px;
    }

    td, th {
        border: 1px solid gray;
        padding: 8px;
    }

    input {
        margin: 5px;
        padding: 5px;
        width: 140px;
    }

    button {
        margin: 5px;
        padding: 5px 10px;
    }
</style>