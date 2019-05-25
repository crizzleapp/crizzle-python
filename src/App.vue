<template>
    <v-app dark class="grey darken-4">
        <Sidebar/>
        <v-content>
            <router-view/>
        </v-content>
    </v-app>
</template>

<script>
    import Sidebar from "./components/sidebar";

    export default {
        name: 'App',
        components: {
            Sidebar,
        },
        data() {
            return {}
        }
    }
</script>
