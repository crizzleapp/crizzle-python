<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
    <div>
        <v-dialog v-model="dialog"></v-dialog>
        <v-data-table :items="apiKeys" :headers="headers">
            <template v-slot:items="props">
                <td>{{props.item.service}}</td>
                <td>{{props.item.name}}</td>
                <td>{{props.item.modified}}
                    <v-icon class="info--text mx-2" @click="editKey(props.item)">edit</v-icon>
                    <v-icon class="red--text mx-2" @click="deleteKey(props.item)">delete</v-icon>
                </td>
                <td class="px-0">
                    <v-layout row wrap align-center>
                        <v-flex xs3>
                            <v-text-field class="title" type="password" readonly value="#########################">
                            </v-text-field>
                        </v-flex>
                        <v-flex xs2>
                            <v-btn class="warning">Reveal</v-btn>
                        </v-flex>
                    </v-layout>
                </td>
            </template>
            <template v-slot:no-data>
                <v-alert :value="true" color="info" icon="info">
                    Add an API Key to get started
                </v-alert>
            </template>
        </v-data-table>
    </div>
</template>

<script>
    export default {
        name: "KeyConfig",
        data: () => ({
            headers: [
                {text: 'Service', value: 'service'},
                {text: 'Name', value: 'name'},
                {text: 'Last Modified', value: 'modified'},
                {text: 'Contents', value: 'contents', sortable: false},

            ],
            apiKeys: [
                {
                    name: 'Binance Read Only',
                    service: 'Binance',
                    contents: {
                        api: 't9n86g3qr69ng8q3rn698t3qrn9t7g86qr3wbn7t89ybc13n78yg9bt',
                        secret: '917435rtf91sa34c56tb2f91t2078b3c5t078v2bt8051v2tb5v4',
                    },
                    modified: {}
                }
            ],
            editKeyIndex: null,
            dialog: false,
            defaultItem: {
                name: '',
                service: '',
                contents: {'api': ''}
            },
            editedItem: {}
        }),
        methods: {
            editKey(item) {
                console.log("Editing key:")
                console.log(item)
            },
            deleteKey(item) {

            },
            addKey(item) {

            },
        },
        computed: {
            formTitle() {
                return this.apiKeys[this.editKeyIndex].name
            }
        }
    }
</script>

<style scoped>

</style>