<script setup>
</script>

<script>
export default {
data(){
    return {
        progressItems:[
        {
            label: 'Step 1',
            items: [
                {
                    label: 'Research interests',
                    icon: 'pi pi-code',
                    route: '/'
                }
            ]
        },{
            label: 'Step 2',
            items: [
                {
                    label: 'Prepare literatures',
                    icon: 'pi pi-book',
                    route: '/'
                }
            ]
        },
        {
            label: 'Step 3',
            items: [
                {
                    label: 'Cite suggestions',
                    icon: 'pi pi-comments',
                    route: '/booklist'
                }
            ]
        },
        {
            label: 'Step 4',
            items: [
                {
                    label: 'Wirte Outline',
                    icon: 'pi pi-list',
                    route: '/outline'
                }
            ]
        },
        {
            label: 'Step 5',
            items: [
                {
                    label: 'Write Content',
                    icon: 'pi pi-align-center',
                    route: '/'
                }
            ]
        },
        {
            label: 'Step 6',
            items: [
                {
                    label: 'Write Introduction',
                    icon: 'pi pi-sort-amount-up-alt',
                    route: '/'
                }
            ]
        },
        {
            label: 'Step 7',
            items: [
                {
                    label: 'Postprocess',
                    icon: 'pi pi-language',
                    route: '/'
                }
            ]
        }
    ]
};
}
};
</script>

<template>
<div class="appmenu">
<Menu :model="progressItems">
    <template #start>
        <router-link to="/">
            <div class="menustart">
            <span class="pi pi-compass text-primary" style="font-size: 2rem;" />
            <span class="text-xl font-semibold">GPT<span class="text-primary">AutoSurvey</span></span>
            </div>
        </router-link>
    </template>
    <template #item="{ item, props }">
        <router-link v-slot="{ href, navigate }" :to="item.route" cus tom>
            <a v-ripple :href="href" v-bind="props.action" @click="navigate">
                <span :class="item.icon" />
                <span>{{ item.label }}</span>
            </a>
        </router-link>
    </template>
</Menu>
</div>
<router-view />
</template>

<style scoped>
.appmenu {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.menustart {
  display: flex;
  padding: 10px;
  justify-items: center;
  align-items: center;
}
span{
  padding-right: 5px;
  padding-left: 5px;
}
.text-xl {
  font-size: 1.25rem;
}
.font-semibold {
  font-weight: 600;
}
.text-primary {
  color: var(--primary-color);
}
</style>
