<template>

  <div class="col-md-2 navbar-container">
    <div class="logo-container">
      <img src="@/assets/Logo.svg" alt="" class="logo-img">
    </div>

    <nav>
      <div class="top-nav">
        <ul v-if="role === 'influencer'">
          <li>
            <router-link to="/influencer"><i class="fa-solid fa-chart-line"></i>Overview</router-link>
          </li>
          <li>
            <router-link to="/influencer/campaigns"><i class="fa-solid fa-bullhorn"></i>Active Campaigns</router-link>
          </li>
          <li>
            <router-link to="/influencer/my-campaigns"><i class="fa-solid fa-list"></i>My Campaigns</router-link>
          </li>
          <li>
            <router-link to="/influencer/ad-requests"><i class="fa-solid fa-envelope"></i>Ad Requests</router-link>
          </li>
        </ul>
        <ul v-if="role === 'sponsor'">
          <li>
            <router-link to="/sponsor"><i class="fa-solid fa-chart-line"></i>Overview</router-link>
          </li>
          <li>
            <router-link to="/sponsor/influencers-list"><i class="fa-solid fa-people-group"></i>Influencers
            </router-link>
          </li>
          <li>
            <router-link to="/sponsor/campaigns"><i class="fa-solid fa-bullhorn"></i>Campaigns</router-link>
          </li>
        </ul>
        <ul v-if="role === 'admin'">
          <li>
            <router-link to="/admin"><i class="fa-solid fa-chart-line"></i>Overview</router-link>
          </li>
          <li>
            <router-link to="/admin/influencers"><i class="fa-solid fa-people-group"></i>Influencers</router-link>
          </li>
          <li>
            <router-link to="/admin/sponsors"><i class="fa-solid fa-bullhorn"></i>Sponsors</router-link>
          </li>
          <li>
            <router-link to="/admin/campaigns"><i class="fa-solid fa-bars"></i>Campaigns</router-link>
          </li>
        </ul>
      </div>
      <div class="bottom-nav">
        <ul>
          <li>
            <router-link to="/profile" v-if="role!=='admin'"><i class="fa-regular fa-user"></i>Profile</router-link>
          </li>
          <li>
            <router-link to="/" @click="logout"><i class="fa-solid fa-power-off"></i>Logout</router-link>
          </li>
        </ul>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  name: "NavBar",
  computed: {
    role() {
      return JSON.parse(localStorage.getItem("role"));
    }
  },
  methods: {
    logout() {
      localStorage.clear();
      this.$store.commit("setSearchResults",[])
      this.$router.push("/login");
    },
  }
}
</script>

<style scoped>


.navbar-container {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding: 1rem;
  height: 100vh;
  background-color: #F6F8F9;
  border-right: 2px solid #E0E0E0;
}


nav {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}


nav a {
  color: #39465B;
  text-decoration: none;
}


.logo-img {
  width: 75%;
  padding: 1em;
  height: auto;
}

ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

ul li {
  padding: 1em;
}

i {
  padding-right: 1em;
  height: 1.5em;
}

nav a {
  color: #39465B;
  text-decoration: none;
}

nav a.router-link-exact-active {
  background-color: #506582;
  color: #f5f5f5;
  padding: 0.5rem 4rem 0.5rem 0.5rem;
  border-radius: 6px;
  font-weight: 600;

}

</style>