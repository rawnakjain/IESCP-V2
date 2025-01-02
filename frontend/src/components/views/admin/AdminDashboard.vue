<template>
  <layout-ui>
    <template v-slot:main>
      <div class="container-fluid">
        <div class="row">
          <dashboard-greetings :greeting="greeting"></dashboard-greetings>
        </div>
        <div class="row">
          <div class="col-md-12 content">
            <div class="btns-container">
              <button @click="changeShow('users')" class="btn-each"><span>Users</span></button>
              <button @click="changeShow('campaigns')" class="btn-each"><span>Campaigns</span></button>
              <button @click="changeShow('ads')" class="btn-each"><span>Ad Requests</span></button>
            </div>
            <div class="chart-container">
              <graph-users v-if="show==='users'"></graph-users>
              <graph-campaigns v-else-if="show==='campaigns'"></graph-campaigns>
              <graph-ads v-else-if="show==='ads'"></graph-ads>
            </div>
          </div>
        </div>
      </div>
    </template>
  </layout-ui>


</template>

<script>

import LayoutUi from "@/components/LayoutUi.vue";
import DashboardGreetings from "@/components/DashboardGreetings.vue";
import GraphUsers from "@/components/views/admin/GraphUsers.vue";
import GraphCampaigns from "@/components/views/admin/GraphCampaigns.vue";
import GraphAds from "@/components/views/admin/GraphAds.vue";


export default {
  name: "AdminDashboard",
  components: {GraphAds, GraphCampaigns, GraphUsers, DashboardGreetings, LayoutUi},
  data() {
    return {
      show: 'users',

    }
  },
  computed: {
    greeting() {
      return this.$store.getters.greeting;
    },
  },
  methods: {
    changeShow(data) {
      this.show = data;
    }
  },
  beforeMount() {
    this.$store.dispatch('fetchUserbaseData')
  }
}
</script>

<style scoped>

.chart-container {
  width: 50vw;
  height: 500px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.btns-container {
  display: flex;
  justify-content: space-around;
  margin: 1rem 0 4rem 0;
}

.btn-each {
  width: 10vw;
  font-size: 1.2rem;
  text-decoration: none;
  color: white;
  background-color: #506582;
  padding: 0.5rem 0.5rem;
  border-radius: 8px;
  margin: 0.2rem;
  font-weight: 600;
}
</style>