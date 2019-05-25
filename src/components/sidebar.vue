<template>
    <v-navigation-drawer app id="sidebar" class="elevation-8 grey darken-4">
        <v-list subheader>
            <div v-for="item in navItems" :key="item.title">
                <v-list-tile @click="" ripple replace
                             :to="{path: item.endpoint ? item.endpoint : item.title.toLowerCase()}">
                    <v-list-tile-action>
                        <v-icon>{{ item.icon }}</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>
                        <v-list-tile-title>{{ item.title }}</v-list-tile-title>
                    </v-list-tile-content>
                </v-list-tile>
            </div>
        </v-list>
    </v-navigation-drawer>
</template>

<script>
    export default {
        name: "sidebar",
        data() {
            return {
                navItems: [
                    {title: 'CRIZZLE', icon: 'home', endpoint: "/"},
                    {title: 'Data', icon: 'dns'},
                    {title: 'Research', icon: 'explore'},
                    {title: 'Portfolio', icon: 'file_copy'},
                    {title: 'Backtesting', icon: 'replay'},
                    {title: 'Trading', icon: 'fast_forward'},
                    {title: 'Configuration', icon: 'settings'},
                    {title: 'Docs', icon: 'help'},
                ]
            }
        }
    }
</script>

<style scoped>

</style>