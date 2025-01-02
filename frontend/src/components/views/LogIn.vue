<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-md-7 left-side">
        <div class="logo">
          <img src="../../assets/Logo.svg" alt="">
        </div>
        <div class="form-container">
          <div class="form-heading">
            <h1> Log In</h1>
          </div>
          <form class="form" @submit.prevent="login">
            <div class="form-group">
              <label for="username"> Username </label>
              <input type="text" id="username" name="username" class="inputs form-control shadow-none"
                     v-model="form.username" required>
            </div>
            <div class="form-group">
              <label for="password">Password</label>
              <input type="password" id="password" name="password" class="inputs form-control shadow-none"
                     v-model="form.password" required>
            </div>
            <div class="error" v-if="error">
              <p> "{{ error }} </p>
            </div>
            <input type="submit" value="Log In" class="inputs form-control submit-btn shadow-none">
          </form>
        </div>
        <already-link :text="alreadyLink.text" :link="alreadyLink.link"></already-link>
      </div>
      <right-static></right-static>
    </div>
  </div>
</template>


<script>
import RightStatic from "@/components/sign-page/RightStatic.vue";
import AlreadyLink from "@/components/sign-page/AlreadyLink.vue";
import {mapGetters} from "vuex";

export default {
  name: 'LogIn',
  components: {AlreadyLink, RightStatic,},
  data() {
    return {
      alreadyLink: {"text": "Don't have an account? Register", "link": "/register"},
      form: {
        username: "",
        password: "",
      },
    }
  },
  computed: {
    ...mapGetters(["getAuth", "getStatus", "getError"]),
    error(){
      return this.$store.getters.getError
    },
  },
  methods: {
    async login() {
      await this.$store.dispatch("login", this.form);
      if (this.getAuth.token) {
        if (this.getAuth.role === "sponsor") {
          this.$router.push("/sponsor");
        } else if (this.getAuth.role === "influencer") {
          this.$router.push("/influencer");
        } else if (this.getAuth.role === "admin") {
          this.$router.push("/admin");
        }
      }
    },
  },
  mounted() {
    if (localStorage.token) {
      this.$router.push('/' + JSON.parse(localStorage.role));
    }
  }
}
</script>

<style scoped>

.container-fluid {
  height: auto;
}


.left-side {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 2em;
  background-color: #f5f5f5;
}


.logo img {
  margin: 0 0 3vh -15vw;
}


.form-heading h1 {
  color: #454545;
  font-family: "Raleway", sans-serif;
  font-optical-sizing: auto;
  font-weight: bolder;
  font-size: 2rem;
}

.form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}


.form .form-group {
  margin-top: 1em;
}


.inputs {
  width: 30vw;
  padding: 0.5em;
  border-radius: 0.5em;
  border: 1px solid #000000;
  font-size: 1rem;
  font-family: "Raleway", sans-serif;
  font-weight: 500;
}


.submit-btn {
  background: linear-gradient(to right, #2C3646, #506582);
  color: white;
  padding: 8px;
  border-radius: 5px;
  font-size: 1.2rem;
  font-family: "Raleway", sans-serif;
  font-weight: bold;
  margin-top: 2rem;
  margin-bottom: 1rem;
}

.error{
  margin-top:1rem;
  margin-bottom: -2rem;
  color: red;
  font-size: 1rem;
  font-family: "Raleway", sans-serif;
  font-weight: 400;
}

@media (max-width: 576px) {
  .left-side {
    padding: 1em;
    margin-bottom: 1em;
    height: 85vh;
  }

  .inputs {
    width: 80vw;
  }


  .form-heading h1 {
    font-size: 1.5rem;
  }
}
</style>