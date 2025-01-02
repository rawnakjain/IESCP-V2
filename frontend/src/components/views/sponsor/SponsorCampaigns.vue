<template>
  <layout-ui>
    <template v-slot:main>
      <div class="container-fluid">
        <div class="row">
          <DashboardHeading title="Your Campaigns"></DashboardHeading>
        </div>
        <div class="row" >
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
                  <th scope="col">Actions</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="sponsorCampaign in sponsorCampaigns" :key="sponsorCampaign.id">
                  <td>{{ sponsorCampaign.id }}</td>
                  <td>{{ sponsorCampaign.name }}&nbsp;
                    <i v-if="sponsorCampaign.is_flagged" class="fa-solid fa-flag"></i>
                  </td>
                  <td>{{ sponsorCampaign.description }}
                  </td>
                  <td>{{ sponsorCampaign.category }}</td>
                  <td>{{ sponsorCampaign.goals }}</td>
                  <td>{{ sponsorCampaign.budget }}</td>
                  <td>
                    <router-link :to="`/sponsor/campaigns/update/${sponsorCampaign.id}`" class="btn blue"><i class="fa-solid fa-pencil"></i></router-link>
                    <button class="btn blue" @click="deleteCampaign(sponsorCampaign.id)"><i class="fa-solid fa-trash"></i></button>
                    <router-link :to="`/sponsor/campaigns/view/${sponsorCampaign.id}`" class="btn-view">View</router-link>
                  </td>
                </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-md-12 create-container">
            <router-link to="/sponsor/campaigns/create" class="create-btn"><i class="fa-solid fa-plus"></i></router-link>
          </div>
        </div>
      </div>
    </template>
  </layout-ui>
</template>

<script>


import LayoutUi from "@/components/LayoutUi.vue";
import DashboardHeading from "@/components/DashboardHeading.vue";

export default {
  name: "SponsorCampaigns",
  components: {DashboardHeading, LayoutUi},
  computed: {
    sponsorCampaigns() {
      return this.$store.getters.getSponsorCampaigns;
    }
  },
  methods: {
    deleteCampaign(id) {
      this.$store.dispatch("deleteSponsorCampaign", id);
    }
  },
  beforeMount() {
    this.$store.dispatch("fetchSponsorCampaigns");
  },
}

</script>

<style scoped>

.create-btn {
  font-size: 2rem;
  font-weight: 600;
  background-color: #506582;
  color: white;
  padding: 0.5rem 1rem 0.5rem 1rem;
  border-radius: 50%;
  text-decoration: none;
  margin: 1.5rem 0 1rem 0;
}

.create-container {
  display: flex;
  justify-content: center;
}

.blue i{
  color:#506582;
}

.btn-view{
  font-size:0.8rem;
  text-decoration: none;
  color: white;
  background-color: #506582;
  padding: 0.5rem 0.5rem;
  border-radius: 5px;
  margin: 1rem;
  font-weight: 600;
}
</style>