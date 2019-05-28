<template>
    <div>
        <v-toolbar app clipped-left id="toolbar">
            <v-toolbar-side-icon @click="toggleDrawer"/>
            <v-spacer/>
            <v-toolbar-title>
                <router-link to="/" tag="span">
                    CRIZZLE
                </router-link>
            </v-toolbar-title>
            <v-spacer/>

        </v-toolbar>
        <v-navigation-drawer
                app
                clipped
                :mini-variant="sidebar.mini"
                mobile-break-point="800"
                v-model="sidebar.open"
                id="sidebar"
                class="elevation-8"
        >
            <v-list subheader>
                <div v-for="(item, i) in sidebar.navItems">
                    <v-list-tile
                            :key="item.title"
                            :to="item.endpoint ? item.endpoint : item.title.toLowerCase()"
                            ripple
                            class="elevation-0"
                            active-class="highlighted"
                    >
                        <v-list-tile-action class="icon">
                            <v-icon>{{ item.icon }}</v-icon>
                        </v-list-tile-action>
                        <v-list-tile-content>
                            <v-list-tile-title>{{ item.title }}</v-list-tile-title>
                        </v-list-tile-content>
                        <v-list-tile-action class="active_indicator">
                            <v-icon>navigate_next</v-icon>
                        </v-list-tile-action>
                    </v-list-tile>
                    <v-divider/>
                </div>
            </v-list>
        </v-navigation-drawer>
    </div>
</template>

<script>
    export default {
        name: "navigation",
        data() {
            return {
                sidebar: {
                    navItems: [
                        {title: 'Data', icon: 'dns'},
                        {title: 'Research', icon: 'explore'},
                        {title: 'Portfolio', icon: 'file_copy'},
                        {title: 'Backtesting', icon: 'replay'},
                        {title: 'Trading', icon: 'fast_forward'},
                        {title: 'Configuration', icon: 'settings'},
                        {title: 'Docs', icon: 'help'},
                    ],
                    mini: false,
                    open: true,
                }
            }
        },
        methods: {
            toggleDrawer() {
                if (!this.sidebar.open) {
                    this.sidebar.open = true;
                } else {
                    this.sidebar.mini = !this.sidebar.mini;
                }
                console.log(this.sidebar)
            },
        }
    }
</script>

<style scoped>
    #sidebar >>> .v-list__tile {
        transition-duration: 0.1s;
        transition-delay: 0s;
        transition-property: all;
    }

    #sidebar >>> .v-list__tile__title {
        transition-duration: inherit;
        transition-delay: 0s;
    }

    #sidebar >>> .highlighted {
        height: 75px !important;
        font-size: 1.3em;
    }

    #sidebar.v-navigation-drawer--mini-variant >>> .highlighted > .icon {
        color: #4CAF50;
    }

    #sidebar >>> .active_indicator {
        opacity: 0;
        transition: opacity 0.3s ease-out;
    }

    #sidebar >>> .v-list__tile:hover > .active_indicator {
        opacity: 1;
    }

    #sidebar >>> .highlighted > .active_indicator {
        opacity: 1;
    }

    #toolbar >>> .v-toolbar__title {
        cursor: pointer;
    }
</style>