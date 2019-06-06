<template xmlns="http://www.w3.org/1999/XSL/Transform">
    <v-card>
        <v-tabs grow v-model="tab">
            <v-tab v-for="tab in tabs" :key="tab.title">
                {{tab.title}}
            </v-tab>
        </v-tabs>
        <v-tabs-items v-model="tab">
            <v-tab-item v-for="tab in tabs" :key="tab.title">
                <v-card flat>
                    <v-card-text>
                        <component :is="tab.component"/>
                    </v-card-text>
                </v-card>
            </v-tab-item>
        </v-tabs-items>
    </v-card>
</template>

<script>
    import KeyConfig from "../components/Configuration/KeyConfig";

    export default {
        name: "configuration",
        components: {
            KeyConfig
        },
        data() {
            return {
                tab: 0,
                tabs: [
                    {
                        title: 'API Keys',
                        component: KeyConfig,
                    },
                ]
            }
        },
    }
</script>