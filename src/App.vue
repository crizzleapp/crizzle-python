<template>
    <v-app dark>
        <Navigation/>
        <v-content>
            <v-container fluid>
                <router-view/>
            </v-container>
        </v-content>
    </v-app>
</template>

<script>
    import Navigation from "./components/navigation";

    export default {
        name: 'App',
        components: {
            Navigation,
        },
        data() {
            return {}
        }
    }
</script>
