<template>
<layout-ui>
    <template v-slot:main>
      <div class="container-fluid">
        <div class="row">
          <DashboardHeading title="All Sponsors"></DashboardHeading>
        </div>
        <div class="row">
          <div class="col-md-12 content">
            <div class="table-container table-responsive">
              <table>
                <thead>
                <tr>
                  <th scope="col">Id</th>
                  <th scope="col">Username</th>
                  <th scope="col">Industry</th>
                  <th scope="col">Budget</th>
                  <th scope="col">Actions</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="sponsor in sponsors" :key="sponsor.id">
                  <td>{{ sponsor.id }}</td>
                  <td>{{ sponsor.username }} &nbsp;
                  </td>
                  <td>{{ sponsor.industry }}</td>
                  <td>{{ sponsor.budget }}</td>
                  <td v-if="sponsor.active">
                    approved
                  </td>
                  <td v-else>
                    <button class="btn-approve" @click="approveSponsor(sponsor.id)"><span>Approve</span></button>
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
import DashboardHeading from "@/components/DashboardHeading.vue";
import LayoutUi from "@/components/LayoutUi.vue";

export default {
  name: "AllSponsors" ,
  components: {LayoutUi, DashboardHeading},
  computed:{
    sponsors(){
      return this.$store.getters.getSponsors;
    }
  },
  methods:{
    approveSponsor(id){
      this.$store.dispatch("approveSponsor", id);
    }
  },

  beforeMount() {
    this.$store.dispatch("fetchAllSponsors");
  },
}
</script>

<style scoped>
body {
  background-color: #f8f9fa; /* Replace with your desired body color */
}

.content {
  margin-top: 2rem;
}

.btn-approve{
  font-size: 0.8rem;
  text-decoration: none;
  color: white;
  background-color: #506582;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  margin: 0.2rem;
  font-weight: 600;
}
</style>