<script>
import DashboardHeading from "@/components/DashboardHeading.vue";
import LayoutUi from "@/components/LayoutUi.vue";

export default {
  name: "ActiveCampaigns",
  components: {LayoutUi, DashboardHeading},
  computed: {
    allCampaigns() {
      return this.$store.getters.getAllCampaigns;
    }
  },
  beforeMount() {
    this.$store.dispatch("fetchAllCampaigns");
  },
}
</script>

<template>
  <layout-ui>
    <template v-slot:main>
      <div class="container-fluid">
        <div class="row">
          <DashboardHeading title="Active Campaigns"></DashboardHeading>
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
                  <th scope="col">Actions</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="allCampaign in allCampaigns" :key="allCampaign.id">
                  <td>{{ allCampaign.id }}</td>
                  <td>{{ allCampaign.name }}&nbsp;
                    <i v-if="allCampaign.is_flagged" class="fa-solid fa-flag"></i>
                  </td>
                  <td>{{ allCampaign.description }}
                  </td>
                  <td>{{ allCampaign.category }}</td>
                  <td>{{ allCampaign.goals }}</td>
                  <td>{{ allCampaign.budget }}</td>
                  <td>
                    <button class="btn">
                      <router-link :to="{ path: '/influencer/ads/create', query: { role: 'influencer' } }">Request
                      </router-link>
                    </button>
                  </td>
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

<style scoped>

.btn a {
  font-size: 0.8rem;
  text-decoration: none;
  color: white;
  background-color: #506582;
  padding: 0.5rem 0.5rem;
  border-radius: 5px;
  margin: 0.5rem;
  font-weight: 600;
}
</style>