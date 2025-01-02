<template>
  <layout-ui>
    <template v-slot:main>
      <div class="container-fluid">
        <div class="row">
          <DashboardHeading title="My Campaigns"></DashboardHeading>
        </div>
        <div class="row">
          <div class="col-md-12 content">
            <div class="table-container table-responsive">
              <table>
                <thead>
                <tr>
                  <th scope="col">ID</th>
                  <th scope="col">Name</th>
                  <th scope="col">Description</th>
                  <th scope="col">Category</th>
                  <th scope="col">Goals</th>
                  <th scope="col">Budget</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="myCampaign in myCampaigns" :key="myCampaign.id">
                  <td>{{ myCampaign.id }}</td>
                  <td>{{ myCampaign.name }}&nbsp;
                  <i v-if="myCampaign.is_flagged" class="fa-solid fa-flag"></i>
                  </td>
                  <td>{{ myCampaign.description }}
                  </td>
                  <td>{{ myCampaign.category }}</td>
                  <td>{{ myCampaign.goals }}</td>
                  <td>{{ myCampaign.budget }}</td>
                </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </template>
  </layout-ui>

</template>

<script>

import DashboardHeading from "@/components/DashboardHeading.vue";
import LayoutUi from "@/components/LayoutUi.vue";

export default {
  name: "MyCampaigns",
  components: {LayoutUi, DashboardHeading},

  computed: {
    myCampaigns() {
      return this.$store.getters.getInfluencerCampaigns;
    },
    influencerUsername() {
      return JSON.parse(localStorage.getItem('username'));
    },
  },

  async beforeMount() {
    await this.$store.dispatch("fetchInfluencerCampaigns", this.influencerUsername);
  },
}
</script>

<style scoped>
</style>