<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-md-7 left-side">
        <div class="header">
          <div class="logo-img">
            <img src="../../assets/Logo.svg" alt="">
          </div>
          <div class="get-started-text">
            <h1 class="display-2">Get Started Today.</h1>
          </div>
          <div class="buttons">
            <router-link to="/register/influencer">
              <p class="btn">
                <img src="../../assets/influencer-button.png" alt="">
                I am a Influencer looking to collaborate with Sponsors </p>
            </router-link>
            <router-link to="/register/sponsor">
              <p class="btn"  >
                <img src="../../assets/sponsor-button.png" alt="" class="btn-img">
                I am a Sponsor looking to collaborate with Influencers</p>
            </router-link>
          </div>
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

export default {
  name: 'GetStarted',
  components:{AlreadyLink, RightStatic},
  data() {
    return {
    alreadyLink: {"text": "Already have an account? Log in", "link": "/login"},
    }
  },
  methods: {}
}
</script>


<style scoped>

.white-font {
  color: #ffffff;
}


.left-side {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  //width: 100%;
  height: 100vh;
  background-color: #f5f5f5;
}


.get-started-text h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #454545;
}


.header {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 1rem;
}


.header div {
  margin-top: 1rem;
}


.buttons {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}


.buttons .btn {
  border: 1px solid #39465B;
  border-radius: 7px;
  padding: 6px 14px;
  font-size: 1.1rem;
  font-weight: 650;
  margin-bottom: 1.5rem;
}

.buttons p {
  color: #39465B;
}

.buttons img {
  height: 32px;
}




@media (max-width: 576px) {

  .logo-img img{
    width: 15em;
  }

  .get-started-text h1{
    font-size:2rem;
  }

  .right-side .description, .join-us {
    display: none;
  }


  .right-side .heading h1 {
    font-size: 1rem;
  }


  .left-side {
    height: 85vh;
  }


  .right-side {
    height: 15vh;
    padding: 0;
    margin: 0;
    position: relative;
  }


  .heading {
    display: flex;
    justify-content: space-evenly;
    align-items: flex-start;
  }

  .heading h1{
    margin-top: -3rem;
  }
}
</style>