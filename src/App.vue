<template>
    <v-app dark>
        <v-toolbar app>
            <v-toolbar-title class="headline text-uppercase">
                <span class="font-weight-black">CRIZZLE</span>
            </v-toolbar-title>
            <v-spacer/>
            <v-toolbar-items>
                <v-btn flat><v-icon left dark>explore</v-icon>Data & Research</v-btn>
                <v-btn flat><v-icon left dark>assignment</v-icon>Portfolio</v-btn>
                <v-btn flat><v-icon left dark>assessment</v-icon>Trading</v-btn>
                <v-btn flat><v-icon left dark>settings</v-icon>Configuration</v-btn>
            </v-toolbar-items>
        </v-toolbar>
        <v-content>
            <HelloWorld/>
        </v-content>
    </v-app>
</template>

<script>
    import HelloWorld from './components/HelloWorld'

    export default {
        name: 'App',
        components: {
            HelloWorld
        },
        data() {
            return {
                //
            }
        }
    }
</script>
