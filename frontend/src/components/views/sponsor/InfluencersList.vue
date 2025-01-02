<template>
  <layout-ui>
    <template v-slot:main>
      <div class="container-fluid">
        <div class="row">
          <DashboardHeading title="Active Influencers"></DashboardHeading>
        </div>
        <div class="row">
          <div class="col-md-12 content">
            <div class="table-container table-responsive">
              <table>
                <thead>
                <tr>
                  <th scope="col">Id</th>
                  <th scope="col">Username</th>
                  <th scope="col">Category</th>
                  <th scope="col">Niche</th>
                  <th scope="col">Reach</th>
                  <th scope="col">Actions</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="influencer in influencers" :key="influencer.id">
                  <td>{{ influencer.id }}</td>
                  <td>{{ influencer.username }}
                    <i v-if="influencer.is_verified" class="fas fa-check-circle text-primary"></i>
                  </td>
                  <td>{{ influencer.category }}</td>
                  <td>{{ influencer.niche }}</td>
                  <td>{{ influencer.reach }}</td>
                  <td>
                    <button class="btn"><router-link to="/sponsor/ads/create"> Request </router-link></button>
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

<script>
import LayoutUi from "@/components/LayoutUi.vue";
import DashboardHeading from "@/components/DashboardHeading.vue";

export default {
  name: "SponsorInfluencers",
  components: {LayoutUi, DashboardHeading},
  beforeMount() {
    this.$store.dispatch("fetchInfluencers");
  },
  computed: {
    influencers() {
      return this.$store.getters.getInfluencers;
    }
  },
  methods:{
    setAdCreate(influencer){
      this.$store.commit("setAdCreate", influencer);
    }
  }
}
</script>

<style scoped>
body {
  background-color: #f8f9fa; /* Replace with your desired body color */
}

.content {
  margin-top: 2rem;
}

.btn a{
  font-size:0.8rem;
  text-decoration: none;
  color: white;
  background-color: #506582;
  padding: 0.5rem 0.5rem;
  border-radius: 5px;
  margin: 0.5rem;
  font-weight: 600;

}

</style>